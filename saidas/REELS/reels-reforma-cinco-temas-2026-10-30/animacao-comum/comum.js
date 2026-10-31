// Ajudantes das animações. Cada anim.html define CENAS, DURACAO e desenhar(t),
// e chama iniciar(). desenhar(t) é pura: o mesmo t sempre dá o mesmo quadro.
const lim = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, a, b) => lim((t - a) / (b - a));
const saida = x => 1 - Math.pow(1 - x, 3);
const mola = x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI) / 3) + 1;
const $ = id => document.getElementById(id);
const virgula = n => n.toFixed(1).replace('.', ',');

// Mostra só a cena do instante t e devolve o tempo local dela.
function cena(id, t) {
  const [a, b] = window.CENAS[id];
  $(id).style.opacity = (t >= a && t < b) ? 1 : 0;
  return t - a;
}

// Entrada padrão: sobe e aparece.
function sobe(id, l, a, b, dist = 80) {
  const p = saida(prog(l, a, b));
  $(id).style.opacity = p;
  $(id).style.transform = `translateY(${(1 - p) * dist}px)`;
}

// Etiqueta que cai de cima.
function cai(id, l, a, b, dist = 220) {
  const p = prog(l, a, b);
  $(id).style.opacity = p > 0 ? 1 : 0;
  $(id).style.transform = `translateY(${-(1 - saida(p)) * dist}px)`;
}

// Carimbo: aparece grande e assenta.
function carimbo(id, l, a, ang = -4) {
  const p = prog(l, a, a + .3);
  $(id).style.opacity = p > 0 ? 1 : 0;
  $(id).style.transform = `rotate(${ang}deg) scale(${1.6 - .6 * saida(p)})`;
}

function iniciar() {
  window.render = window.desenhar;
  const q = new URLSearchParams(location.search);
  if (q.has('t')) window.desenhar(parseFloat(q.get('t')));
  else {
    const t0 = performance.now();
    (function loop() { window.desenhar(((performance.now() - t0) / 1000) % window.DURACAO); requestAnimationFrame(loop); })();
  }
}
