"""Renderizador 3D (relevo + extrusão) da marca do leão, sem dependências além de numpy/cv2/PIL."""
import sys, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

LOGO = '/Users/gilbertosena/Desktop/GilbertoOS/identidade/logo-transparente-crop.png'
SUP = '/System/Library/Fonts/Supplemental/'
SYS = '/System/Library/Fonts/'
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
ONLY = sys.argv[2] if len(sys.argv) > 2 else 'all'
rng = np.random.default_rng(7)


def hexrgb(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], np.float32)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- máscaras
def lion_mask(w):
    a = np.array(Image.open(LOGO).convert('RGBA'))[..., 3].astype(np.float32) / 255
    b = (a > 0.5).astype(np.uint8)
    # tira sujeira pequena do arquivo (manchas soltas)
    n, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
    keep = np.zeros_like(b)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 60:
            keep[lab == i] = 1
    a = a * keep
    h = int(round(a.shape[0] * w / a.shape[1]))
    m = cv2.resize(a, (w, h), interpolation=cv2.INTER_CUBIC)
    m = cv2.GaussianBlur(m, (0, 0), w / 1400)
    return np.clip((m - 0.5) * 3 + 0.5, 0, 1).astype(np.float32)


def text_mask(text, font, size, track=0, idx=0):
    f = ImageFont.truetype(font, size, index=idx)
    widths = [f.getlength(c) for c in text]
    total = int(sum(widths) + track * (len(text) - 1)) + 40
    asc, desc = f.getmetrics()
    im = Image.new('L', (total, asc + desc + 40), 0)
    d = ImageDraw.Draw(im)
    x = 20
    for c, wc in zip(text, widths):
        d.text((x, 20), c, font=f, fill=255)
        x += wc + track
    a = np.array(im).astype(np.float32) / 255
    ys, xs = np.where(a > 0.02)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def paste_max(canvas, m, x, y):
    h, w = m.shape
    canvas[y:y + h, x:x + w] = np.maximum(canvas[y:y + h, x:x + w], m)


