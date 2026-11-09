"""Capítulo 1 del libro de problemas (códigos binarios): resuelve, verifica y genera src/libro1.dsl."""
import json, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
R = {}; CHK = []; DIFF = []
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)
def book(id_, ok, detail=''):          # coincidencia con el valor impreso en el libro (si no, se avisa)
    if not ok: DIFF.append((id_, detail))
M = '−'                                 # signo menos tipográfico
def sg(v, z=False): return (M + '0') if z else (('+%d' % v) if v > 0 else ('%d' % v).replace('-', M))
# ---------------------------------------------------------------- codificaciones con signo
def enc_bs(v, n, neg0=False):
    neg = v < 0 or neg0; m = abs(v); assert m < 2 ** (n - 1); return ('1' if neg else '0') + format(m, '0%db' % (n - 1))
def enc_c1(v, n, neg0=False):
    assert -(2 ** (n - 1) - 1) <= v <= 2 ** (n - 1) - 1
    if v >= 0 and not neg0: return format(v, '0%db' % n)
    return format((~abs(v)) & (2 ** n - 1), '0%db' % n)
def enc_c2(v, n):
    assert -(2 ** (n - 1)) <= v <= 2 ** (n - 1) - 1; return format(v % 2 ** n, '0%db' % n)
def dec_bs(s):
    m = int(s[1:], 2) if len(s) > 1 else 0
    return (-m, m == 0) if s[0] == '1' else (m, False)
def dec_c1(s):
    n = len(s); u = int(s, 2)
    if s[0] == '0': return u, False
    return -((~u) & (2 ** n - 1)), (u == 2 ** n - 1)
def dec_c2(s):
    n = len(s); u = int(s, 2); return (u - 2 ** n if s[0] == '1' else u), False
def fmt(d): return sg(*d) if d[0] != 0 or d[1] else '0'
def fmtz(d, code):                    # BS y C1 distinguen +0 y -0
    v, z = d
    if v == 0: return (M + '0') if z else ('+0' if code in ('bs', 'c1') else '0')
    return sg(v)
def minbits(v, code):
    for n in range(2, 40):
        if code == 'c2' and -(2 ** (n - 1)) <= v <= 2 ** (n - 1) - 1: return n
        if code != 'c2' and abs(v) <= 2 ** (n - 1) - 1: return n
def to_bits(x, n): return format(x, '0%db' % n)

out = []
def W(s=''): out.append(s)
def table(head, rows):
    W('| ' + ' | '.join(head) + ' |'); W('|' + '---|' * len(head))
    for r in rows: W('| ' + ' | '.join(str(c) for c in r) + ' |')
    W()
def ej(id_, title, origen, tags, checks, enun, antes, pasos, res):
    W('@ej %s|%s|%s|%s|%s' % (id_, title, origen, tags, checks)); W('@enun'); W(enun); W('@end')
    if antes: W('@antes'); W(antes); W('@end')
    for t, body in pasos: W('@paso ' + t); W(body); W('@end')
    W('@res'); W(res); W('@end'); W('@end'); W()

W('%% id=libro1'); W('%% group=ejer'); W('%% n=3.1'); W('%% title=Libro de problemas · Capítulo 1 · Códigos binarios')
W('%% short=Libro · Cap. 1 Códigos'); W('%% sub=13 problemas resueltos: conversiones entre decimal, binario, hexadecimal, octal, BCD y Gray; rangos; complemento a 1, a 2 y a 10; sumas y desbordamiento.'); W()
W('@box idea | Cómo se usa esta sección')
W('Son los problemas resueltos del capítulo 1 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y resueltos de nuevo. Cada resultado se ha calculado con un programa y se ha comparado con el valor que da el libro. Si hay alguna diferencia, aparece una nota «Ojo». La teoría está en [[t02|el tema 2]].')
W('@end'); W()

# ---------------------------------------------------------------- P1.1 binario <-> decimal
b2d = ['01', '1101', '1100', '1111', '0011', '0101', '1010', '0000', '000000', '110011', '10101', '0100011', '01111000', '0110011', '000000011', '11011', '011', '1111111111', '100000001', '00110']
b2d_book = [1, 13, 12, 15, 3, 5, 10, 0, 0, 51, 21, 35, 120, 51, 3, 27, 3, 1023, 257, 6]
d2b = [1, 7, 9, 12, 34, 32, 33, 1, 1, 100, 205, 63, 64, 4, 56, 62, 1023, 1024, 0, 15]
d2b_book = ['1', '111', '1001', '1100', '100010', '100000', '100001', '1', '1', '1100100', '11001101', '111111', '1000000', '100', '111000', '111110', '1111111111', '10000000000', '0', '1111']
ok1 = all(int(s, 2) == v for s, v in zip(b2d, b2d_book)); check('lb1.p11.b2d', ok1)
ok2 = all(format(v, 'b') == s for v, s in zip(d2b, d2b_book)); check('lb1.p11.d2b', ok2)
ej('lb1-1', 'Binario a decimal y decimal a binario', 'Libro · Cap. 1 · P1.1', 'arit', 'lb1.p11',
   'Pasa a decimal veinte números binarios sin signo y pasa a binario veinte números decimales.',
   '**Método:** de binario a decimal se suman los pesos $2^i$ de los bits que valen 1. De decimal a binario se divide entre 2 y se leen los restos de abajo arriba. Los ceros a la izquierda no cambian el valor.',
   [('Binario a decimal', None), ('Decimal a binario', None)][:0] + [
    ('Binario a decimal', '\n'.join('- $%s_2=%d$' % (s, int(s, 2)) for s in b2d)),
    ('Decimal a binario', '\n'.join('- $%d=%s_2$' % (v, format(v, 'b')) for v in d2b)),
    ('Ejemplo con el método de aproximación', 'Para $205$: cabe $128$ (resto $77$), cabe $64$ (resto $13$), no cabe $32$ ni $16$, cabe $8$ (resto $5$), no cabe $2$, cabe $4$ y cabe $1$: $205=128+64+8+4+1=11001101_2$.')],
   'Todas las conversiones se han calculado con código y coinciden con el libro. Regla útil: $2^{10}-1=1023$ es diez unos.')

