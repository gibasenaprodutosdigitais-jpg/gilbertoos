"""Remonta um reel a partir de varios trechos da mesma gravacao, pulando o
que estava errado. Legenda e som seguem o mesmo caminho do cortar2.py."""
import json, os, subprocess, sys, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legenda as L

VF = ("crop=1944:3456:108:340,scale=1080:1920:flags=lanczos,"
      "cas=strength=0.22,eq=contrast=1.03:saturation=1.02")
AF = ("highpass=f=85,deesser=i=0.35,"
      "acompressor=threshold=-20dB:ratio=3:attack=8:release=160")

def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        sys.stderr.write((p.stderr or "")[-2500:]); raise SystemExit("ffmpeg falhou")
    return p.stderr

def main(src, tr, destino, trechos):
    tmp = tempfile.mkdtemp(prefix="rem_")
    try:
        words = L.corrigir(json.load(open(tr, encoding="utf-8"))["words"])

        # 1) cada trecho vira um arquivo, com fade de 30ms pra nao estalar na emenda
        partes, palavras, off = [], [], 0.0
        for i, (a, b) in enumerate(trechos):
            d = b - a
            f = os.path.join(tmp, f"p{i}.mov")
            run(["ffmpeg", "-v", "error", "-ss", f"{a}", "-t", f"{d}", "-i", src,
                 "-vf", VF, "-af", f"afade=t=in:st=0:d=0.03,afade=t=out:st={d-0.03:.3f}:d=0.03",
                 "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                 "-pix_fmt", "yuv420p", "-r", "30",
                 "-c:a", "pcm_s16le", "-ar", "48000", "-y", f])
            partes.append(f)
            for w in L.recortar(words, a, b):
                palavras.append({"text": w["text"], "start": w["start"] + off,
                                 "end": w["end"] + off})
            off += d

        # 2) junta
        lista = os.path.join(tmp, "l.txt")
        open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
        junto = os.path.join(tmp, "junto.mov")
        run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", lista,
             "-c", "copy", "-y", junto])

        # 3) legenda, com os tempos ja na linha do tempo nova
        faixa = os.path.join(tmp, "faixa.mov")
        cues = L.montar(palavras)
        vazio = os.path.join(tmp, "vazio.png")
        from PIL import Image
        Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)).save(vazio)
        seq, t = [], 0.0
        for i, c in enumerate(cues):
            if c["ini"] > t + 0.02:
                seq.append((vazio, c["ini"] - t))
            png = os.path.join(tmp, f"c{i:04d}.png")
            L.desenhar(c["txt"], png)
            seq.append((png, max(0.1, c["fim"] - c["ini"])))
            t = c["fim"]
        if t < off:
            seq.append((vazio, off - t))
        lf = os.path.join(tmp, "lf.txt")
        with open(lf, "w") as f:
            for p_, d_ in seq:
                f.write(f"file '{p_}'\nduration {d_:.3f}\n")
            f.write(f"file '{seq[-1][0]}'\n")
        run(["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", lf,
             "-c:v", "qtrle", "-r", "30", "-y", faixa])

        # 4) mede e fecha
        out = run(["ffmpeg", "-v", "info", "-i", junto, "-af",
                   AF + ",loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
        b = out[out.rindex("{"):]
        m = json.loads(b[:b.index("}") + 1])
        af = (AF + f",loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:"
              f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
              f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:"
              "linear=true,aresample=48000")
        run(["ffmpeg", "-v", "error", "-i", junto, "-i", faixa,
             "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1[v]",
             "-map", "[v]", "-map", "0:a", "-af", af,
             "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
             "-crf", "21", "-maxrate", "4M", "-bufsize", "8M",
             "-pix_fmt", "yuv420p", "-r", "30",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
             "-movflags", "+faststart", "-y", destino])
        print(f"ok {os.path.basename(destino)}  {off:.1f}s  {len(trechos)} trechos  {len(cues)} legendas")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    src, tr, destino = sys.argv[1], sys.argv[2], sys.argv[3]
    trechos = [tuple(float(x) for x in t.split("-")) for t in sys.argv[4:]]
    main(src, tr, destino, trechos)