# ---------------------------------------------------------------- geometria
def height(mask, bevel, profile='round'):
    b = (mask > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(b, cv2.DIST_L2, 5)
    t = np.clip(d / bevel, 0, 1)
    h = np.sin(t * np.pi / 2) if profile == 'round' else t
    h = cv2.GaussianBlur(h.astype(np.float32), (0, 0), max(0.8, bevel * 0.06))
    return h


def normals(Hpx):
    gx = cv2.Sobel(Hpx, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(Hpx, cv2.CV_32F, 0, 1, ksize=3) / 8
    n = np.stack([-gx, -gy, np.ones_like(gx)], -1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def unit(v):
    v = np.array(v, np.float32)
    return v / np.linalg.norm(v)


# ---------------------------------------------------------------- materiais
def studio_env(r, key=(-0.55, -0.6, 0.58), fill=(0.7, -0.2, 0.68), keyw=0.05, horizon=0.2):
    up = -r[..., 1]
    base = 0.18 + 0.62 * smoothstep(-0.4, 0.9, up)
    base = base - horizon * np.exp(-((up + 0.05) / 0.09) ** 2)
    k = unit(key); f = unit(fill)
    dk = (r * k).sum(-1); df = (r * f).sum(-1)
    base = base + 1.6 * np.exp(-(1 - dk) / keyw) + 0.55 * np.exp(-(1 - df) / 0.12)
    return base


def reflect(n):
    v = np.array([0, 0, 1], np.float32)
    nv = n[..., 2:3]
    return 2 * nv * n - v


def tone(c):
    return 1 - np.exp(-np.clip(c, 0, None) * 1.35)


def screen_grad(shape, a=0.35):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    g = 1 - (0.6 * yy / h + 0.4 * xx / w)  # mais claro em cima à esquerda
    return a * (g - 0.5)


def metal(n, tint, mask, brushed=0.0, flat_lift=0.0, key=(-0.55, -0.6, 0.58)):
    r = reflect(n)
    e = studio_env(r, key=key)
    flat = smoothstep(0.985, 0.999, n[..., 2])
    e = e + flat * flat_lift + screen_grad(mask.shape, 0.4) * flat
    if brushed:
        h, w = mask.shape
        nz = rng.standard_normal((h, w)).astype(np.float32)
        nz = cv2.blur(nz, (151, 1))
        nz = nz / (nz.std() + 1e-6)
        e = e * (1 + brushed * nz * (0.4 + 0.6 * flat))
    c = tone(e[..., None] * tint[None, None, :] * 1.15)
    return c


def noise_field(shape, scales=(400, 160, 60, 24), seed=3):
    g = np.random.default_rng(seed)
    h, w = shape
    acc = np.zeros(shape, np.float32)
    amp = 1.0
    for s in scales:
        small = g.standard_normal((max(2, h // s), max(2, w // s))).astype(np.float32)
        acc += amp * cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
        amp *= 0.5
    return acc / acc.std()


def marble_albedo(shape, base, vein, seed=5):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = noise_field(shape, seed=seed)
    t2 = noise_field(shape, scales=(250, 90, 30), seed=seed + 1)
    v1 = np.abs(np.sin((xx * 0.0016 + yy * 0.0011) * 9 + t * 2.4))
    v2 = np.abs(np.sin((xx * 0.0009 - yy * 0.0019) * 7 + t2 * 2.8))
    veins = np.clip(1 - v1 ** 0.18, 0, 1) * 0.9 + np.clip(1 - v2 ** 0.12, 0, 1) * 0.45
    cloud = 0.05 * noise_field(shape, scales=(120, 40), seed=seed + 2)
    k = np.clip(veins, 0, 1)[..., None]
    alb = base[None, None] * (1 - k) + vein[None, None] * k
    return np.clip(alb + cloud[..., None], 0, 1)


def stone(n, albedo, gloss=0.6, L=(-0.5, -0.65, 0.58)):
    L = unit(L)
    ndl = np.clip((n * L).sum(-1), 0, 1)
    diff = 0.42 + 0.7 * ndl
    hv = unit(L + np.array([0, 0, 1], np.float32))
    spec = np.clip((n * hv).sum(-1), 0, 1) ** 90 * 0.9
    r = reflect(n)
    env = studio_env(r) * 0.12
    fres = (1 - n[..., 2]) ** 3
    c = albedo * diff[..., None] + (gloss * (spec + env * (0.3 + fres)))[..., None]
    return np.clip(c, 0, 1)


# ---------------------------------------------------------------- composição 3D
def shift(a, dx, dy):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR, borderValue=0)


def extrude(face_rgb, mask, depth, side_top, side_bot, direction=(0.28, 1.0), steps=None):
    """Monta a peça: paredes laterais (empilhadas na direção dada) + face por cima. Retorna RGB, alpha."""
    d = unit(direction)
    steps = steps or int(depth)
    h, w = mask.shape
    rgb = np.zeros((h, w, 3), np.float32)
    al = np.zeros((h, w), np.float32)
    for i in range(steps, 0, -1):
        k = depth * i / steps
        m = shift(mask, d[0] * k, d[1] * k)
        t = i / steps
        col = side_top * (1 - t) + side_bot * t
        rgb = rgb * (1 - m[..., None]) + col[None, None] * m[..., None]
        al = np.maximum(al, m)
    # escurece a quina logo abaixo da face (oclusão)
    edge = np.clip(shift(mask, d[0] * 2, d[1] * 2) - mask, 0, 1)
    rgb = rgb * (1 - 0.35 * edge[..., None])
    rgb = rgb * (1 - mask[..., None]) + face_rgb * mask[..., None]
    al = np.maximum(al, mask)
    return rgb, al


def shadow(alpha, dx, dy, blur, strength):
    s = shift(alpha, dx, dy)
    s = cv2.GaussianBlur(s, (0, 0), blur)
    return np.clip(s * strength, 0, 1)


def over(bg_rgb, rgb, a):
    return bg_rgb * (1 - a[..., None]) + rgb * a[..., None]


def save_rgba(rgb, a, path):
    out = np.dstack([np.clip(rgb, 0, 1), np.clip(a, 0, 1)])
    Image.fromarray((out * 255 + 0.5).astype(np.uint8), 'RGBA').save(path, optimize=True)


def save_rgb(rgb, path):
    Image.fromarray((np.clip(rgb, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGB').save(path, optimize=True)


def trim(rgb, a, pad):
    ys, xs = np.where(a > 0.01)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    y0 = max(0, y0 - pad); x0 = max(0, x0 - pad)
    y1 = min(a.shape[0], y1 + pad); x1 = min(a.shape[1], x1 + pad)
    return rgb[y0:y1, x0:x1], a[y0:y1, x0:x1]


# =============================================================== OPÇÃO 1: aço escovado, empilhada
def opcao1():
    W, H = 3600, 3600
    m = np.zeros((H, W), np.float32)
    lion = lion_mask(1900)
    ly = 520
    paste_max(m, lion, (W - lion.shape[1]) // 2, ly)
    name = text_mask('GILBERTO SENA', SUP + 'Didot.ttc', 330, track=34, idx=0)
    ny = ly + lion.shape[0] + 230
    nm = np.zeros_like(m); paste_max(nm, name, (W - name.shape[1]) // 2, ny)
    sub = text_mask('BUSINESS ADVISOR & CONSULTANT', SYS + 'Avenir Next.ttc', 92, track=40, idx=5)
    sy = ny + name.shape[0] + 170
    sm = np.zeros_like(m); paste_max(sm, sub, (W - sub.shape[1]) // 2, sy)
    # fio fino entre nome e serviço
    rule = np.zeros_like(m)

    tint = hexrgb('#D9DCE0')
    Hl = height(lion, 26) * 26
    Hlion = np.zeros_like(m); paste_max(Hlion, Hl, (W - lion.shape[1]) // 2, ly)
    Hn = height(nm, 7) * 7
    Htot = np.maximum(Hlion, Hn)
    n = normals(Htot)
    face_mask = np.maximum(m, nm)
    face = metal(n, tint, face_mask, brushed=0.10, flat_lift=0.8)
    side_top = hexrgb('#8E939A'); side_bot = hexrgb('#4A4E54')
    rgb, al = extrude(face, face_mask, 34, side_top, side_bot, direction=(0.22, 1.0))
    # serviço e fio: grafite chapado, sem relevo (texto pequeno não aguenta bisel)
    ink = hexrgb('#2B2E33')
    flat = np.maximum(sm, rule)
    rgb = rgb * (1 - flat[..., None]) + ink * flat[..., None]
    al = np.maximum(al, flat)

    rgb_t, al_t = trim(rgb, al, 80)
    save_rgba(rgb_t, al_t, f'{OUT}/opcao-1-aco-escovado-transparente.png')
    bg = np.ones((H, W, 3), np.float32) * hexrgb('#F2F0EB')
    sh = shadow(np.maximum(al - flat, 0), 30, 70, 38, 0.28)
    out = over(bg, np.zeros_like(bg) + hexrgb('#5B5650'), sh)
    out = over(out, rgb, al)
    save_rgb(out, f'{OUT}/opcao-1-aco-escovado-fundo-claro.png')


# =============================================================== OPÇÃO 2: mármore branco, horizontal, fundo escuro
def opcao2():
    W, H = 5200, 2400
    lion = lion_mask(1600)
    lx, ly = 420, (H - lion.shape[0]) // 2 - 20
    m = np.zeros((H, W), np.float32); paste_max(m, lion, lx, ly)
    tx = lx + lion.shape[1] + 330
    l1 = text_mask('GILBERTO', SUP + 'Futura.ttc', 360, track=60, idx=0)
    l2 = text_mask('SENA', SUP + 'Futura.ttc', 360, track=60, idx=0)
    sub = text_mask('BUSINESS ADVISOR & CONSULTANT', SUP + 'Futura.ttc', 96, track=34, idx=0)
    block_h = l1.shape[0] + 110 + l2.shape[0] + 170 + sub.shape[0]
    y0 = (H - block_h) // 2 - 20
    tm = np.zeros_like(m)
    paste_max(tm, l1, tx, y0)
    paste_max(tm, l2, tx, y0 + l1.shape[0] + 110)
    sy = y0 + l1.shape[0] + 110 + l2.shape[0] + 170
    sm = np.zeros_like(m); paste_max(sm, sub, tx, sy)
    # fio vertical entre leão e nome
    rule = np.zeros_like(m)
    rx = lx + lion.shape[1] + 165
    rule[ly + 180:ly + lion.shape[0] - 180, rx:rx + 5] = 1
    rule = cv2.GaussianBlur(rule, (0, 0), 1.0)

    Hl = height(m, 30) * 30
    Ht = height(tm, 9) * 9
    Htot = np.maximum(Hl, Ht)
    n = normals(Htot)
    face_mask = np.maximum(m, tm)
    alb = marble_albedo((H, W), hexrgb('#EEEBE5'), hexrgb('#8C8A87'))
    face = stone(n, alb, gloss=0.55)
    side_top = hexrgb('#BDB8B0'); side_bot = hexrgb('#6E6A64')
    rgb, al = extrude(face, face_mask, 40, side_top, side_bot, direction=(0.3, 1.0))
    ink = hexrgb('#A8A196')
    flat = np.maximum(sm, rule)
    rgb = rgb * (1 - flat[..., None]) + ink * flat[..., None]
    al = np.maximum(al, flat)

    rgb_t, al_t = trim(rgb, al, 80)
    save_rgba(rgb_t, al_t, f'{OUT}/opcao-2-marmore-transparente.png')
    bgc = hexrgb('#141A18')
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vig = np.clip(1.15 - 0.55 * np.hypot((xx - W * 0.42) / W, (yy - H * 0.45) / H), 0.6, 1.15)
    bg = bgc[None, None] * vig[..., None]
    sh = shadow(np.maximum(al - flat, 0), 40, 80, 45, 0.55)
    out = over(bg, np.zeros_like(bg) + hexrgb('#050706'), sh)
    out = over(out, rgb, al)
    save_rgb(out, f'{OUT}/opcao-2-marmore-fundo-escuro.png')


# =============================================================== OPÇÃO 3: medalha de cobre (selo)
def arc_text(canvas, text, font, size, R, cx, cy, top=True, track=0, idx=0):
    f = ImageFont.truetype(font, size, index=idx)
    adv = [f.getlength(c) + track for c in text]
    total = sum(adv) - track
    ang = total / R
    pos = -ang / 2
    for c, a in zip(text, adv):
        mid = pos + (a - track) / 2 / R
        pos += a / R
        if c == ' ':
            continue
        box = int(size * 2)
        im = Image.new('L', (box, box), 0)
        d = ImageDraw.Draw(im)
        bb = d.textbbox((0, 0), c, font=f)
        gw, gh = bb[2] - bb[0], bb[3] - bb[1]
        d.text(((box - gw) / 2 - bb[0], (box - gh) / 2 - bb[1]), c, font=f, fill=255)
        deg = np.degrees(mid)
        if top:
            px, py = cx + R * np.sin(mid), cy - R * np.cos(mid)
            im = im.rotate(-deg, resample=Image.BICUBIC)
        else:
            px, py = cx + R * np.sin(mid), cy + R * np.cos(mid)
            im = im.rotate(deg, resample=Image.BICUBIC)
        g = np.array(im).astype(np.float32) / 255
        paste_max(canvas, g, int(px - box / 2), int(py - box / 2))


def opcao3():
    S = 3600
    cx = cy = S // 2
    R = 1440
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    rr = np.hypot(xx - cx, yy - cy)
    disk = np.clip(R - rr + 0.5, 0, 1)
    # alturas: borda alta, faixa do texto, anel de contas, campo rebaixado
    rim = smoothstep(R - 10, R - 70, rr) * smoothstep(R - 175, R - 120, rr)  # aro externo
    band = smoothstep(R - 175, R - 200, rr) * smoothstep(R - 470, R - 445, rr)
    inner_ring = np.exp(-((rr - (R - 500)) / 9) ** 2)
    field_r = R - 540
    dome = 1 - (rr / R) ** 2
    Hc = 18 * dome * disk + 70 * rim + 30 * band + 34 * inner_ring
    Hc = Hc + 22 * smoothstep(R - 4, R - 40, rr)  # bisel da borda
    # contas no anel interno
    beads = np.zeros((S, S), np.float32)
    nb = 120
    for i in range(nb):
        t = 2 * np.pi * i / nb
        bx, by = cx + (R - 500) * np.sin(t), cy - (R - 500) * np.cos(t)
        cv2.circle(beads, (int(bx), int(by)), 9, 1.0, -1, lineType=cv2.LINE_AA)
    Hc = np.where(beads > 0, np.maximum(Hc, 30 + 14 * beads), Hc)

    # texto em arco, em relevo dentro da faixa
    tm = np.zeros((S, S), np.float32)
    font = SUP + 'Copperplate.ttc'
    arc_text(tm, 'GILBERTO SENA', font, 190, R - 320, cx, cy, top=True, track=46, idx=1)
    arc_text(tm, 'BUSINESS ADVISOR & CONSULTANT', font, 128, R - 330, cx, cy, top=False, track=20, idx=0)
    # dois losangos separando as frases
    for side in (-1, 1):
        x = cx + side * (R - 322)
        pts = np.array([[x, cy - 26], [x + 20, cy], [x, cy + 26], [x - 20, cy]], np.int32)
        cv2.fillPoly(tm, [pts], 1.0, lineType=cv2.LINE_AA)
    tm = tm * band
    Ht = height(tm, 6) * 26

    lion = lion_mask(1460)
    lm = np.zeros((S, S), np.float32)
    lx, ly = cx - lion.shape[1] // 2 + 20, cy - lion.shape[0] // 2 + 10
    paste_max(lm, lion, lx, ly)
    Hl = height(lm, 22) * 52

    Htot = Hc + np.maximum(Ht, Hl)
    n = normals(Htot.astype(np.float32))
    tint = hexrgb('#EE9A70')  # cobre
    key = (-0.5, -0.65, 0.57)
    face_po = metal(n, tint, disk, flat_lift=0.75, key=key)
    face_fo = metal(n, tint, disk, flat_lift=0.05, key=key)
    raised = np.clip(np.maximum(lm, tm), 0, 1)[..., None]
    face = face_po * raised + face_fo * (1 - raised)
    # campo jateado: mais escuro e granulado, pra o leão polido saltar
    field = ((rr < field_r).astype(np.float32) * (1 - lm))[..., None]
    grain = 1 + 0.07 * cv2.GaussianBlur(rng.standard_normal((S, S)).astype(np.float32), (0, 0), 0.9)
    matte = face_fo * 0.62 * grain[..., None]
    face = face * (1 - field) + matte * field
    # sombra de contato nos rebaixos
    cav = np.clip(cv2.GaussianBlur(Htot, (0, 0), 6) - Htot, 0, 8) / 8
    face = face * (1 - 0.35 * cav[..., None])

    side_top = hexrgb('#9A5236'); side_bot = hexrgb('#4A2418')
    rgb, al = extrude(face, disk, 80, side_top, side_bot, direction=(0.0, 1.0), steps=80)
    # serrilhado na espessura da moeda
    h_, w_ = disk.shape
    teeth = 0.85 + 0.15 * (np.sin(np.arctan2(yy - cy, xx - cx) * 420) > 0)
    sidemask = np.clip(al - disk, 0, 1)
    rgb = rgb * (1 - sidemask[..., None]) + rgb * teeth[..., None] * sidemask[..., None]

    rgb_t, al_t = trim(rgb, al, 60)
    save_rgba(rgb_t, al_t, f'{OUT}/opcao-3-medalha-cobre-transparente.png')
    bgc = hexrgb('#3B1519')
    vig = np.clip(1.12 - 0.6 * np.hypot((xx - cx) / S, (yy - cy * 0.9) / S), 0.55, 1.1)
    bg = bgc[None, None] * vig[..., None]
    sh = shadow(al, 30, 90, 60, 0.6)
    out = over(bg, np.zeros_like(bg) + hexrgb('#12060A'), sh)
    out = over(out, rgb, al)
    save_rgb(out, f'{OUT}/opcao-3-medalha-cobre-fundo-vinho.png')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for k, f in (('1', opcao1), ('2', opcao2), ('3', opcao3)):
        if ONLY in ('all', k):
            f(); print('ok', k, flush=True)