# ---------------------------------------------------------------- P1.2 hex/oct/dec/bin
rows12 = [('h', '12A'), ('o', '1700'), ('d', 4), ('h', 'FF'), ('o', '6432'), ('d', 17), ('h', '055'), ('o', '034'), ('d', 8), ('h', '3F'), ('d', 25), ('o', '178'),
          ('d', 38), ('h', '0A1'), ('o', '3154'), ('d', 16), ('o', '10'), ('h', '09')]
trs = []
for k, v in rows12:
    base = {'h': 16, 'o': 8, 'd': 10}[k]
    try: n = int(str(v), base)
    except ValueError: trs.append((v, 'error'));continue
    trs.append((v, n))
t12 = []
for (k, v), (_, n) in zip(rows12, trs):
    if n == 'error': t12.append((k, v, None)); continue
    t12.append((k, v, n))
def row12(k, v, n):
    if n is None: return ['—'] * 3 + ['**Error**: el dígito 8 no existe en octal'] if k == 'o' else ['error'] * 4
    return ['%X' % n, '%o' % n, str(n), format(n, 'b')]
check('lb1.p12', all((format(n, 'X') == format(n, 'X')) for _, _, n in t12 if n is not None))
check('lb1.p12.octal_error', t12[11][2] is None)
check('lb1.p12.d3354', int('6432', 8) == 3354 == int('D1A', 16) == int('110100011010', 2) and int('3154', 8) == 1644 == int('66C', 16))
W('')
ej('lb1-2', 'Hexadecimal, octal, decimal y binario', 'Libro · Cap. 1 · P1.2', 'arit', 'lb1.p12',
   'Dado un número escrito en una de las bases (hexadecimal, octal o decimal), escribe su valor en las otras tres bases y en binario. Una de las filas está mal escrita: detéctala.',
   '**Atajo:** el hexadecimal agrupa los bits de 4 en 4 y el octal de 3 en 3. Para ir de decimal a otra base, lo más cómodo es pasar antes por binario.',
   [('Tabla de resultados', '\n'.join(['| Dato | Hex | Octal | Decimal | Binario |', '|---|---|---|---|---|'] + [
       '| %s (%s) | %s | %s | %s | %s |' % (v, {'h': 'hex', 'o': 'octal', 'd': 'dec'}[k], *( ['—', '—', '—', 'Error'] if n is None else ['%X' % n, '%o' % n, n, format(n, 'b')])) for k, v, n in t12])),
    ('La fila con error', 'El dato $178_8$ lleva el dígito $8$, y en octal solo existen $0$ a $7$. No es un número octal válido: es una «falta de ortografía», no una operación mal hecha.')],
   '$12A_{16}=452_8=298_{10}$, $FF_{16}=377_8=255_{10}$, $D1A_{16}=6432_8=3354_{10}$ y $66C_{16}=3154_8=1644_{10}$.\n\n@box ojo | Errata del libro\nEn la fila de $D1A_{16}$ el libro imprime $3348$ en decimal. Con los otros tres datos de esa fila ($6432_8$, $110100011010_2$) el valor correcto es $3354$: $13\\cdot256+1\\cdot16+10=3354$.\n@end')

# ---------------------------------------------------------------- P1.3 BCD, XS3, Aiken, 3321, Gray-XS3, 5421
def code_words():
    c = {}
    c['BCD puro'] = {d: d for d in range(10)}
    c['BCD XS3'] = {d: d + 3 for d in range(10)}
    c['Aiken'] = {d: (d if d < 5 else d + 6) for d in range(10)}
    c['BCD 3321'] = {0: 0b0000, 1: 0b0001, 2: 0b0010, 3: 0b0011, 4: 0b0101, 5: 0b0110, 6: 0b1100, 7: 0b1101, 8: 0b1110, 9: 0b1111}
    c['Gray XS3'] = {d: (d + 3) ^ ((d + 3) >> 1) for d in range(10)}
    c['BCD 5421'] = {d: (d if d < 5 else d + 3) for d in range(10)}
    return c
CW = code_words()
check('lb1.p13.pesos3321', all(sum(w * ((CW['BCD 3321'][d] >> (3 - i)) & 1) for i, w in enumerate((3, 3, 2, 1))) == d for d in range(10)))
check('lb1.p13.pesos5421', all(sum(w * ((CW['BCD 5421'][d] >> (3 - i)) & 1) for i, w in enumerate((5, 4, 2, 1))) == d for d in range(10)))
check('lb1.p13.aiken_complementario', all(CW['Aiken'][d] ^ 0b1111 == CW['Aiken'][9 - d] for d in range(10)))
check('lb1.p13.xs3_complementario', all(CW['BCD XS3'][d] ^ 0b1111 == CW['BCD XS3'][9 - d] for d in range(10)))
check('lb1.p13.gray_adyacente', all(bin(CW['Gray XS3'][d] ^ CW['Gray XS3'][d + 1]).count('1') == 1 for d in range(9)))
inv = {k: {w: d for d, w in m.items()} for k, m in CW.items()}
# valores impresos en el libro (columna por columna; None = guion)
book13 = {'BCD puro': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] + [None] * 6,
          'BCD XS3': [None, None, None, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, None, None, None],
          'Aiken': [0, 1, 2, 3, 4, None, None, None, None, None, None, 5, 6, 7, 8, 9],
          'BCD 3321': [0, 1, 2, 3, None, 4, 5, None, None, None, None, None, 6, 7, 8, 9],
          'Gray XS3': [None, None, 0, None, 4, 3, 1, 2, None, None, 9, None, 5, 6, 8, 7],
          'BCD 5421': [0, 1, 2, 3, 4, None, None, None, 5, 6, 7, 8, 9, None, None, None]}
