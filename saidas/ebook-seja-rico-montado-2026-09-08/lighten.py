#!/usr/bin/env python3
"""Clareia os fundos escuros de um PDF de e-book (padrão editorial Gilberto Sena)
trocando os operadores de cor no content-stream. Preserva texto/fontes/tabelas.
Uso: lighten.py entrada.pdf saida.pdf
"""
import sys, re, pymupdf

# triplas de cor (como aparecem no stream) -> nova tripla
#   fundos escuros -> papel / caixa clara
#   textos claros sobre escuro -> tinta / cinza
SWAP = {
  ".0392 .0392 .0392": ".9569 .9451 .9176",   # #0A0A0A  (.preto: capa/divisórias)  -> papel
  ".0588 .0784 .098":  ".9294 .902 .8471",    # #0F1419  (.grafite: box.dark / th)   -> #EDE6D8
  ".9569 .9451 .9176": ".0902 .0902 .0902",   # #F4F1EA texto claro -> tinta
  ".8431 .8157 .7451": ".2 .2 .2",            # #D7D0BE -> cinza escuro
  ".7882 .7608 .6902": ".33 .3 .24",          # #C9C2B0 -> quase-tinta
  ".6627 .6353 .5686": ".4 .38 .33",          # #A9A291 -> cinza
  ".9804 .9725 .949":  ".9804 .9725 .949",    # #faf8f2 (.box claro) inalterado
}
# ordem importa: primeiro os fundos, senão a troca de texto pega o fundo já trocado.
ORDER = [".0392 .0392 .0392", ".0588 .0784 .098",
         ".9569 .9451 .9176", ".8431 .8157 .7451",
         ".7882 .7608 .6902", ".6627 .6353 .5686"]

DARK_BG = (".0392 .0392 .0392 rg", ".0588 .0784 .098 rg")

def recolor_stream(data: bytes):
    txt = data.decode("latin-1")
    if not any(b in txt for b in DARK_BG):
        return None
    # marca cada tripla-alvo com placeholder pra não recontaminar
    for i, src in enumerate(ORDER):
        for op in (" rg", " RG"):
            txt = txt.replace(src + op, f"\x00{i}\x00" + op)
    for i, src in enumerate(ORDER):
        dst = SWAP[src]
        txt = txt.replace(f"\x00{i}\x00", dst)
    return txt.encode("latin-1")

def main():
    inp, out = sys.argv[1], sys.argv[2]
    doc = pymupdf.open(inp)
    changed = 0
    for pg in doc:
        pg.clean_contents()
        xref = pg.get_contents()[0]
        data = doc.xref_stream(xref)
        new = recolor_stream(data)
        if new is not None:
            doc.update_stream(xref, new)
            changed += 1
    doc.save(out, garbage=4, deflate=True)
    print(f"{inp.split('/')[-1]}: {changed} páginas clareadas -> {out}")

if __name__ == "__main__":
    main()
