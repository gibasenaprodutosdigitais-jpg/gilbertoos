import re

ATRIB = re.compile(r'[—–]\s*(Gilberto Sena|Og Mandino|[A-Z][a-zà-ú]+ [A-Z][a-zà-ú]+)\s*$')

def corrige(t):
    """Troca o travessao de efeito pela pontuacao que um humano usaria.
    Mantem o travessao de atribuicao de citacao, que e uso legitimo."""
    def troca(m):
        antes, depois = m.group(1), m.group(2)
        # atribuicao de citacao: nao mexe
        if re.match(r'\s*(Gilberto|Og|[A-Z][a-zà-ú]+\s+[A-Z])', depois) and antes.rstrip().endswith('.'):
            return m.group(0)
        d = depois.lstrip()
        if not d:                      # travessao solto no fim do trecho
            return antes.rstrip()
        # vira ponto final: o classico "nao e X — e Y"
        if re.match(r'é\s', d):
            return antes.rstrip() + '. É ' + d[2:].lstrip()
        # vira virgula: continuacao da mesma frase
        if re.match(r'(e|mas|ou|nem|com|sem|so|só|que|porque|vira|nao|não)\s', d):
            return antes.rstrip() + ', ' + d
        # vira dois-pontos: abre uma lista
        if ',' in d[:46]:
            return antes.rstrip() + ': ' + d
        # o resto vira ponto final
        return antes.rstrip() + '. ' + d[0].upper() + d[1:]
    # primeiro o par aposto: "a — b — c" vira "a, b, c"
    t = re.sub(r'\s*[—–]\s*([^—–.!?]{3,60}?)\s*[—–]\s*', r', \1, ', t)
    return re.sub(r'(.{0,80}?)\s*[—–]\s*(.{0,80})', troca, t)

if __name__ == '__main__':
    testes = [
        'conhecimento não é luxo de terapia — é a bússola de quem empreende.',
        'redução de 30% de IBS e CBS — advocacia, contabilidade, administração',
        'Use o método SMART — e nunca esqueça do mais no final',
        'deixa de ser otimização — vira sobrevivência do negócio',
        'propriedade intelectual central — blinde isso antes de crescer',
        'construir um relacionamento. — Gilberto Sena',
        'quanto você precisa vender — em reais ou em unidades — só pra fechar',
    ]
    for t in testes:
        print('  ANTES :', t)
        print('  DEPOIS:', corrige(t)); print()