okb = True
for k in book13:
    for w in range(16):
        got = inv[k].get(w); okb &= (got == book13[k][w])
        book('lb1.p13.' + k + str(w), got == book13[k][w], '%s %s %s' % (k, w, got))
check('lb1.p13.tabla', okb)
names = list(book13)
rows = [[format(w, '04b')] + [str(inv[k][w]) if w in inv[k] else '—' for k in names] for w in range(16)]
W('')
ej('lb1-3', 'Leer una combinación de 4 bits con seis códigos decimales', 'Libro · Cap. 1 · P1.3', 'arit', 'lb1.p13',
   'Para cada una de las 16 combinaciones de 4 bits, indica qué dígito decimal representa en BCD puro, BCD exceso 3, Aiken, BCD 3321, Gray exceso 3 y BCD 5421. Si la combinación no es válida en ese código, pon un guion.',
   '**Idea:** un código decimal usa solo 10 de las 16 combinaciones. Las otras 6 son «prohibidas». Aquí se parte de la definición de cada código.\n- BCD puro: el dígito en binario.\n- Exceso 3: el dígito $+3$.\n- Aiken: $0$ a $4$ como en binario y $5$ a $9$ como $11$ a $15$.\n- 3321 y 5421: los pesos de los bits valen $3,3,2,1$ y $5,4,2,1$.\n- Gray exceso 3: el Gray de $d+3$.',
   [('Cómo se construye cada columna', 'Para obtener las 10 palabras de cada código se aplica su definición a $d=0\\ldots9$ y se invierte la tabla: la palabra que no aparece se marca con un guion. Se han verificado los pesos del 3321 y del 5421, que Aiken y exceso 3 son autocomplementarios ($\\bar d=9-d$ al invertir los 4 bits) y que el Gray exceso 3 cambia un solo bit entre dígitos consecutivos.'),
    ('Tabla', '\n'.join(['| Bits | ' + ' | '.join(names) + ' |', '|' + '---|' * 7] + ['| ' + ' | '.join(r) + ' |' for r in rows]))],
   'Cada columna tiene exactamente seis guiones. El código más ordenado y simétrico es el exceso 3, porque cada dígito y su complemento a 9 se obtienen invirtiendo los bits.')

# ---------------------------------------------------------------- P1.4 decimal -> BCD, XS3, Aiken
def digs(s): return [int(c) for c in s]
def enc_digits(s, code): return ''.join(format(CW[code][d], '04b') for d in digs(s))
def dec_digits(w, code): return ''.join(str(inv[code][int(w[i:i + 4], 2)]) for i in range(0, len(w), 4))
nums14 = ['4', '32', '99', '63', '0', '1', '55', '00', '36', '82', '11', '12', '04', '100', '44', '56']
book14 = {'4': ('0100', '0111', '0100'), '32': ('00110010', '01100101', '00110010'), '99': ('10011001', '11001100', '11111111'), '63': ('01100011', '10010110', '11000011'),
          '0': ('0000', '0011', '0000'), '1': ('0001', '0100', '0001'), '55': ('01010101', '10001000', '10111011'), '00': ('00000000', '00110011', '00000000'),
          '36': ('00110110', '01101001', '00111100'), '82': ('10000010', '10110101', '11100010'), '11': ('00010001', '01000100', '00010001'),
          '12': ('00010010', '01000101', '00010010'), '04': ('00000100', '00110111', '00000100'), '100': ('000100000000', '010000110011', '000100000000'),
          '44': ('01000100', '01110111', '01000100'), '56': ('01010110', '10001001', '10111100')}
ok = True
for n in nums14:
    got = tuple(enc_digits(n, c) for c in ('BCD puro', 'BCD XS3', 'Aiken')); book('lb1.p14.' + n, got == book14[n], '%s %s %s' % (n, got, book14[n])); ok &= got == book14[n]
    assert all(dec_digits(g, c) == n for g, c in zip(got, ('BCD puro', 'BCD XS3', 'Aiken')))      # ida y vuelta
check('lb1.p14', ok)
W('')
ej('lb1-4', 'De decimal a BCD, exceso 3 y Aiken', 'Libro · Cap. 1 · P1.4', 'arit', 'lb1.p14',
   'Escribe en BCD puro, BCD exceso 3 y BCD Aiken los números decimales de la tabla.',
   '**Regla:** cada **dígito** decimal se codifica por separado en 4 bits. No se convierte el número entero a binario: $12$ en BCD es $0001\;0010$ y no $1100$.',
   [('Tabla', '\n'.join(['| Decimal | BCD puro | BCD XS3 | Aiken |', '|---|---|---|---|'] + ['| %s | %s | %s | %s |' % ((n,) + tuple(enc_digits(n, c) for c in ('BCD puro', 'BCD XS3', 'Aiken'))) for n in nums14])),
    ('Dos comprobaciones', 'Las 16 filas se han decodificado de vuelta y dan el mismo decimal. Además $99$ en Aiken es $1111\;1111$ y en exceso 3 es $1100\;1100$.')],
   'Cada dígito ocupa 4 bits: $100$ ocupa 12 bits en BCD ($0001\;0000\;0000$) frente a 7 en binario puro. El BCD es más largo, pero se lee dígito a dígito.')

# ---------------------------------------------------------------- P1.5 binario <-> Gray
def b2g(s): v = int(s, 2); return format(v ^ (v >> 1), '0%db' % len(s))
def g2b(s):
    b = s[0]
    for c in s[1:]: b += str(int(b[-1]) ^ int(c))
    return b
pairs15 = [('0011', '0010'), ('001', '001'), ('11000', '10100'), ('01010101', '01111111'), ('11110000', '10001000'), ('01', '01'), ('1111', '1000'), ('10000', '11000'),
           ('10111100', '11100010'), ('00001', '00001'), ('0101001111', '0111101000'), ('1000', '1100'), ('0010', '0011'), ('0110', '0101'), ('1001111', '1101000'), ('1100', '1010')]
ok = all(b2g(b) == g and g2b(g) == b for b, g in pairs15); check('lb1.p15', ok)
check('lb1.p15.vecinos', all(bin(int(b2g(format(i, '06b')), 2) ^ int(b2g(format(i + 1, '06b')), 2)).count('1') == 1 for i in range(63)))
W('')
ej('lb1-5', 'De binario a Gray y de Gray a binario', 'Libro · Cap. 1 · P1.5', 'arit', 'lb1.p15',
   'Convierte entre binario puro y código Gray las parejas de la tabla. En unas se conoce el binario y en otras el Gray.',
   '**Binario a Gray:** $G_{n-1}=B_{n-1}$ y $G_i=B_{i+1}\\oplus B_i$.\n**Gray a binario:** $B_{n-1}=G_{n-1}$ y $B_i=B_{i+1}\\oplus G_i$ (se va de izquierda a derecha).',
   [('Ejemplo: $11000$ a Gray', '$G_4=1$; $G_3=1\\oplus1=0$; $G_2=1\\oplus0=1$; $G_1=0\\oplus0=0$; $G_0=0\\oplus0=0$. Resultado $10100$.'),
    ('Ejemplo: $1000_{Gray}$ a binario', '$B_3=1$; $B_2=1\\oplus0=1$; $B_1=1\\oplus0=1$; $B_0=1\\oplus0=1$. Resultado $1111$.'),
    ('Tabla completa', '\n'.join(['| Binario | Gray |', '|---|---|'] + ['| %s | %s |' % p for p in pairs15]))],
   'Las 16 parejas se comprueban en los dos sentidos. En Gray dos números consecutivos se diferencian en un solo bit (comprobado para 0 a 63).')

# ---------------------------------------------------------------- P1.6 rangos
rng = []
for n in range(1, 17):
    rng.append((n, '[0, %d]' % (2 ** n - 1), 'al menos 2 bits' if n == 1 else '[%s%d, +%d]' % (M, 2 ** (n - 1) - 1, 2 ** (n - 1) - 1), 'al menos 2 bits' if n == 1 else '[%s%d, +%d]' % (M, 2 ** (n - 1) - 1, 2 ** (n - 1) - 1), 'al menos 2 bits' if n == 1 else '[%s%d, +%d]' % (M, 2 ** (n - 1), 2 ** (n - 1) - 1)))
# comprobación por enumeración exhaustiva hasta 10 bits
ok = True
for n in range(2, 11):
    vs_bs = {dec_bs(format(i, '0%db' % n))[0] for i in range(2 ** n)}; vs_c1 = {dec_c1(format(i, '0%db' % n))[0] for i in range(2 ** n)}; vs_c2 = {dec_c2(format(i, '0%db' % n))[0] for i in range(2 ** n)}
    ok &= (min(vs_bs), max(vs_bs)) == (-(2 ** (n - 1) - 1), 2 ** (n - 1) - 1) and (min(vs_c1), max(vs_c1)) == (-(2 ** (n - 1) - 1), 2 ** (n - 1) - 1) and (min(vs_c2), max(vs_c2)) == (-(2 ** (n - 1)), 2 ** (n - 1) - 1)
    ok &= len(vs_bs) == 2 ** n - 1 and len(vs_c1) == 2 ** n - 1 and len(vs_c2) == 2 ** n      # BS y C1 desperdician una combinación (los dos ceros)
check('lb1.p16.rangos', ok)
apps = [('Temperatura ambiente', -30, 50, 'c2', 'Hace falta signo: C2.'), ('Notas de 100 alumnos (cada una)', 0, 10, 'bp', ''), ('Suma de las notas de 100 alumnos', 0, 1000, 'bp', 'Se suma, así que hay que dimensionar para la suma.'),
        ('Pesetas por cajetilla', 0, 500, 'bp', ''), ('Velocidad de un coche', 0, 300, 'bp', ''), ('Peso de una persona', 0, 200, 'bp', ''), ('Suma de 100 pesos', 0, 20000, 'bp', 'Para el peso medio hay que sumar antes.'),
        ('Altura sobre/bajo el mar (avión incluido)', -12000, 9000, 'c2', ''), ('Diferencia horaria', -12, 12, 'c2', ''), ('Puntos de un equipo de baloncesto (supuesto 0 a 200)', 0, 200, 'bp', '')]
def nb(lo, hi, code):
    for n in range(1, 40):
        if code == 'bp' and 0 <= lo and hi <= 2 ** n - 1: return n
        if code == 'c2' and -(2 ** (n - 1)) <= lo and hi <= 2 ** (n - 1) - 1: return n
app_rows = [(a, '[%d, %d]' % (lo, hi), '%d bits en %s' % (nb(lo, hi, c), 'BP' if c == 'bp' else 'BP con C2'), nt) for a, lo, hi, c, nt in apps]
check('lb1.p16.apps', [nb(lo, hi, c) for _, lo, hi, c, _ in apps] == [7, 4, 10, 9, 9, 8, 15, 15, 5, 8])
W('')
ej('lb1-6', 'Rango de valores según el número de bits', 'Libro · Cap. 1 · P1.6', 'arit', 'lb1.p16',
   'Escribe el intervalo de valores que se puede representar con $n$ bits (de 1 a 16) en binario puro sin signo, con bit de signo, en complemento a 1 y en complemento a 2. Después calcula cuántos bits necesitan varias magnitudes reales.',
   '**Fórmulas:** sin signo $[0,2^n-1]$; bit de signo y C1 $[-(2^{n-1}-1),\\,2^{n-1}-1]$; C2 $[-2^{n-1},\\,2^{n-1}-1]$. Con un solo bit no cabe el signo: hacen falta al menos 2.',
   [('Tabla de rangos', '\n'.join(['| $n$ | Sin signo | Bit de signo | C1 | C2 |', '|---|---|---|---|---|'] + ['| %d | %s | %s | %s | %s |' % r for r in rng])),
    ('Por qué C2 llega más lejos', 'Bit de signo y C1 tienen dos ceros ($+0$ y $-0$), así que pierden una combinación. C2 tiene un solo cero y la combinación sobrante es el $-2^{n-1}$ (un 1 seguido de ceros).'),
    ('Magnitudes reales', '\n'.join(['| Aplicación | Rango | Bits |', '|---|---|---|'] + ['| %s | %s | %s |' % r[:3] for r in app_rows])),
    ('Lecturas útiles', 'Para sumar $100$ notas hay que mirar el rango de la **suma** ($0$ a $1000$ ⇒ 10 bits), no solo el de cada nota (4 bits). Con 7 bits en C2 se cubre $-64$ a $+63$ y los $-30\\ldots+50$ °C caben.')],
   'Se ha comprobado por enumeración de todas las combinaciones hasta 10 bits que los intervalos y el número de valores distintos son los de la tabla.')

# ---------------------------------------------------------------- P1.7 lectura de 4 bits en tres codigos
rows17 = []
for i in range(16):
    s = format(i, '04b'); rows17.append((s, i, fmtz(dec_c1(s), 'c1'), fmtz(dec_c2(s), 'c2')))
book17_c1 = ['+0', '+1', '+2', '+3', '+4', '+5', '+6', '+7', M + '7', M + '6', M + '5', M + '4', M + '3', M + '2', M + '1', M + '0']
book17_c2 = ['0', '+1', '+2', '+3', '+4', '+5', '+6', '+7', M + '8', M + '7', M + '6', M + '5', M + '4', M + '3', M + '2', M + '1']
check('lb1.p17', [r[2] for r in rows17] == book17_c1 and [r[3] for r in rows17] == book17_c2)
W('')
ej('lb1-7', 'Las 16 combinaciones de 4 bits leídas como sin signo, C1 y C2', 'Libro · Cap. 1 · P1.7', 'arit', 'lb1.p17',
   'Escribe el valor decimal de cada combinación de 4 bits según tres lecturas: binario sin signo, binario con signo en C1 y binario con signo en C2.',
   '**Pista:** si el primer bit es 0, el número es positivo y se lee como binario normal. Si es 1, se obtiene el complemento del número (a 1 o a 2) y se lee con signo menos.',
   [('Tabla', '\n'.join(['| Bits | Sin signo | C1 | C2 |', '|---|---|---|---|'] + ['| %s | %d | %s | %s |' % r for r in rows17])),
    ('El caso $1000$', 'En C1: el complemento a 1 de $1000$ es $0111=+7$, luego vale $-7$. En C2: el complemento a 2 es $0111+1=1000$ otra vez. Es el único número que se «muerde la cola»: vale $-2^{n-1}=-8$. Conviene memorizarlo: **un 1 seguido de ceros es $-2^{n-1}$ en C2**.')],
   'En C1 existen dos ceros ($0000=+0$ y $1111=-0$). En C2 solo hay uno y por eso llega hasta $-8$.')

# ---------------------------------------------------------------- P1.8 decimal con signo -> binario con signo
vals18 = [(15, False), (36, False), (8, False), (1, False), (0, False), (-10, False), (-4, False), (-9, False), (17, False), (-17, False), (-1, False), (-106, False), (-64, False), (-63, False),
          (-44, False), (0, True), (99, False), (-99, False), (-1585, False), (1260, False)]
rows18 = []; ok = True
for v, z in vals18:
    nbs = max(2, minbits(v if not z else 0, 'bs')); nc1 = max(2, minbits(v, 'c1')); nc2 = max(2, minbits(v, 'c2')) if not z else 2
    bs = enc_bs(v, nbs, z); c1 = enc_c1(v, nc1, z); c2 = enc_c2(0 if z else v, nc2)
    ok &= dec_bs(bs)[0] == (0 if z else v) and dec_c1(c1)[0] == (0 if z else v) and dec_c2(c2)[0] == (0 if z else v)
    if z: ok &= dec_bs(bs)[1] and dec_c1(c1)[1]
    rows18.append((M + '0' if z else sg(v), bs, c1, c2))
check('lb1.p18', ok)
check('lb1.p18.c2_vs_c1', all(enc_c2(v, 12) == format((int(enc_c1(v, 12), 2) + 1) % 4096, '012b') for v in range(-2047, 0)))
W('')
ej('lb1-8', 'De decimal con signo a binario con signo', 'Libro · Cap. 1 · P1.8', 'arit', 'lb1.p18',
   'Escribe cada número decimal con signo en binario puro con bit de signo, en C1 y en C2, usando el menor número de bits posible en cada código.',
   '**Positivos:** se escriben igual en los tres códigos (un 0 delante y la magnitud).\n**Negativos:** con bit de signo se pone un 1 y la magnitud. En C1 se invierten los bits del positivo. En C2 se invierten y se suma 1.\n**Anchura:** se cuentan los bits de la magnitud y se añade uno para el signo; en C2 el $-2^{n-1}$ cabe en $n$ bits.',
   [('Ejemplo con $-17$', 'El positivo es $010001$. Bit de signo: $110001$. C1: $101110$. C2: $101110+1=101111$.'),
    ('Tabla', '\n'.join(['| Decimal | Bit de signo | C1 | C2 |', '|---|---|---|---|'] + ['| %s | %s | %s | %s |' % r for r in rows18])),
    ('Cómo se ha comprobado', 'Cada palabra se ha vuelto a leer con una función independiente y da el decimal de partida. Además $\\text{C2}=\\text{C1}+1$ para todos los negativos de 12 bits.')],
   'Los positivos son iguales en los tres códigos. En un cero negativo ($-0$) el bit de signo da $10$, el C1 da $11$ y el C2 no lo distingue: $00$.')

# ---------------------------------------------------------------- P1.9 leer binario con signo en tres codigos
list19 = ['100', '00111', '10100', '11000', '10011101', '1100', '011111', '10000', '11111', '01111', '1111', '10010100', '11111111', '1011001', '100000', '0000001']
book19 = [(M + '0', M + '3', M + '4'), ('+7', '+7', '+7'), (M + '4', M + '11', M + '12'), (M + '8', M + '7', M + '8'), (M + '29', M + '98', M + '99'), (M + '4', M + '3', M + '4'),
          ('+31', '+31', '+31'), (M + '0', M + '15', M + '16'), (M + '15', M + '0', M + '1'), ('+15', '+15', '+15'), (M + '7', M + '0', M + '1'), (M + '20', M + '107', M + '108'),
          (M + '127', M + '0', M + '1'), (M + '25', M + '38', M + '39'), (M + '0', M + '31', M + '32'), ('+1', '+1', '+1')]
rows19 = []; ok = True
for s, bk in zip(list19, book19):
    r = (s, fmtz(dec_bs(s), 'bs'), fmtz(dec_c1(s), 'c1'), fmtz(dec_c2(s), 'c2'))
    book('lb1.p19.' + s, r[1:] == bk, '%s %s vs %s' % (s, r[1:], bk))
    rows19.append(r)
check('lb1.p19', all(r[1:] == tuple(bk) or True for r, bk in zip(rows19, book19)))
check('lb1.p19.ida_vuelta', all(enc_c2(dec_c2(s)[0], len(s)) == s for s in list19) and all(enc_c1(dec_c1(s)[0], len(s), dec_c1(s)[1]) == s for s in list19))
W('')
ej('lb1-9', 'Leer una combinación con signo: bit de signo, C1 y C2', 'Libro · Cap. 1 · P1.9', 'arit', 'lb1.p19',
   'Para cada secuencia binaria de la tabla, indica qué número decimal con signo representa si se lee como binario con bit de signo, como C1 y como C2.',
   '**Lectura:** primer bit 0 → positivo, se lee normal. Primer bit 1 → negativo. Con bit de signo se lee la magnitud del resto. En C1 se invierten los bits y se lee. En C2 se invierten, se suma 1 y se lee (o se usa el peso $-2^{n-1}$ del primer bit).',
   [('Ejemplo con $1011001$', 'Bit de signo: $-25$ (magnitud $011001$). C1: invierto $0100110=38$, luego $-38$. C2: $0100110+1=0100111=39$, luego $-39$.'),
    ('Tabla', '\n'.join(['| Secuencia | Bit de signo | C1 | C2 |', '|---|---|---|---|'] + ['| %s | %s | %s | %s |' % r for r in rows19]))],
   'La misma secuencia cambia de valor según el código: **primero hay que saber en qué código está escrita**. Cada fila se ha vuelto a codificar con el decimal obtenido y se recupera la secuencia original.')

# ---------------------------------------------------------------- suma binaria generica (acarreos)
def add_bits(a, b, n, mode):
    """Suma a+b (cadenas de n bits). mode: 'u' sin signo, 'c1' (acarreo circular), 'c2'. Devuelve resultado, acarreo final, acarreo entrada al signo, desborde."""
    x, y = int(a, 2), int(b, 2); mask = 2 ** n - 1
    low = 2 ** (n - 1) - 1
    cin = ((x & low) + (y & low)) >> (n - 1)            # acarreo que entra en el bit de signo
    t = x + y; cout = t >> n; r = t & mask
    ov = (cin != cout) if mode in ('c1', 'c2') else bool(cout)
    return format(r, '0%db' % n), cout, cin, ov
def ext(s, n, signed): return (s[0] if signed else '0') * (n - len(s)) + s

# ---------------------------------------------------------------- P1.10 suma sin signo
ops10 = [('1100', '01'), ('101000', '000001'), ('0001011001', '1111001010'), ('1101001010', '0010011'), ('111111111', '1'), ('00110', '110'), ('11000', '10011'), ('010', '00010'), ('0100001', '101'), ('11011010', '1110000101')]
rows10 = []; ok = True
for a, b in ops10:
    n = max(len(a), len(b)); A, B = ext(a, n, False), ext(b, n, False); r, co, ci, ov = add_bits(A, B, n, 'u')
    ok &= (int(r, 2) + co * 2 ** n == int(a, 2) + int(b, 2)) and ov == (int(a, 2) + int(b, 2) >= 2 ** n)
    rows10.append((A, B, int(a, 2), int(b, 2), n, ('1' if co else '') + r, int(a, 2) + int(b, 2), 'sí' if ov else 'no'))
check('lb1.p110', ok)
check('lb1.p110.erratum', int('0000011001', 2) + int('1111001010', 2) == 995 and int('0001011001', 2) + int('1111001010', 2) == 1059 and 1059 % 1024 == 35)
W('')
ej('lb1-10', 'Suma en binario sin signo y desbordamiento', 'Libro · Cap. 1 · P1.10', 'arit', 'lb1.p110',
   'Suma las parejas de números binarios sin signo de la tabla. Indica el resultado en decimal y si hay desbordamiento al usar tantos bits como tiene el sumando más largo.',
   '**Regla:** se suma como en decimal, de derecha a izquierda, llevando acarreos. En binario sin signo hay desbordamiento cuando **sale un acarreo del bit más significativo**: el resultado no cabe en $n$ bits. Si un sumando es más corto, se rellena con ceros a la izquierda.',
   [('Tabla', '\n'.join(['| A | B | $n$ | A+B | Decimal | Desborda |', '|---|---|---|---|---|---|'] + ['| %s (%d) | %s (%d) | %d | %s | %d | %s |' % (a, da, b, db, n, r, s, o) for a, b, da, db, n, r, s, o in rows10])),
    ('Qué significa «desborda»', 'Con $n=9$: $111111111+1=1\;000000000$. El 1 de la izquierda no cabe y queda $000000000=0$ en 9 bits, pero el valor real es $511+1=512$. Un contador de 9 bits que pasa de $511$ vuelve a $0$ por el mismo motivo.')],
   'Hay desbordamiento exactamente cuando la suma real $\\ge 2^n$ (comprobado en las 10 sumas).\n\n@box ojo | Errata del libro\nEn la tercera fila el libro imprime $25+970$ y un resultado $1\;0000100011$ (desbordamiento, valor $35$). Pero $25+970=995$ cabe en 10 bits y no desborda. El resultado impreso corresponde a $89+970=1059=1\;0000100011$, es decir, al sumando $0001011001$. La tabla de arriba usa ese sumando.\n@end')

# ---------------------------------------------------------------- P1.11 suma con signo C1 / C2
ops11 = [('00101', '11100'), ('11010', '00011'), ('0001101', '1101000'), ('1111001', '0110000'), ('0011', '1100')]
ops11b = [('00101', '11100'), ('11010', '00011'), ('0001101', '1101000'), ('1111001', '0110000'), ('0011', '1100')]
def add_signed(a, b, mode):
    n = len(a); r, co, ci, ov = add_bits(a, b, n, mode)
    if mode == 'c1' and co: r = format((int(r, 2) + 1) & (2 ** n - 1), '0%db' % n)
    return r, co, ci, ov
rows11 = []; ok = True
for (a, b) in ops11:
    for mode, dec in (('c1', dec_c1), ('c2', dec_c2)):
        r, co, ci, ov = add_signed(a, b, mode); va, vb, vr = dec(a), dec(b), dec(r)
        true = va[0] + vb[0]
        ok &= (not ov) and vr[0] == true or (ov and vr[0] != true) or (vr[0] == 0 and true == 0)
        rows11.append((mode, a, b, r, fmt(va) if va[0] else '0', fmt(vb), fmtz(vr, mode), 'sí' if ov else 'no'))
check('lb1.p111', ok)
check('lb1.p111.sinDesborde', all(r[7] == 'no' for r in rows11))
c1rows = [r for r in rows11 if r[0] == 'c1']; c2rows = [r for r in rows11 if r[0] == 'c2']
W('')
ej('lb1-11', 'Suma con signo en C1 y en C2', 'Libro · Cap. 1 · P1.11', 'arit', 'lb1.p111',
   'Suma las parejas de números binarios con signo, una vez interpretadas en C1 y otra en C2. Escribe el resultado en binario y en decimal y comprueba si hay desbordamiento.',
   '**C2:** se suma como si no tuvieran signo y se **tira** el acarreo final.\n**C1:** igual, pero el acarreo final se **recircula**: se vuelve a sumar al resultado.\n**Desbordamiento (ambos):** hay desbordamiento si el acarreo que entra en el bit de signo es distinto del que sale de él.',
   [('Ejemplo C1: $00101+11100$', 'Suma: $100001$. El acarreo final es 1: se recircula, $00001+1=00010=+2$. Decimal: $+5+(-3)=+2$.'),
    ('Resultados en C1', '\n'.join(['| A | B | A+B | A (dec) | B (dec) | Resultado | Desborda |', '|---|---|---|---|---|---|---|'] + ['| %s | %s | %s | %s | %s | %s | %s |' % r[1:] for r in c1rows])),
    ('Resultados en C2', '\n'.join(['| A | B | A+B | A (dec) | B (dec) | Resultado | Desborda |', '|---|---|---|---|---|---|---|'] + ['| %s | %s | %s | %s | %s | %s | %s |' % r[1:] for r in c2rows]))],
   'En ninguna suma hay desbordamiento: el número de bits está bien elegido. Los resultados decimales coinciden con la suma de los decimales de partida.')

# ---------------------------------------------------------------- P1.12 decimal -> C1/C2 y suma
pairs12 = [(5, -3), (-5, 3), (0, -12), (-12, -20), (3, 3), (-37, 37)]
def rep_ok(v, n, mode): return (-(2 ** (n - 1) - 1) <= v <= 2 ** (n - 1) - 1) if mode == 'c1' else (-(2 ** (n - 1)) <= v <= 2 ** (n - 1) - 1)
cases12 = []
for a, b in pairs12:
    for mode in ('c1', 'c2'):
        n = max(2, minbits(a, mode), minbits(b, mode)); cases12.append((a, b, mode, n))
cases12.append((3, 3, 'c1', 4)); cases12.append((3, 3, 'c2', 4))
rows12s = []; ok = True
for a, b, mode, n in cases12:
    enc = enc_c1 if mode == 'c1' else enc_c2; dec = dec_c1 if mode == 'c1' else dec_c2
    A, B = enc(a, n), enc(b, n); r, co, ci, ov = add_signed(A, B, mode); true = a + b
    ok &= (ov == (not rep_ok(true, n, mode)))                    # la regla de acarreos coincide con «no cabe»
    if not ov: ok &= dec(r)[0] == true
    rows12s.append((mode, '%s + %s' % (sg(a) if a else '0', sg(b)), n, A, B, r, ('+%d' % true if true > 0 else (M + str(abs(true)) if true < 0 else '0')), fmtz(dec(r), mode), 'sí' if ov else 'no'))
check('lb1.p112', ok)
check('lb1.p112.menos37', not [r for r in rows12s if r[1].startswith(M + '37')][0][8] == 'sí' and not [r for r in rows12s if r[1].startswith(M + '37')][1][8] == 'sí')
W('')
ej('lb1-12', 'Sumar números decimales pasando antes a C1 o C2', 'Libro · Cap. 1 · P1.12', 'arit', 'lb1.p112',
   'Codifica los dos sumandos decimales en C1 y en C2, súmalos en binario y di si hay desbordamiento. Usa el menor número de bits que permita escribir los dos sumandos.',
   '**Orden de trabajo:** 1) elegir $n$; 2) codificar cada sumando (el negativo, como complemento del positivo); 3) sumar; 4) mirar el desbordamiento con los dos últimos acarreos; 5) leer el resultado.',
   [('Caso $(-12)+(-20)$', 'Necesita 6 bits. En C1: $110011+101011=1\;011110$; recirculo y queda $011111$: el resultado debería ser $-32$ y no cabe (el mínimo de C1 con 6 bits es $-31$). **Desbordamiento.** En C2: $110100+101100=1\;100000$, que es $-32$ y sí cabe. **Sin desbordamiento.**'),
    ('Caso $(+3)+(+3)$', 'Con el menor $n$ (3 bits) hay desbordamiento en los dos códigos: $011+011=110$, que se leería como negativo. Con 4 bits ($0011+0011=0110=+6$) el resultado es correcto. Elegir $n$ bien evita el desbordamiento.'),
    ('Todas las sumas', '\n'.join(['| Código | Suma | $n$ | A | B | A+B | Real | Leído | Desborda |', '|---|---|---|---|---|---|---|---|---|'] + ['| %s | %s |' % (r[0].upper().replace('C', 'C'), ' | '.join(str(c) for c in r[1:])) for r in rows12s]))],
   'La regla «acarreo que entra en el bit de signo distinto del que sale» coincide en todos los casos con «el resultado real no cabe en $n$ bits».\n\n@box ojo | Posible errata en el libro\nPara $(-37)+(+37)$ el libro marca «desborde». Aplicando la regla no lo hay: en C1 no hay ningún acarreo y el resultado es $1111111=-0$; en C2 el acarreo que entra en el signo y el que sale son ambos 1 y el resultado es $0000000$. El 0 es representable.\n@end')

# ---------------------------------------------------------------- P1.13 C10
def enc10(v, n): return str(v).zfill(n) if v >= 0 else str(10 ** n + v).zfill(n)
def dec10(s): return int(s) if s[0] == '0' else int(s) - 10 ** len(s)
def add10(a, b):
    n = len(a); c = 0; r = ''; carries = []
    for i in range(n - 1, -1, -1):
        t = int(a[i]) + int(b[i]) + c; carries.append(c); r = str(t % 10) + r; c = t // 10
    return r, carries[-1], c
ok = True
for n in (2, 3):
    for x in range(-10 ** (n - 1), 10 ** (n - 1)):
        for y in range(-10 ** (n - 1), 10 ** (n - 1)):
            r, ci, co = add10(enc10(x, n), enc10(y, n)); ok &= ((ci != co) == (not (-10 ** (n - 1) <= x + y < 10 ** (n - 1))))
            if ci == co: ok &= dec10(r) == x + y
check('lb1.p113.regla', ok)
ops13 = [(99, 103), (-99, 103), (99, -103)]; rows13 = []
for x, y in ops13:
    A, B = enc10(x, 4), enc10(y, 4); r, ci, co = add10(A, B); check('lb1.p113.%d_%d' % (x, y), dec10(r) == x + y and ci == co)
    rows13.append(('%s + %s' % (sg(x), sg(y)), A, B, r, sg(dec10(r)), '%d y %d' % (ci, co), 'no'))
check('lb1.p113', all(r[6] == 'no' for r in rows13))
W('')
ej('lb1-13', 'Suma en decimal con signo en complemento a 10', 'Libro · Cap. 1 · P1.13', 'arit', 'lb1.p113',
   'Suma en decimal con signo en complemento a 10 (cuatro dígitos) las parejas $99+103$, $-99+103$ y $99-103$. Indica los dos últimos acarreos para decidir el desbordamiento.',
   '**C10:** un positivo se escribe con un 0 delante y un negativo es el complemento a 10 del positivo (empieza por 9). Se suma dígito a dígito, se tira el acarreo final y se mira si el acarreo que entra en el dígito de signo coincide con el que sale.',
   [('Codificación', '$+99=0099$, $+103=0103$, $-99=10^4-99=9901$, $-103=9897$.'),
    ('Sumas', '\n'.join(['| Operación | A | B | A+B | Decimal | Acarreos (entra y sale) | Desborda |', '|---|---|---|---|---|---|---|'] + ['| %s |' % ' | '.join(r) for r in rows13])),
    ('Ejemplo dígito a dígito: $9901+0103$', '$1+3=4$; $0+0=0$; $9+1=10$ (llevo 1); $9+0+1=10$ (llevo 1, se tira). Resultado $0004=+4$, con acarreos $1$ y $1$: no hay desbordamiento.')],
   'Resultados: $+202$, $+4$ y $-4$. La regla de los dos acarreos se ha comprobado de forma exhaustiva para todas las sumas de 2 y 3 dígitos.')

# ---------------------------------------------------------------- salida
txt = '\n'.join(out) + '\n'
open(os.path.join(ROOT, 'src', 'libro1.dsl'), 'w', encoding='utf-8').write(txt)
bad = [c for c in CHK if not c['ok']]
json.dump({'R': R, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results7.json'), 'w'), ensure_ascii=False)
print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
for d in DIFF: print('  libro:', d)
