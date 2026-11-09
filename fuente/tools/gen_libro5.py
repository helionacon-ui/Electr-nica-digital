# -*- coding: utf-8 -*-
"""Capítulo 5 del libro de problemas (bloques MSI): simula cada bloque, verifica y genera src/libro5.dsl."""
import json, os, itertools, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
CHK = []; DIFF = []; R = {}
def check(id_, ok, detail=''):
    CHK.append({'id': id_, 'ok': bool(ok), 'detail': detail})
    if not ok: print('FALLA', id_, detail)
def book(id_, ok, detail=''):
    if not ok: DIFF.append((id_, detail)); print('DIF', id_, detail)
out = []
def W(s=''): out.append(s)
def ej(id_, title, origen, tags, checks, enun, antes, pasos, res):
    W('@ej %s|%s|%s|%s|%s' % (id_, title, origen, tags, checks)); W('@enun'); W(enun); W('@end')
    if antes: W('@antes'); W(antes); W('@end')
    for t, body in pasos: W('@paso ' + t); W(body); W('@end')
    W('@res'); W(res); W('@end'); W('@end'); W()
def tab(head, rws):
    return '\n'.join(['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)] + ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rws])
def b(v, n): return format(v & ((1 << n) - 1), '0%db' % n)
def ojo(txt): return '\n\n@box ojo | Errata en el libro\n' + txt + '\n@end'

W('%% id=libro5'); W('%% group=ejer'); W('%% n=3.5'); W('%% title=Libro de problemas · Capítulo 5 · Bloques MSI')
W('%% short=Libro · Cap. 5 Bloques MSI'); W('%% sub=Veinte problemas con codificadores, decodificadores, multiplexores, comparadores y sumadores: cada bloque se simula y se comprueba con todas las entradas.'); W()
W('@box idea | Cómo se usa esta sección')
W('Son los problemas resueltos del capítulo 5 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Aquí no se diseña con puertas sino con **bloques funcionales**: sumadores, comparadores, multiplexores, codificadores y decodificadores BCD‑7 segmentos (teoría en [[t05|el tema 5]]). Cada bloque está programado como una función, el circuito entero se simula con **todas** las combinaciones de entrada y se compara con lo que debería hacer. Los esquemas no se copian: cada circuito se describe en texto, bloque a bloque. Si el libro tiene un fallo, aparece en un recuadro de errata.')
W('@end'); W()

# ---------------------------------------------------------------- bloques MSI
def fa(a, b_, c): s = a + b_ + c; return s & 1, s >> 1
def add4(a, b_, cin=0): s = (a & 15) + (b_ & 15) + cin; return s & 15, s >> 4          # sumador 4+4: (suma, Cout)
def comp(a, b_): return (a > b_, a == b_, a < b_)                                         # comparador: A>B, A=B, A<B
def mux(sel, *ins): return ins[sel]
def neg4(x): return (~x) & 15
def c2val(x, n=4): return x - (1 << n) if x >> (n - 1) & 1 else x

# ================================================================ 5.1 codificador 10:4 decimal-BCD XS3 sin prioridad
def enc_xs3(EI, E):          # E = lista [E9..E0]
    if not EI: return dict(EO=0, S=0, GS=0)
    S = 0
    for d in range(10):
        if E[9 - d]: S |= (d + 3)
    GS = int(any(E)); EO = int(not any(E))
    return dict(EO=EO, S=S, GS=GS)
rows51 = []
for d in range(9, -1, -1):
    E = [1 if (9 - i) == d else 0 for i in range(10)]
    rows51.append((1, E, enc_xs3(1, E)))
bk51 = {9: 12, 8: 11, 7: 10, 6: 9, 5: 8, 4: 7, 3: 6, 2: 5, 1: 4, 0: 3}
ok51 = all(r[2]['S'] == bk51[d] and r[2]['EO'] == 0 and r[2]['GS'] == 1 for (d, r) in zip(range(9, -1, -1), rows51))
check('lb5.p51.codigos', ok51)
idle = enc_xs3(1, [0] * 10); off = enc_xs3(0, [0] * 10)
check('lb5.p51.reposo', idle == dict(EO=1, S=0, GS=0) and off == dict(EO=0, S=0, GS=0))
def eq51(EI, E):             # ecuaciones del libro
    e = {i: E[9 - i] for i in range(10)}
    S3 = (e[9] | e[8] | e[7] | e[6] | e[5]) & EI
    S2 = (e[9] | e[4] | e[3] | e[2] | e[1]) & EI
    S1 = (e[8] | e[7] | e[4] | e[3] | e[0]) & EI
    S0 = (e[8] | e[6] | e[4] | e[2] | e[0]) & EI
    GS = int(any(E)) & EI
    EO = int(not any(E)) & EI
    return dict(EO=EO, S=S3 * 8 + S2 * 4 + S1 * 2 + S0, GS=GS)
ok51e = True
for EI in (0, 1):
    for E in [[1 if (9 - i) == d else 0 for i in range(10)] for d in range(10)] + [[0] * 10]:
        ok51e &= eq51(EI, E) == enc_xs3(EI, E)
check('lb5.p51.ecuaciones', ok51e)
dos = enc_xs3(1, [1, 0, 0, 0, 0, 0, 0, 0, 0, 1])      # E9 y E0 a la vez
check('lb5.p51.sin_prioridad', dos['S'] == (12 | 3) and dos['S'] not in range(3, 13))
check('lb5.p51', ok51 and ok51e)
tb51 = tab(['EI', 'Entrada activa', 'EO', 'S3S2S1S0', 'GS'],
           [[1, 'E%d' % d, 0, b(bk51[d], 4), 1] for d in range(9, -1, -1)] + [[1, 'ninguna', 1, '0000', 0], [0, '(cualquiera)', 0, '0000', 0]])
ej('lb5-1', 'Codificador decimal a BCD exceso 3 sin prioridad', 'Libro · Cap. 5 · P5.1', 'msi,codigos', 'lb5.p51',
   'Completa la tabla de un codificador de 10 líneas a 4 bits que entregue el dígito decimal en BCD exceso 3, con entrada de habilitación EI, salida de habilitación EO y señal GS de «hay alguna tecla». No tiene prioridad.',
   '**Dos ideas:** (1) *sin prioridad* significa que el diseño solo garantiza el resultado cuando **una** línea está activa; (2) el exceso 3 de un dígito $d$ es simplemente $d+3$ en binario: $0\\to0011$, $9\\to1100$.',
   [('Qué hace cada señal', '$EI$ habilita el bloque: si vale 0, todo queda en 0. $GS$ ($=1$) indica que hay alguna entrada activa. $EO$ vale 1 solo cuando el bloque está habilitado y **no** hay ninguna entrada activa: sirve para encadenar otro codificador detrás.'),
    ('Tabla', tb51),
    ('Ecuaciones', 'Cada bit de salida es un OR de las entradas cuyo código lo tiene a 1, todo AND con $EI$: $S_3=(E_9+E_8+E_7+E_6+E_5)\\,EI$, $S_2=(E_9+E_4+E_3+E_2+E_1)\\,EI$, $S_1=(E_8+E_7+E_4+E_3+E_0)\\,EI$, $S_0=(E_8+E_6+E_4+E_2+E_0)\\,EI$. Además $GS=(E_9+\\dots+E_0)\\,EI$ y $EO=\\overline{E_9}\\cdots\\overline{E_0}\\,EI$. El programa simula el bloque con las 11 combinaciones de una tecla (o ninguna) y con $EI=0$ y $EI=1$: las ecuaciones coinciden con la tabla.'),
    ('Qué pasa con dos teclas a la vez', 'Como los ORs mezclan los códigos, pulsar $E_9$ y $E_0$ da $1100\\,|\\,0011=1111$, que no es ningún dígito válido. Para evitarlo hace falta un codificador **con** prioridad.')],
   'La tabla anterior y las seis ecuaciones describen el bloque. Todas se han verificado por simulación.')

# ================================================================ 5.2 decodificador BCD-7 segmentos con entradas y salidas activas a nivel bajo
SEGN = 'abcdefg'
ON = {0: 'abcdef', 1: 'bc', 2: 'abdeg', 3: 'abcdg', 4: 'bcfg', 5: 'acdfg', 6: 'cdefg', 7: 'abc', 8: 'abcdefg'}        # 6 sin trazo superior
ALT = {6: ['acdefg', 'cdefg'], 9: ['abcfg', 'abcdfg']}
def seg_low(code):                                         # salidas activas a nivel bajo (0 = encendido)
    if code not in ON: return None
    return ''.join('0' if s in ON[code] else '1' for s in SEGN)
def dec7(LT, RBI, E, BIin=1):                              # E = (E3,E2,E1,E0) activas a nivel bajo; devuelve (RBO, segmentos)
    code = (~((E[0] << 3) | (E[1] << 2) | (E[2] << 1) | E[3])) & 15
    if BIin == 0: return 0, '1111111'
    if LT == 0: return 1, '0000000'
    if RBI == 0 and code == 0: return 0, '1111111'
    return 1, seg_low(code)
up = [((0, 0, 0, 0, 0, 0), 1, '0000000'), ((1, 1, 1, 1, 0, 0), 1, '0000110'), ((1, 1, 0, 1, 1, 1), 1, '0000000'),
      ((1, 0, 1, 0, 0, 0), 1, '0001111'), ((1, 1, 1, 1, 1, 1), 1, '0000001'), ((1, 0, 1, 1, 1, 1), 0, '1111111'),
      ((0, 1, 1, 1, 1, 1), 1, '0000000'), ((1, 1, 1, 0, 0, 1), 1, '1100000'), ((1, 1, 0, 0, 1, 1), 1, None), ((1, 0, 1, 1, 1, 0), 1, '1001111')]
okup = True; fila_invalida = None
for ins, rbo, seg in up:
    r, s = dec7(ins[0], ins[1], ins[2:])
    if seg is None: fila_invalida = (ins, s)
    else: okup &= (r == rbo and s == seg)
check('lb5.p52.mitad_superior', okup)
check('lb5.p52.fila_invalida', fila_invalida is not None and fila_invalida[1] is None)       # código 12: sin dígito
lo = [(('1', 'X', '1', '0', '0', '1'), 1, '1100000'), (('1', 'X', '1', '1', '0', '0'), 1, '0000110'), (('1', 'X', '1', '1', '1', '0'), 1, '1001111'),
      (('1', '1', '1', '1', '1', '1'), 1, '0000001'), (('1', '1', '1', '0', '1', '0'), 1, '0100100'), (('1', '1', '1', '0', '0', '0'), 1, '0001111')]
def in_pre(pat, rbo, seg, BIin=1):
    cnt = 0
    for v in itertools.product((0, 1), repeat=6):
        if all(p == 'X' or int(p) == x for p, x in zip(pat, v)):
            r, s = dec7(v[0], v[1], v[2:], BIin)
            if (r, s) != (rbo, seg): return False
    return True
oklo = all(in_pre(p, r, s) for p, r, s in lo)
check('lb5.p52.mitad_inferior', oklo)
# filas con dos respuestas posibles
alt1 = in_pre(('0', 'X', 'X', 'X', 'X', 'X'), 1, '0000000') and in_pre(('1', 'X', '0', '1', '1', '1'), 1, '0000000')
alt2 = in_pre(('1', '0', '1', '1', '1', '1'), 0, '1111111') and in_pre(('1', 'X', 'X', 'X', 'X', 'X'), 0, '1111111', BIin=0)
check('lb5.p52.dos_respuestas', alt1 and alt2)
# el patrón 0110110 (a, d, g) no es ningún dígito
patrones = {''.join('0' if sg in ss else '1' for sg in SEGN) for ss in list(ON.values()) + ALT[6] + ALT[9]}
check('lb5.p52.patron_adg', '0110110' not in patrones)
# inconsistencia del 6
six_a = '1100000'; six_b = '0100000'
check('lb5.p52.seis_dos_formas', dec7(1, 1, (1, 0, 0, 1))[1] == six_a and six_a != six_b)
book('lb5.p52.seis', False, 'el 6 aparece con y sin trazo superior')
check('lb5.p52', okup and oklo and alt1 and alt2)
tb52a = tab(['LT', 'RBI', 'E3', 'E2', 'E1', 'E0', 'RBO/BI', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'Qué se ve'],
            [[*i, r, *(list(s) if s else ['¿'] * 7), ({'0000000': 'todo encendido', '0000110': '3', '0001111': '7', '0000001': '0', '1111111': 'apagado', '1100000': '6 (sin trazo superior)', '1001111': '1', None: 'código no BCD'}[s])] for i, r, s in up])
ej('lb5-2', 'Decodificador BCD a 7 segmentos con LT, RBI y RBO', 'Libro · Cap. 5 · P5.2', 'msi,7seg,bcd', 'lb5.p52',
   'Completa la tabla de un decodificador BCD a 7 segmentos cuyas entradas y salidas son todas activas a nivel bajo. Tiene prueba de lámparas (LT), supresión de ceros a la izquierda (RBI) y una línea RBO/BI que es salida de supresión y a la vez entrada de borrado.',
   '**Pistas para leer la tabla.** «Activa a nivel bajo» significa que un 0 *activa*: una salida $\\bar a=0$ **enciende** el segmento $a$, y una entrada $\\bar E_3\\ldots\\bar E_0$ se lee invertida (el código $1100$ en las entradas es el dígito $0011=3$). La tabla se lee en dos direcciones: arriba, de entradas a salidas; abajo, al revés (dadas las salidas, ¿qué entradas las producen?).',
   [('Reglas del bloque', '1) Si $BI=0$ entra por la línea RBO/BI, todo se apaga y $RBO=0$. 2) Si $\\overline{LT}=0$, se encienden los siete segmentos (prueba de lámparas). 3) Si $\\overline{RBI}=0$ y el dígito es $0$, se apaga y $RBO=0$: así un 0 a la izquierda no se escribe y avisa al siguiente dígito. 4) En cualquier otro caso se dibuja el dígito y $RBO=1$.'),
    ('Parte superior (entradas → salidas)', tb52a + '\n\nLa fila del código $0011$ invertido (dígito 12) no es BCD: el programa confirma que el modelo no define ninguna salida y por eso se deja como «¿».'),
    ('Parte inferior (salidas → entradas)', 'Se busca qué entradas dan la salida pedida. El programa recorre las 64 combinaciones de $LT,RBI,E_3..E_0$ y comprueba que cada fila del libro es cierta **para todas las combinaciones que cubren sus «X»**. Casos con dos respuestas posibles: (a) salida «todo encendido» con $RBO=1$: $LT=0$ y lo demás indiferente, **o** $LT=1$ con el dígito 8 (entradas $0111$); (b) «todo apagado» con $RBO=0$: $LT=1,RBI=0$ y dígito 0, **o** $BI=0$ forzado desde fuera (cualquier entrada). Las filas de los dígitos 6, 3, 1, 0, 5 y 7 salen de las entradas $1001$, $1100$, $1110$, $1111$, $1010$ y $1000$ respectivamente.'),
    ('La fila «¿»', 'El patrón $a,d,g$ encendidos ($0110110$) no coincide con ningún dígito 0–9, ni siquiera con las variantes del 6 y del 9 con o sin trazo. Es el patrón que un fabricante da a un código **no BCD** (10–15); cuál es depende del integrado, así que el ejercicio solo pide reconocer que no hay dígito.')],
   'Las dos mitades de la tabla son coherentes con las cuatro reglas de arriba, salvo una excepción que anotamos.' + ojo('El dígito 6 aparece de dos formas: en la mitad superior y en la primera fila de la inferior sale **sin** el trazo superior ($\\bar a=1$, salidas $1100000$), pero en la penúltima fila del bloque inferior el mismo código $1001$ da **con** trazo superior ($0100000$). Un decodificador no puede dar dos salidas distintas para la misma entrada: una de las dos filas es una errata de copia. Aquí se ha tomado la versión sin trazo, que es la que aparece dos veces.'))

# ================================================================ 5.3 multiplicador 3x3 con ANDs y sumadores completos
def mult3(a, b_):
    A = [(a >> i) & 1 for i in range(3)]; B = [(b_ >> i) & 1 for i in range(3)]
    pp = [[A[i] & B[j] for j in range(3)] for i in range(3)]          # pp[i][j] = A_i B_j
    P = [0] * 6; P[0] = pp[0][0]
    s1, c1 = fa(pp[1][0], pp[0][1], 0); P[1] = s1
    s2, c2 = fa(pp[1][1], pp[0][2], c1)
    s3, c3 = fa(pp[1][2], 0, c2)
    t2, d2 = fa(pp[2][0], s2, 0); P[2] = t2
    t3, d3 = fa(pp[2][1], s3, d2); P[3] = t3
    t4, d4 = fa(pp[2][2], c3, d3); P[4] = t4; P[5] = d4
    return sum(P[i] << i for i in range(6))
ok53 = all(mult3(a, b_) == a * b_ for a in range(8) for b_ in range(8))
check('lb5.p53.64_productos', ok53)
filas53 = [(2, 6, 12), (7, 7, 49), (0, 0, 0), (6, 6, 36), (1, 2, 2)]
check('lb5.p53.tabla', all(mult3(a, b_) == p for a, b_, p in filas53))
check('lb5.p53', ok53)
ej('lb5-3', 'Qué hace una red de ANDs y sumadores completos', 'Libro · Cap. 5 · P5.3', 'msi,aritmetica', 'lb5.p53',
   'Un circuito tiene nueve puertas AND y seis sumadores completos conectados en dos filas. Rellena una tabla de funcionamiento con cinco pares de entradas $A_{2\\text{-}0}$, $B_{2\\text{-}0}$ y averigua qué operación realiza.',
   '**Cómo se analiza:** se pone un valor en cada entrada y se propaga hacia la salida bloque a bloque. Cada AND forma un producto parcial $A_iB_j$; cada sumador completo (FA) suma tres bits y deja un bit de suma y un acarreo.',
   [('Producto parcial por filas', 'Las tres ANDs de cada fila multiplican **un bit de $A$** por los tres de $B$. La fila de $A_0$ está sin desplazar, la de $A_1$ desplazada una posición y la de $A_2$ dos. Las dos filas de sumadores van acumulando esas tres filas columna a columna, y el acarreo de cada FA pasa al siguiente.'),
    ('Tabla', tab(['$A_{2\\text{-}0}$', '$B_{2\\text{-}0}$', '$P_{5\\text{-}0}$', 'decimal'], [[b(a, 3) + ' (%d)' % a, b(b_, 3) + ' (%d)' % b_, b(mult3(a, b_), 6), mult3(a, b_)] for a, b_, _ in filas53]) + '\n\nEjemplo $010\\times110$: $A_0=0$ da la fila $000$, $A_1=1$ da $110$ (desplazada), $A_2=0$ da $000$. Suma: $1100=12=2\\times6$.'),
    ('Qué operación es', 'Los resultados son $2\\cdot6=12$, $7\\cdot7=49$, $0$, $6\\cdot6=36$ y $1\\cdot2=2$: es un **multiplicador de $3\\times3$ bits**. El programa modela las nueve ANDs y los seis FA y comprueba que da $A\\times B$ en las 64 combinaciones de entrada.')],
   'El circuito es un multiplicador binario sin signo de $3\\times3$ bits con salida de 6 bits. Verificado con las 64 combinaciones.')

# ================================================================ 5.4 mostrar el mayor de dos dígitos decimales
def mostrar_mayor(a, b_):
    A, B = a, b_                                        # tras codificar 10:4
    gt, eq, lt = comp(A, B)
    S = mux(int(gt), B, A)
    BI = int(eq)
    return None if BI else S
ok54 = all(mostrar_mayor(a, b_) == (None if a == b_ else max(a, b_)) for a in range(10) for b_ in range(10))
check('lb5.p54', ok54)
ej('lb5-4', 'Mostrar el mayor de dos números decimales', 'Libro · Cap. 5 · P5.4', 'msi,7seg,comparador', 'lb5.p54',
   'Dos selectores giratorios dan los dígitos decimales $A$ y $B$. Un 7 segmentos debe mostrar solo el mayor; si son iguales no se ve nada. Diseña el circuito con bloques MSI.',
   '**Receta general:** *codificar → comparar → elegir → decodificar*. Cada selector entrega una línea de 10 (una por dígito), así que lo primero es pasarla a binario.',
   [('Codificar', 'Un codificador 10:4 por selector convierte «la línea $k$ activa» en el número $k$ en BCD (4 bits).'),
    ('Comparar', 'Un comparador de 4 bits da $A>B$ y $A=B$.'),
    ('Elegir', 'Un cuádruple multiplexor 2:1, mandado por $A>B$, deja pasar $A$ si $A>B=1$ y $B$ en caso contrario. Cuando son iguales da igual cuál pase, porque el display se borrará.'),
    ('Mostrar', 'La salida del multiplexor va a un decodificador BCD‑7 segmentos. La señal $A=B$ se conecta a su entrada de borrado $BI$: si $A=B$, el display queda apagado.'),
    ('Comprobación', 'El programa prueba los 100 pares $(A,B)$: muestra $\\max(A,B)$ en todos los casos con $A\\ne B$ y apagado en los 10 con $A=B$.')],
   'Coste: 2 codificadores 10:4, 1 comparador de 4 bits, 1 cuádruple mux 2:1 y 1 decodificador BCD‑7 segmentos con entrada de borrado. Verificado con los 100 pares.')

# ================================================================ 5.5 restar y mostrar solo si no es negativo
def restar_libro(a, b_):
    nb = neg4(b_)
    c2, _ = add4(nb, 1)                     # -B = NOT(B)+1 (4 bits)
    R_, _ = add4(a, c2)
    BI = (R_ >> 3) & 1
    return None if BI else R_
def restar_ok(a, b_):
    s, cout = add4(a, neg4(b_), 1)          # A + NOT(B) + 1 en un solo sumador
    return None if cout == 0 else s
esperado = lambda a, b_: (a - b_) if a >= b_ else None
malos = [(a, b_) for a in range(10) for b_ in range(10) if restar_libro(a, b_) != esperado(a, b_)]
check('lb5.p55.fallos_libro', sorted(malos) == [(0, 9), (8, 0), (9, 0), (9, 1)], str(malos))
check('lb5.p55.libro_bien_si_menor_8', all(restar_libro(a, b_) == esperado(a, b_) for a in range(10) for b_ in range(10) if -8 <= a - b_ <= 7))
check('lb5.p55.cout_corregido', all(restar_ok(a, b_) == esperado(a, b_) for a in range(10) for b_ in range(10)))
check('lb5.p55.cout_equivale_a_mayor_igual', all((add4(a, neg4(b_), 1)[1] == 1) == (a >= b_) for a in range(16) for b_ in range(16)))
check('lb5.p55', len(malos) == 4)
book('lb5.p55', False, 'falla con A-B = 8 o 9')
ej('lb5-5', 'Restar dos dígitos y mostrar solo si es positivo', 'Libro · Cap. 5 · P5.5', 'msi,aritmetica,7seg', 'lb5.p55',
   'Dos selectores dan los dígitos decimales $A$ y $B$. Un 7 segmentos debe mostrar $A-B$ solo si el resultado es positivo o cero; si es negativo, no debe mostrarse nada.',
   '**Restar en binario** es sumar el opuesto: $A-B=A+(-B)$, y en complemento a dos $-B=\\overline{B}+1$. Con 4 bits se pueden representar los números $-8\\ldots+7$.',
   [('Diseño del libro', '1) Un sumador 4+4 calcula $-B=\\overline{B}+1$ (cuatro inversores y la constante $0001$). 2) Otro sumador 4+4 hace $A+(-B)$ y da $R_3R_2R_1R_0$. 3) El resultado va al decodificador BCD‑7 segmentos, y el bit $R_3$ se lleva a su entrada de borrado: $R_3=1$ ⇒ «resta negativa» ⇒ display apagado. Hace falta un sumador 4+4 (no uno 1+1) porque el $+1$ puede generar acarreos entre bits.'),
    ('Qué comprueba el programa', 'Se simulan los 100 pares $(A,B)$ de dígitos y se compara con el resultado esperado (mostrar $A-B$ si $A\\ge B$, apagado si $A<B$). El diseño del libro acierta en 96 pares y **falla en cuatro**:'),
    ('Los cuatro pares que fallan', tab(['A', 'B', 'A−B', 'R3R2R1R0', 'Debería mostrar', 'Muestra'], [[a, b_, a - b_, b(add4(a, add4(neg4(b_), 1)[0])[0], 4), ('nada' if esperado(a, b_) is None else esperado(a, b_)), ('nada' if restar_libro(a, b_) is None else restar_libro(a, b_))] for a, b_ in sorted(malos)]) + '\n\nLa resta de dos dígitos va de $-9$ a $+9$, pero con 4 bits en complemento a dos solo caben $-8\\ldots+7$. Si la diferencia es **8 o 9** ($1000$ y $1001$, con $R_3=1$), el circuito la toma por negativa y **borra** un resultado que debía verse. Si la diferencia es $-9$ ($0-9$), el resultado se desborda a $+7$ ($0111$, $R_3=0$) y el circuito **muestra un 7** en lugar de apagarse.'),
    ('Diseño corregido', 'Se usa **un solo sumador 4+4** con $A$, $\\overline{B}$ y $C_{in}=1$. Su acarreo de salida $C_{out}$ vale 1 si y solo si $A\\ge B$ (comprobado para los 256 pares de 4 bits). Se conecta $\\overline{C_{out}}$ a $BI$. Las cuatro salidas $S_3S_2S_1S_0$ son directamente el resultado, hasta 9. El programa confirma que acierta en los 100 pares.')],
   'La estructura del libro sirve cuando $-8\\le A-B\\le7$, pero falla en $8-0$, $9-0$ y $9-1$ (borra) y en $0-9$ (muestra un 7).' + ojo('Con $R_3$ como indicador de signo falla en cuatro pares de dígitos: con diferencia 8 o 9 (tres pares) borra un resultado válido, y con $0-9$ el desbordamiento da $+7$ y lo muestra. La solución más simple es usar el acarreo de salida de un único sumador $A+\\overline{B}+1$ y negarlo hacia $BI$. El libro avisa de que no hay que comparar con $0000$ con un comparador, lo cual es cierto; pero tampoco basta con mirar el bit de signo.'))

# ================================================================ 5.6 mayor de tres números
def mayor3(a, b_, c):
    Rp = mux(int(comp(a, b_)[0]), b_, a)
    return mux(int(comp(Rp, c)[0]), c, Rp)
ok56 = all(mayor3(a, b_, c) == max(a, b_, c) for a in range(16) for b_ in range(16) for c in range(16))
check('lb5.p56', ok56)
ej('lb5-6', 'Mostrar el mayor de tres números', 'Libro · Cap. 5 · P5.6', 'msi,7seg,comparador', 'lb5.p56',
   'Tres selectores dan los dígitos decimales $A$, $B$ y $C$. Un 7 segmentos debe mostrar el mayor de los tres.',
   '**Torneo de eliminación:** el mayor de tres se obtiene en dos rondas, igual que en el problema de dos números.',
   [('Ronda 1', 'Un comparador $A>B$ gobierna un cuádruple mux 2:1 que da $R'+"'"+'$: si $A>B$, $R\'=A$; si no, $R\'=B$ (da igual cuál se tome cuando son iguales).'),
    ('Ronda 2', 'Otro comparador compara $R\'>C$ y manda otro cuádruple mux 2:1: si $R\'>C$ el resultado es $R=R\'$, si no, $R=C$.'),
    ('Mostrar', '$R$ entra en un decodificador BCD‑7 segmentos.'),
    ('Comprobación', 'Se simulan las $16^3=4096$ ternas de números de 4 bits (incluidos los empates) y el resultado es siempre el máximo. En los empates da igual qué rama se escoja porque el valor es el mismo.')],
   'Dos comparadores de 4 bits, dos cuádruples multiplexores 2:1 y un decodificador. Verificado con las 4096 ternas.')

# ================================================================ 5.7 los dos mayores de tres
SEL_L = {0: 'B', 1: 'B', 3: 'A', 4: 'A', 6: 'A', 7: 'A'}         # entradas de los multiplexores del libro (M1)
SEL_R = {0: 'C', 1: 'C', 3: 'B', 4: 'C', 6: 'C', 7: 'B'}         # (M2)
def dos_mayores(a, b_, c):
    x, y, z = int(a > b_), int(a > c), int(b_ > c)
    idx = 4 * x + 2 * y + z
    if idx not in SEL_L: return None
    v = {'A': a, 'B': b_, 'C': c}
    return v[SEL_L[idx]], v[SEL_R[idx]]
ok57 = True; ok57i = True
for a in range(16):
    for b_ in range(16):
        for c in range(16):
            r = dos_mayores(a, b_, c)
            if r is None: ok57i = False; continue
            top2 = sorted([a, b_, c])[1:]
            if sorted(r) != top2: ok57 = False
check('lb5.p57.dos_mayores', ok57)
check('lb5.p57.idx_2_y_5_imposibles', ok57i)
# ordenado: M1 el mayor, M2 el segundo
def ordenado(a, b_, c):
    x, y, z = int(a > b_), int(a > c), int(b_ > c)
    idx = 4 * x + 2 * y + z
    v = {'A': a, 'B': b_, 'C': c}
    TOP = {0: ('C', 'B'), 1: ('B', 'C'), 3: ('B', 'A'), 4: ('C', 'A'), 6: ('A', 'C'), 7: ('A', 'B')}
    p, q = TOP[idx]; return v[p], v[q]
ok57o = all(ordenado(a, b_, c) == tuple(sorted([a, b_, c], reverse=True)[:2]) for a in range(16) for b_ in range(16) for c in range(16))
check('lb5.p57.ordenado', ok57o)
check('lb5.p57', ok57 and ok57i and ok57o)
ej('lb5-7', 'Mostrar los dos mayores de tres números', 'Libro · Cap. 5 · P5.7', 'msi,7seg,comparador', 'lb5.p57',
   'Tres selectores dan los dígitos decimales $A$, $B$ y $C$. Dos 7 segmentos deben mostrar los dos mayores.',
   '**Idea:** tres comparaciones ($A>B$, $A>C$, $B>C$) determinan el orden completo de los tres números. Esas tres señales sirven de código de selección de dos multiplexores de 8 entradas.',
   [('Código de selección', 'Con $x=A>B$ (peso 4), $y=A>C$ (peso 2) y $z=B>C$ (peso 1) hay 8 combinaciones, pero **dos son imposibles**: $x=1,z=1,y=0$ ($A>B>C$ y $A\\le C$) y $x=0,z=0,y=1$. Corresponden a los índices 5 y 2, y se dejan sin conectar (N.C.).'),
    ('Entradas de los multiplexores', tab(['x y z', 'Orden', 'M1', 'M2'], [[format(i, '03b'), {0: '$A\\le B\\le C$', 1: '$A\\le C<B$', 3: '$C<A\\le B$', 4: '$B<A\\le C$', 6: '$A>C\\ge B$', 7: '$A>B>C$'}[i], SEL_L[i], SEL_R[i]] for i in (0, 1, 3, 4, 6, 7)]) + '\n\nEn cada fila M1 y M2 son los **dos mayores**, sin garantizar quién es el primero: por ejemplo en $x\\,y\\,z=001$ el mayor es $B$ y el segundo $C$, y el libro los saca por M1 y M2 en ese orden, mientras que en $011$ el mayor es $B$ y sale por M2.'),
    ('Comprobación', 'Con las $16^3=4096$ ternas el par $\\{M_1,M_2\\}$ coincide siempre con los dos mayores, **incluidos los empates**, y nunca se llega a los índices 2 y 5. El libro deja como ejercicio saber cuál es el mayor.'),
    ('Variante: M1 el mayor y M2 el segundo', 'Basta con cambiar las entradas de los multiplexores: M1: $0\\to C$, $1\\to B$, $3\\to B$, $4\\to C$, $6\\to A$, $7\\to A$; M2: $0\\to B$, $1\\to C$, $3\\to A$, $4\\to A$, $6\\to C$, $7\\to B$. El programa comprueba que así M1 es siempre el mayor y M2 el segundo en las 4096 ternas.')],
   'Tres comparadores y dos multiplexores 4×8:1 (cuádruples) más dos decodificadores. Todo comprobado, incluidos los empates.')

# ================================================================ 5.8 valor absoluto en complemento a dos
def abs_c2(a):
    n, _ = add4(neg4(a), 1)
    return mux((a >> 3) & 1, a, n)
ok58 = all(c2val(abs_c2(a)) == abs(c2val(a)) for a in range(16) if a != 8)
check('lb5.p58.todos_menos_menos8', ok58)
check('lb5.p58.menos8', abs_c2(8) == 8 and c2val(abs_c2(8)) == -8)
check('lb5.p58', ok58 and abs_c2(8) == 8)
ej('lb5-8', 'Valor absoluto de un número en complemento a dos', 'Libro · Cap. 5 · P5.8', 'msi,aritmetica,c2', 'lb5.p58',
   'Diseña un circuito que obtenga el valor absoluto de un número de cuatro bits en complemento a dos.',
   '**Idea:** el valor absoluto es $A$ si es positivo y $-A$ si es negativo. El signo está en el bit más significativo, $A_3$.',
   [('Calcular $-A$', 'Cuatro inversores y un sumador 4+4 con la constante $0001$ dan $\\overline{A}+1$.'),
    ('Elegir', 'Un cuádruple multiplexor 2:1, mandado por $A_3$, deja pasar $A$ si $A_3=0$ y $-A$ si $A_3=1$.'),
    ('Tabla de comprobación', tab(['A', 'valor', '|A| calculado', 'valor'], [[b(a, 4), c2val(a), b(abs_c2(a), 4), c2val(abs_c2(a))] for a in range(16)]) + '\n\nEl programa simula las 16 entradas: en 15 de ellas el resultado es correcto.')],
   'Un sumador 4+4, cuatro inversores y un cuádruple mux 2:1.' + ojo('Con 4 bits el número $1000$ ($-8$) no tiene opuesto representable: el circuito devuelve $1000$, que sigue valiendo $-8$ y no $+8$. Es el único caso en el que el valor absoluto no es correcto. El libro no lo menciona; se ha detectado simulando las 16 entradas.'))

# ================================================================ 5.9 nota final con redondeo
def nota(a, b_, c):
    s, cout = add4(a, b_)
    sfull = s | (cout << 4)
    defecto = sfull >> 1
    exceso = defecto + (sfull & 1)
    mini = mux(int(comp(a, b_)[2]), b_, a)
    maxi = mux(int(comp(a, b_)[0]), b_, a)
    return [defecto, mini, maxi, exceso][c]
ok59 = all(nota(a, b_, 0) == (a + b_) // 2 and nota(a, b_, 1) == min(a, b_) and nota(a, b_, 2) == max(a, b_) and nota(a, b_, 3) == (a + b_ + 1) // 2 for a in range(10) for b_ in range(10))
check('lb5.p59', ok59)
check('lb5.p59.ejemplos', [nota(3, 4, 0), nota(3, 4, 3), nota(3, 5, 0), nota(3, 5, 3), nota(8, 9, 0), nota(8, 9, 3)] == [3, 4, 4, 4, 8, 9])
ej('lb5-9', 'Nota final: media por defecto, por exceso, mínima o máxima', 'Libro · Cap. 5 · P5.9', 'msi,aritmetica,bcd,7seg', 'lb5.p59',
   'Se tienen dos notas $N_1$ y $N_0$ (cada una un dígito BCD). Con dos líneas de control $C_1C_0$ se elige la nota final: $00$ media redondeada por defecto, $01$ nota mínima, $10$ nota máxima, $11$ media redondeada por exceso. Muéstrala en un 7 segmentos.',
   '**Dividir entre 2 en binario** es desplazar un bit a la derecha: el bit que se pierde es el resto. Si el resto es 1, redondear por exceso es sumar 1.',
   [('Media por defecto', 'Un sumador 4+4 da $A+B=C_{out}S_3S_2S_1S_0$ (5 bits). Se descarta $S_0$: queda $C_{out}S_3S_2S_1$, el cociente de dividir entre 2.'),
    ('Media por exceso', 'Se suma $S_0$ al cociente anterior: con $S_0=0$ se suma 0 y con $S_0=1$ se suma 1. Así sale $\\lceil (A+B)/2\\rceil$. Un segundo sumador 4+4 hace esa suma.'),
    ('Mínimo y máximo', 'Un comparador de 4 bits y dos cuádruples mux 2:1 eligen el menor y el mayor.'),
    ('Elegir', 'Un cuádruple mux 4:1, mandado por $C_1C_0$, escoge entre las cuatro opciones (en el orden de la tabla del enunciado) y el decodificador BCD‑7 segmentos las muestra.'),
    ('Ejemplos', tab(['$N_1$', '$N_0$', 'suma', 'por defecto', 'por exceso'], [[a, b_, a + b_, nota(a, b_, 0), nota(a, b_, 3)] for a, b_ in ((3, 4), (3, 5), (8, 9))]) + '\n\nSe ha comprobado con las 100 parejas de dígitos que las cuatro opciones coinciden con $\\lfloor(a+b)/2\\rfloor$, $\\min$, $\\max$ y $\\lceil(a+b)/2\\rceil$.')],
   'Dos sumadores 4+4, un comparador de 4 bits, dos cuádruples mux 2:1 (mínimo y máximo) y un cuádruple mux 4:1. Verificado con las 100 parejas.')

# ================================================================ 5.10 sensor de temperatura entre -5 y +4
def ventana(t): return int(comp(t, 5)[2] or comp(t, 10)[0])
ok510 = all(ventana(t) == (1 if -5 <= c2val(t) <= 4 else 0) for t in range(16))
check('lb5.p510', ok510)
ej('lb5-10', 'Sensor de temperatura entre −5 °C y +4 °C', 'Libro · Cap. 5 · P5.10', 'msi,comparador,c2', 'lb5.p510',
   'Un sensor entrega la temperatura en 4 bits, en complemento a dos. La salida debe activarse cuando la temperatura esté entre $-5$ °C y $+4$ °C, ambos incluidos.',
   '**Truco:** los comparadores MSI comparan en binario puro, no en complemento a dos. Así que conviene mirar el intervalo como números **sin signo**.',
   [('Cómo se ven los valores', 'En 4 bits: $0000\\ldots0100$ son $0\\ldots+4$ y $1011\\ldots1111$ son $-5\\ldots-1$. Sin signo, los primeros son $0\\ldots4$ y los segundos $11\\ldots15$: dos tramos separados.'),
    ('Dos comparadores', 'Un comparador da $T<0101$ (menor que 5 ⇒ valores $0\\ldots4$, o sea $0\\ldots+4$ °C). Otro da $T>1010$ (mayor que 10 ⇒ $11\\ldots15$, o sea $-5\\ldots-1$ °C).'),
    ('Salida', 'Una puerta OR une las dos salidas: $Salida=(T<5)+(T>10)$. Se prueban los 16 valores y la salida vale 1 exactamente cuando $-5\\le T\\le4$.')],
   'Dos comparadores de 4 bits con constantes $0101$ y $1010$, y una OR. Verificado con los 16 códigos.')

# ================================================================ 5.11 expendedor de golosinas
PRECIO = {'G': 2, 'Ch': 3, 'R': 5, 'P': 6}
NEG = {'G': 0b1110, 'Ch': 0b1101, 'R': 0b1011, 'P': 0b1010}
def expendedor_libro(dinero, prod):
    Rr, _ = add4(dinero, NEG[prod])
    R3 = (Rr >> 3) & 1
    n, _ = add4(neg4(Rr), 1)
    S = mux(R3, Rr, n)
    return S, int(not R3), R3
def expendedor_ok(dinero, prod):
    Rr, cout = add4(dinero, NEG[prod])
    n, _ = add4(neg4(Rr), 1)
    S = mux(int(not cout), Rr, n)
    return S, cout, int(not cout)
def esperado11(dinero, prod):
    d = dinero - PRECIO[prod]
    return abs(d), int(d >= 0), int(d < 0)
malos11 = [(d, p) for d in range(16) for p in PRECIO if expendedor_libro(d, p) != esperado11(d, p)]
check('lb5.p511.corregido', all(expendedor_ok(d, p) == esperado11(d, p) for d in range(16) for p in PRECIO))
check('lb5.p511.libro_bien_si_sobra_menos_8', all(expendedor_libro(d, p) == esperado11(d, p) for d in range(16) for p in PRECIO if d - PRECIO[p] <= 7))
check('lb5.p511.fallos', all(d - PRECIO[p] >= 8 for d, p in malos11) and len(malos11) > 0, str(len(malos11)))
check('lb5.p511', len(malos11) > 0)
book('lb5.p511', False, '%d casos con sobra >= 8' % len(malos11))
ej('lb5-11', 'Expendedor de golosinas: dinero que falta o que sobra', 'Libro · Cap. 5 · P5.11', 'msi,aritmetica,7seg', 'lb5.p511',
   'Un expendedor recibe el dinero introducido (4 bits, en céntimos de euro, binario puro) y el producto pedido mediante cuatro microinterruptores G, Ch, R y P (gominolas, chicle, regaliz y pipas), que cuestan 2, 3, 5 y 6 céntimos. Un 7 segmentos muestra cuánto dinero falta o sobra, y dos leds indican si debe entregarse el producto (LP) o si el usuario debe completar el dinero (LD).',
   '**Idea:** la resta *dinero − precio* da la información que se pide. Si es $\\ge0$, el producto se entrega y la cifra es lo que sobra. Si es negativa, falta dinero y la cifra es su valor absoluto.',
   [('Elegir el precio', 'Un codificador 4:2 pasa la tecla pulsada a un código de 2 bits y un cuádruple multiplexor 4:1 saca **el precio ya negado** en complemento a dos: $-2=1110$, $-3=1101$, $-5=1011$, $-6=1010$.'),
    ('Restar', 'Un sumador 4+4 hace $D+(-\\text{precio})=R$.'),
    ('Valor absoluto de $R$', 'Cuatro inversores y otro sumador 4+4 dan $-R=\\overline{R}+1$. Un mux 2:1 gobernado por $R_3$ elige $R$ o $-R$.'),
    ('Salidas', 'El 7 segmentos muestra $S$. $LP=\\overline{R_3}$ (el producto sale si $R_3=0$) y $LD=R_3$ (el decodificador 1:2 de las dos señales es un simple inversor).'),
    ('Qué ocurre si sobra mucho', 'Se han simulado los 16 importes con los cuatro productos. El diseño del libro acierta siempre que la diferencia $D-\\text{precio}$ sea **como mucho 7**; falla cuando es 8 o más: ' + str(len(malos11)) + ' casos, p. ej. $D=15$ con gominolas ($15-2=13=1101$, que parece negativo porque $R_3=1$, y el circuito dice que falta dinero: $LD=1$ y muestra 3).'),
    ('Diseño corregido', 'Se usa el **acarreo** del primer sumador: $C_{out}=1$ exactamente cuando $D\\ge$ precio. Entonces $LP=C_{out}$, $LD=\\overline{C_{out}}$ y el mux elige $R$ si $C_{out}=1$ y $-R$ si no. El programa lo comprueba con los 64 casos.')],
   'El diseño del libro es correcto para sobras de hasta 7 céntimos; con el acarreo como señal de «llega el dinero» lo es en todo el rango.' + ojo('1) Con $R_3$ como indicador de signo falla cuando la diferencia es $\\ge8$ (por ejemplo, 15 céntimos para unas gominolas de 2). 2) En el texto la lista de códigos del producto (gominolas $00$, chicle $01$, regaliz $10$, pipas $11$) está invertida respecto al esquema, donde G entra por la línea 3 del codificador 4:2 y selecciona el precio $-2$. El esquema es el coherente.'))

# ================================================================ 5.12 votación en un consejo
def voto4(A, Bv, C, D, trampa):
    s1 = Bv + A; s2 = D + C                       # dos sumadores 1+1
    S, _ = add4(s1, s2)
    gt, eq, lt = comp(S, 2)
    V = mux(2 * int(gt) + int(eq), 0, A, 1, 0)      # 00->0, 01->A, 10->1
    return V ^ trampa
def voto4_ref(A, Bv, C, D, trampa):
    n = A + Bv + C + D
    v = 1 if n > 2 else (A if n == 2 else 0)
    return v ^ trampa
ok512a = all(voto4(*v, t) == voto4_ref(*v, t) for v in itertools.product((0, 1), repeat=4) for t in (0, 1))
check('lb5.p512.sol1', ok512a)
# segunda solución: multiplexor 16:1 con ceros y unos constantes
TAB16 = [voto4_ref(*bits_, 0) for bits_ in [(((i >> 3) & 1), ((i >> 2) & 1), ((i >> 1) & 1), i & 1) for i in range(16)]]
ok512b = all(TAB16[8 * A + 4 * Bv + 2 * C + D] == voto4_ref(A, Bv, C, D, 0) for A, Bv, C, D in itertools.product((0, 1), repeat=4))
check('lb5.p512.sol2', ok512b)
check('lb5.p512.empates_3_6_9_12', [i for i in range(16) if bin(i).count('1') == 2 and TAB16[i] == 1] == [9, 10, 12] and [i for i in range(16) if bin(i).count('1') == 2 and TAB16[i] == 0] == [3, 5, 6])
# seis países: A y B valen doble + veto
def addn(a, b_, cin, n):
    t = a + b_ + cin; return t & ((1 << n) - 1), t >> n
def voto6(A, Bv, C, D, E, F, trampa, veto):
    s2, c2 = addn(2 * A + C, 2 * Bv + D, E, 2)       # sumador 2+2: (A C) + (B D) + E
    s3 = s2 | (c2 << 2)
    t, c3 = addn(s3, 0, F, 3)                         # sumador 3+3: + "000" + F
    T = t | (c3 << 3)
    gt, eq, lt = comp(T, 4)
    V = mux(2 * int(gt) + int(eq), 0, A, 1, 0) ^ trampa
    return None if veto else V
def voto6_ref(A, Bv, C, D, E, F, trampa, veto):
    pesos = 2 * A + 2 * Bv + C + D + E + F
    v = 1 if pesos > 4 else (A if pesos == 4 else 0)
    return None if veto else v ^ trampa
ok512c = all(voto6(*x, t, vv) == voto6_ref(*x, t, vv) for x in itertools.product((0, 1), repeat=6) for t in (0, 1) for vv in (0, 1))
check('lb5.p512.sol3', ok512c)
check('lb5.p512', ok512a and ok512b and ok512c)
tb512 = tab(['A B C D', 'votos a favor', 'resultado (sin trampa)'], [[format(i, '04b'), bin(i).count('1'), TAB16[i]] for i in range(16)])
ej('lb5-12', 'Votación en un consejo con voto de calidad, trampa y veto', 'Libro · Cap. 5 · P5.12', 'msi,7seg,comparador,aritmetica', 'lb5.p512',
   'Cuatro países, A, B, C y D, votan en un consejo. Un 7 segmentos muestra el resultado de la votación. Si hay empate decide el voto de calidad de A. Además, el país anfitrión tiene un interruptor de trampa que da la vuelta al resultado. Después hay que rediseñar el circuito para seis países en los que los votos de A y B valen doble, y añadir el derecho de veto de un país.',
   '**Dos ideas:** (1) contar votos = **sumar bits**; (2) el resultado depende de si la suma es mayor, igual o menor que la mitad. Con cuatro votos, «mitad» es 2.',
   [('Primera solución: contar con sumadores y comparar', 'Dos sumadores 1+1 dan $S\'=A+B$ y $S\'\'=C+D$ (2 bits cada uno), y otro $S=S\'+S\'\'$ de 3 bits (0–4). Un comparador de 3 bits compara $S$ con $010$: $S>2$ ⇒ voto 1; $S=2$ ⇒ voto de $A$; $S<2$ ⇒ voto 0. Un multiplexor 4:1 gobernado por $(S>2,\\;S=2)$ elige entre $0$, $A$ y $1$ (la combinación «mayor y a la vez igual» es imposible y queda sin conectar). Para la trampa un mux 2:1 elige entre $V$ y $\\overline V$ según el interruptor. El resultado ($V_0$) y tres ceros forman el dígito BCD $000V_0$ que va al decodificador: muestra 0 o 1.'),
    ('Segunda solución: fuerza bruta', 'Un solo multiplexor 16:1 con $A,B,C,D$ como selección y constantes en las entradas. Las 16 posiciones se rellenan a mano, porque se sabe qué vale el resultado en cada caso:\n\n' + tb512 + '\n\nCon exactamente dos votos a favor, el resultado es el voto de $A$: es 1 en las posiciones 9, 10 y 12 ($A=1$) y 0 en la 3, 5 y 6. Las demás se rellenan por mayoría. Lo demás del circuito es igual (trampa y decodificador).'),
    ('Tercera solución: seis países, A y B valen doble', 'Los votos pesan $2A+2B+C+D+E+F$, con total 8; la mayoría es $>4$ y el empate es $=4$. Un sumador 2+2 suma los números de dos bits $AC$ y $BD$ (donde $A$ y $B$ ocupan el bit de peso 2, así valen doble) y $E$ entra por su acarreo de entrada. Su resultado de 3 bits se suma con $000$ y con $F$ como acarreo de entrada en un sumador 3+3. Así los pesos no se mezclan; no valdría un sumador 2+2 *sin* agrupar, porque dos países valdrían doble por la posición equivocada. La salida de 4 bits se compara con $0100$. Un mux 4:1 elige $0$, $A$ o $1$ y otro 2:1 la trampa. La línea de **veto** va a la entrada de borrado del decodificador: si algún país veta, la pantalla se apaga.'),
    ('Comprobación', 'Con las 16 combinaciones de 4 países y las dos posiciones de la trampa, las soluciones 1 y 2 dan lo mismo que una cuenta directa (empate para $A$). Con las 64 combinaciones de 6 países, las 2 de la trampa y las 2 del veto (256 casos) la solución de seis países coincide con $2A+2B+C+D+E+F$ comparado con 4.')],
   'Tres diseños verificados: dos sumadores 1+1 + sumador + comparador + mux (elegante), un mux 16:1 (fuerza bruta) y el rediseño de seis países con veto.')

# ================================================================ 5.13 votación por bloques
def v513_ref(A, B3):
    a = sum(A); bsum = sum(B3)
    return 1 if a > 2 else (1 if (a == 2 and bsum > 1) else 0)
def v513_s1(A, B3):                                # tres sumadores 1+1 para A, uno para B, 2 comparadores y mux 2:1
    a0, a1, a2, a3 = A
    sa_lo, c1 = fa(a0, a1, 0); sa_hi, c2 = fa(a2, a3, 0)          # 1+1 (sumas de 2 bits, 0-2)
    p = (c1 << 1) | sa_lo; q = (c2 << 1) | sa_hi
    SA, _ = add4(p, q)
    SB, _ = add4(B3[0] + B3[1], B3[2])
    gt2, eq2, _ = comp(SA, 2); gtB = comp(SB, 1)[0]
    return int(gt2) if not eq2 else int(gtB)
def v513_s2(A, B3):                                # sumadores 4+4
    a, _ = add4(A[0], A[1]); c, _ = add4(A[2], A[3])
    SA, _ = add4(a, c)
    SB, _ = add4(B3[0] + B3[1], B3[2])
    gt, eq, _ = comp(SA, 2)
    return int(gt) if not eq else int(comp(SB, 1)[0])
def v513_s3(A, B3):                                # SA2 + SA1 SA0 + SA1 /SA0 SB1
    SA = sum(A); SB = sum(B3)
    SA2, SA1, SA0 = (SA >> 2) & 1, (SA >> 1) & 1, SA & 1; SB1 = (SB >> 1) & 1
    return SA2 | (SA1 & SA0) | (SA1 & (1 - SA0) & SB1)
ok513 = all(f(A, B3) == v513_ref(A, B3) for f in (v513_s1, v513_s2, v513_s3) for A in itertools.product((0, 1), repeat=4) for B3 in itertools.product((0, 1), repeat=3))
check('lb5.p513', ok513)
ej('lb5-13', 'Votación por bloques: cuatro países en A y tres en B', 'Libro · Cap. 5 · P5.13', 'msi,7seg,comparador,aritmetica', 'lb5.p513',
   'En una votación los países se agrupan en dos bloques: cuatro en el bloque A y tres en el B. Un 7 segmentos muestra el resultado: si hay mayoría en A, ése es el resultado; si hay empate en A, decide el bloque B. Diseña el circuito.',
   '**Cómo se razona:** hay que saber **cuántos** votos a favor hay en A (0 a 4) y en B (0 a 3). La regla es: $a>2$ ⇒ 1; $a<2$ ⇒ 0; $a=2$ ⇒ el resultado lo da $B$, y gana el 1 si en $B$ hay al menos dos votos.',
   [('Primera solución', 'Cuatro sumadores 1+1 para el bloque A en dos capas (primero $A_3+A_2$ y $A_1+A_0$, luego se suman sus resultados de 2 bits columna a columna, $S_{A2..0}$) y un sumador 1+1 para B (suma 3 bits, uno por el acarreo de entrada, y da $S_{B1}S_{B0}$). Un comparador de 3 bits compara $S_A$ con $010$ ($A>2$ y $A=2$, la señal $C$). Un comparador de 2 bits compara $S_B$ con $01$ ($B>1$). Un mux 2:1 gobernado por $C$ elige entre $(A>2)$ si $C=0$ y $(B>1)$ si $C=1$. Se visualiza el resultado con $000V$ en el decodificador.'),
    ('Segunda solución', 'Muy parecida, pero con sumadores 4+4 en lugar de 1+1: se rellenan con ceros las entradas libres. Funciona igual y no mezcla pesos porque la suma se hace en dos niveles.'),
    ('Tercera solución: con puertas', 'Tres sumadores 1+1 para A (resultado $S_{A2}S_{A1}S_{A0}$) y uno para B ($S_{B1}S_{B0}$). El voto vale 1 si: $S_{A2}=1$ (cuatro votos), $S_{A1}S_{A0}=11$ (tres), o $S_{A1}S_{A0}=10$ (dos) y además $S_{B1}=1$. O sea $V=S_{A2}+S_{A1}S_{A0}+S_{A1}\\overline{S_{A0}}S_{B1}$: una AND y una OR detectan «3 ó 4», otra AND resuelve el caso de 2 con $B$. Se sustituyen los comparadores y el multiplexor por tres puertas.'),
    ('Comprobación', 'Las tres soluciones se han simulado con las $2^7=128$ combinaciones de votos y las tres coinciden con la regla $a>2$ ó $(a=2$ y $b\\ge2)$.')],
   'Las tres soluciones son equivalentes. La tercera es la más barata; las dos primeras son más fáciles de ampliar si cambia el número de países.')

# ================================================================ 5.14 reloj con alarma: cuatro displays y cuádruples multiplexores 4:1
ENT14 = {0: ['HD', 'HU', 'MD', 'MU'], 1: ['SD', 'SU', 'DD', 'DU'], 2: ['HAD', 'HAU', 'MAD', 'MAU'], 3: ['MD', 'MU', 'DD', 'DU']}
def displays(p1, p2, fuentes):                      # 4 multiplexores 4:1 de 4 bits, selección común P1P2
    return [mux(2 * p1 + p2, *[fuentes[ENT14[k][d]] for k in range(4)]) for d in range(4)]
nombres = sorted({n for v in ENT14.values() for n in v})
fuentes = {n: (3 * i + 1) % 10 for i, n in enumerate(nombres)}
ok514 = all(displays(p1, p2, fuentes) == [fuentes[n] for n in ENT14[2 * p1 + p2]] for p1 in (0, 1) for p2 in (0, 1))
check('lb5.p514', ok514)
check('lb5.p514.cuatro_displays', all(len(v) == 4 for v in ENT14.values()))
ej('lb5-14', 'Reloj con alarma: cuatro displays y cuatro vistas', 'Libro · Cap. 5 · P5.14', 'msi,7seg,multiplexor', 'lb5.p514',
   'Cuatro 7 segmentos deben mostrar, según dos señales de control $P_1$ y $P_2$, el mes, el día, la hora, los minutos, los segundos y las décimas de segundo del día en curso, y también la hora y los minutos de la alarma. Diseña el circuito.',
   '**Un multiplexor por display.** Cada display $SG_k$ necesita elegir su dígito entre cuatro fuentes, y la elección la hacen las mismas dos líneas $P_1P_2$ para los cuatro. Es el uso clásico de un **cuádruple multiplexor 4:1**: 4 bits de dato por entrada, 4 entradas.',
   [('Qué muestra cada combinación', tab(['$P_1P_2$', 'Se ve', '$SG_3$', '$SG_2$', '$SG_1$', '$SG_0$'], [['00', 'HH MM', *ENT14[0]], ['01', 'SS DD', *ENT14[1]], ['10', 'HH MM de alarma', *ENT14[2]], ['11', 'MM DD (mes y día)', *ENT14[3]]]) + '\n\nSiglas: HD/HU decenas/unidades de hora; MD/MU de minutos; SD/SU de segundos; HAD/HAU y MAD/MAU de hora y minutos de alarma; DD/DU de día.'),
    ('Estructura', 'Cuatro multiplexores 4:1 de 4 bits (uno por display), con $P_1P_2$ como selección común; la salida de cada uno va a un decodificador BCD‑7 segmentos. Total: 4 cuádruples mux 4:1 y 4 decodificadores.'),
    ('Comprobación', 'El programa recorre las cuatro combinaciones $P_1P_2$ y verifica que cada display recibe exactamente su fuente de la tabla.')],
   'Con esta estructura, para mostrar otra «vista» basta añadir una entrada a cada multiplexor.' + ojo('En el esquema las entradas 1 de los displays $SG_1$ y $SG_0$ (vista «segundos y décimas») se llaman DD y DU, igual que las del día (entrada 3). Como las décimas de segundo no son el día del mes, deben ser señales distintas, por ejemplo $\\text{dc}_D$ y $\\text{dc}_U$.'))

# ================================================================ 5.15 sumador/restador con C-1 o C-2
def sumres(a, b_, op, cod):
    bp = (b_ ^ (15 if op else 0))
    if (op, cod) == (0, 1): cin_fijo = 0
    elif (op, cod) == (1, 1): cin_fijo = 1
    else: cin_fijo = None                        # recircular Cout (C-1)
    if cin_fijo is not None:
        s, c = add4(a, bp, cin_fijo); return [s]
    pts = []
    for cin in (0, 1):                           # puntos fijos del bucle Cout -> Cin
        s, c = add4(a, bp, cin)
        if c == cin: pts.append(s)
    return pts
def c1val(x): return -(15 - x) if x >> 3 & 1 else x
ok515_c2 = True; ok515_c1 = True; doble = []
for a in range(16):
    for b_ in range(16):
        for op in (0, 1):
            # C-2
            v = c2val(a) + (-c2val(b_) if op else c2val(b_))
            if -8 <= v <= 7: ok515_c2 &= (c2val(sumres(a, b_, op, 1)[0]) == v)
            # C-1
            v1 = c1val(a) + (-c1val(b_) if op else c1val(b_))
            if -7 <= v1 <= 7:
                pts = sumres(a, b_, op, 0)
                ok515_c1 &= len(pts) >= 1 and all(c1val(p) == v1 for p in pts)
                if len(pts) == 2: doble.append((a, b_, op))
check('lb5.p515.c2', ok515_c2)
check('lb5.p515.c1', ok515_c1)
check('lb5.p515.punto_fijo_doble_solo_en_cero', all(c1val(sumres(a, b_, op, 0)[0]) == 0 for a, b_, op in doble) and len(doble) > 0)
check('lb5.p515', ok515_c2 and ok515_c1)
ej('lb5-15', 'Sumador/restador en C-1 o C-2', 'Libro · Cap. 5 · P5.15', 'msi,aritmetica,c2', 'lb5.p515',
   'Diseña un sumador/restador en binario puro con signo en complemento a uno o a dos. Dos líneas de control: $COD=0$ elige C-1 y $COD=1$ elige C-2; $OP=0$ suma y $OP=1$ resta.',
   '**Recordatorio:** restar es sumar el opuesto. El opuesto en C-1 es invertir todos los bits ($\\overline{B}$). En C-2 es invertir y sumar 1. La suma en C-1 necesita además el **acarreo circular**: el acarreo de salida se vuelve a sumar al bit menos significativo.',
   [('Negar $B$ si hay resta', 'Cuatro puertas XOR: $B\'=B\\oplus OP$. Si $OP=1$ invierten $B$; si $OP=0$ lo dejan igual.'),
    ('Sumar', 'Un sumador 4+4 hace $A+B\'+C_{in}$.'),
    ('Elegir $C_{in}$', 'Un mux 4:1 gobernado por $OP\\,COD$ da: $00$ (suma C-1) ⇒ $C_{in}=C_{out}$ (acarreo circular); $01$ (suma C-2) ⇒ $0$; $10$ (resta C-1) ⇒ $C_{out}$; $11$ (resta C-2) ⇒ $1$ (el $+1$ del complemento a dos).'),
    ('Comprobación', 'Para los 256 pares de operandos y las dos operaciones, el programa calcula el resultado de cada modo y lo compara con el valor aritmético: en C-2 sale bien siempre que el resultado esté en $-8\\ldots7$, y en C-1 siempre que esté en $-7\\ldots7$ (fuera de esos rangos hay desbordamiento y el circuito no lo detecta).')],
   'El circuito funciona. Un único sumador 4+4 más 4 XOR y un mux 4:1.' + ojo('En los modos C-1 el acarreo de salida alimenta la entrada de acarreo del mismo sumador, es decir, hay un **bucle combinacional**. Estable no siempre es único: cuando $A+B'+"'"+'=15$ ($1111$) hay dos soluciones consistentes ($1111$ con $C_{in}=0$ y $0000$ con $C_{in}=1$). Las dos son «cero» en C-1, así que el valor es correcto, pero el circuito físico puede quedarse en cualquiera. Un diseño sin bucle usa dos sumadores en cascada (el segundo suma el acarreo del primero).'))

# ================================================================ 5.16 comparadores para C-1, C-2 y signo-magnitud
def comp_signo(a, b_):                                   # entradas 4 bits; circuito del libro (A3,B3 gobiernan dos mux 4:1)
    gt, eq, lt = comp(a, b_)
    A3, B3 = (a >> 3) & 1, (b_ >> 3) & 1
    sel = 2 * A3 + B3
    GT = mux(sel, gt, 1, 0, gt)
    LT = mux(sel, lt, 0, 1, lt)
    return int(GT), int(eq), int(LT)
ok516_c2 = all(comp_signo(a, b_) == tuple(int(x) for x in comp(c2val(a), c2val(b_))) for a in range(16) for b_ in range(16))
check('lb5.p516.c2', ok516_c2)
exc_c1 = [(a, b_) for a in range(16) for b_ in range(16) if comp_signo(a, b_) != tuple(int(x) for x in comp(c1val(a), c1val(b_)))]
check('lb5.p516.c1_solo_ceros', sorted(exc_c1) == [(0, 15), (15, 0)], str(exc_c1))
def sm_a_c1(x): return (x & 8) | ((x & 7) ^ (7 if x & 8 else 0))
def smval(x): return -(x & 7) if x & 8 else x
def comp_sm(a, b_): return comp_signo(sm_a_c1(a), sm_a_c1(b_))
exc_sm = [(a, b_) for a in range(16) for b_ in range(16) if comp_sm(a, b_) != tuple(int(x) for x in comp(smval(a), smval(b_)))]
check('lb5.p516.sm_solo_ceros', sorted(exc_sm) == [(0, 8), (8, 0)], str(exc_sm))
check('lb5.p516', ok516_c2)
ej('lb5-16', 'Comparadores para C-1, C-2 y signo-magnitud con un comparador de 4 bits', 'Libro · Cap. 5 · P5.16', 'msi,comparador,c2', 'lb5.p516',
   'A partir de un comparador de cuatro bits, diseña tres comparadores: uno para binario puro con complemento a 1, otro para binario puro con complemento a 2 y otro para binario con bit de signo.',
   '**El problema:** el comparador MSI trata sus 4 bits como un número **sin signo**. Si ambos operandos tienen el mismo signo, el orden es el mismo con o sin signo; si los signos difieren, el positivo siempre gana.',
   [('C-1 y C-2: el mismo circuito', 'Se usan $A_3$ y $B_3$ para gobernar dos multiplexores 4:1, uno para $A>B$ y otro para $A<B$: con $A_3B_3=00$ (ambos positivos) y $11$ (ambos negativos) se deja pasar la salida del comparador, porque en ambos casos el orden sin signo coincide con el orden con signo (p. ej. $1100$ vs $1001$: sin signo $12>9$, con signo $-4>-7$). Con $A_3B_3=01$ ($A$ positivo, $B$ negativo): $A>B=1$ y $A<B=0$. Con $10$: $A>B=0$ y $A<B=1$. La salida $A=B$ pasa directa.'),
    ('Comparador con bit de signo', 'Antes del comparador se transcodifica cada operando a C-1 con cuatro XOR: si $A_3=1$ se invierte la magnitud $A_{2\\text{-}0}$ ($A\'=A_{2\\text{-}0}\\oplus A_3$) y si $A_3=0$ se deja igual. Después se usa el mismo circuito que antes. Ejemplo: $1100$ ($-4$ en signo y magnitud) y $1001$ ($-1$) se transcodifican a $1011$ y $1110$. Ambos son negativos, el comparador sin signo da $11<14$ y en efecto $-4<-1$.'),
    ('Comprobación', 'Con los 256 pares de números en C-2, el circuito da exactamente la comparación aritmética. Con C-1 y con signo-magnitud, coincide en todos salvo en dos pares ordenados: el cero con cero negativo (en C-1: $0000$ y $1111$; con signo: $0000$ y $1000$), donde el circuito dice que el positivo es mayor en lugar de «iguales».')],
   'Un comparador de 4 bits y dos multiplexores 4:1 sirven para C-1 y C-2; para signo-magnitud se añaden dos cuartetos de XOR.' + ojo('Con C-1 y con signo y magnitud hay **dos representaciones del cero** ($+0$ y $-0$). El circuito del libro las ordena ($+0>-0$) en vez de declararlas iguales; el libro no lo advierte. Si hace falta distinguirlo, hay que añadir una comprobación específica (por ejemplo, si los dos números son cero).'))

# ================================================================ 5.17 sumador XS3
def xs3(a, b_):
    s, c = add4(a, b_)
    return add4(s, 0b0011 if c else 0b1101)[0], c
ok517 = all(xs3(x + 3, y + 3) == ((x + y) % 10 + 3, int(x + y >= 10)) for x in range(10) for y in range(10))
check('lb5.p517', ok517)
check('lb5.p517.ejemplos', xs3(0b0011, 0b0011) == (0b0011, 0) and xs3(0b0110, 0b1010) == (0b0011, 1) and xs3(0b1100, 0b1100) == (0b1011, 1))
def bcd_add(a, b_):
    s, c = add4(a, b_)
    corr = c | ((s >> 3) & (s >> 2) & 1) | ((s >> 3) & (s >> 1) & 1)
    r, c2 = add4(s, 0b0110 if corr else 0)
    return r, corr
check('lb5.p517.bcd', all(bcd_add(x, y) == ((x + y) % 10, int(x + y >= 10)) for x in range(10) for y in range(10)))
ej('lb5-17', 'Sumador BCD exceso 3 con sumadores binarios', 'Libro · Cap. 5 · P5.17', 'msi,aritmetica,bcd', 'lb5.p517',
   'Diseña un sumador de un dígito en BCD exceso 3 utilizando sumadores 4+4 en binario puro. Compruébalo con al menos tres ejemplos. ¿Es más sencillo un sumador BCD natural o uno en exceso 3? ¿Por qué?',
   '**Exceso 3:** el dígito $d$ se guarda como $d+3$. Al sumar dos dígitos se suman dos «+3», así que el resultado queda con un **exceso 6**. Hay que corregirlo para dejarlo con exceso 3 y, si la suma pasa de 9, pasar a la siguiente cifra.',
   [('Diseño', '1) Un sumador 4+4 calcula $S\'=A+B$. 2) Si $C\'_{out}=0$ no hubo acarreo del dígito ($S\'$ sigue en exceso 6 y la suma decimal es $\\le9$): hay que restar 3, es decir, sumar $1101$. 3) Si $C\'_{out}=1$ la suma decimal es $\\ge10$, se genera acarreo y el resultado debe quedar en exceso 3: se suma $0011$. 4) La constante se obtiene con un inversor y un 1: $B_3=B_2=\\overline{C\'_{out}}$, $B_1=C\'_{out}$, $B_0=1$. 5) Un segundo sumador 4+4 hace $S=S\'+\\text{constante}$. El acarreo de salida es $C\'_{out}$.'),
    ('Tres ejemplos', tab(['$A$', '$B$', '$S\'=A+B$', '$C\'$', 'se suma', '$S$', 'resultado'], [['0011 (0)', '0011 (0)', '0110', 0, '1101', '0011', '0, acarreo 0'], ['0110 (3)', '1010 (7)', '0000', 1, '0011', '0011', '0, acarreo 1 (10)'], ['1100 (9)', '1100 (9)', '1000', 1, '0011', '1011', '8, acarreo 1 (18)']]) + '\n\nEl programa comprueba los 100 pares de dígitos.'),
    ('¿Cuál es más sencillo?', 'El de **exceso 3**: solo necesita un inversor para generar la constante. El BCD natural necesita detectar «suma $>9$ o acarreo» ($C\'_{out}+S_3S_2+S_3S_1$, es decir, 2 AND y 1 OR de tres entradas) y además hacer la corrección $+0110$. La razón es que el exceso de 6 de la primera suma coincide con los 6 códigos que sobran en 4 bits: el acarreo binario es directamente el acarreo decimal y no hace falta detectar «>9». El programa simula ambos sumadores con los 100 pares.')],
   'Dos sumadores 4+4 y un inversor. El BCD natural cuesta además 2 AND y una OR de tres entradas.')

# ================================================================ 5.18 binario de 5 bits a dos dígitos BCD
def bin5_a_bcd(a):
    a40 = a & 15; a4 = (a >> 4) & 1
    corr = ((a40 >> 3) & (a40 >> 2) & 1) | ((a40 >> 3) & (a40 >> 1) & 1)
    s1, c1 = add4(a40, 0b0110 if corr else 0)
    r, cor = bcd_add(s1, 0b0110 if a4 else 0)
    RD = a4 + c1 + cor
    return RD, r
ok518 = all(bin5_a_bcd(a) == (a // 10, a % 10) for a in range(32))
check('lb5.p518', ok518)
check('lb5.p518.ejemplos', bin5_a_bcd(7) == (0, 7) and bin5_a_bcd(12) == (1, 2) and bin5_a_bcd(31) == (3, 1))
ej('lb5-18', 'Binario de 5 bits a dos dígitos BCD', 'Libro · Cap. 5 · P5.18', 'msi,aritmetica,bcd', 'lb5.p518',
   'Diseña un circuito que pase un número de cinco bits en binario puro a dos dígitos BCD.',
   '**Dividir entre 10:** un número entre 0 y 31 tiene como máximo 3 decenas. Cada vez que se pasa de 9 hay que «llevar» una decena, y como un dígito BCD usa 4 bits (16 combinaciones) para 10 valores, hay que sumar **6** para saltarse los códigos sobrantes.',
   [('Paso 1: los cuatro bits bajos', 'Se detecta si $A_{3\\text{-}0}\\ge10$ con $A_3A_2+A_3A_1$ (2 AND y una OR). Si es así se suma $0110$ con un sumador 4+4: $S\'=A_{3\\text{-}0}+(0\\text{ ó }6)$; el acarreo $C_{out}S\'$ vale 1 exactamente en ese caso (es la decena que hay que llevar).'),
    ('Paso 2: el bit de peso 16', 'El bit $A_4$ vale 16, que es «1 decena y 6 unidades». Se le suma 6 al dígito de unidades: $RU=S\'+(0\\text{ ó }6)$ con $A_4$ como control. Esto debe hacerse con un **sumador BCD**, porque la suma puede pasar de 9 (por ejemplo $5+6=11$ ⇒ unidad 1 y acarreo 1).'),
    ('Paso 3: decenas', '$RD_{1\\text{-}0}=A_4+C_{out}S\'+C_{out}RU$ con un sumador 1+1 (valores 0 a 3).'),
    ('Ejemplos', tab(['$A_{4\\text{-}0}$', '$S\'$', '$RU$', '$RD$'], [['00111 (7)', '0111', '0111 (7)', '0'], ['01100 (12)', '1100+0110 = 0010', '0010 (2)', '0+1+0 = 1'], ['11111 (31)', '1111+0110 = 0101', '0101+0110 = 0001 (1)', '1+1+1 = 3']]) + '\n\nSe han simulado las 32 entradas y siempre sale el cociente y el resto de dividir entre 10.')],
   'Dos sumadores 4+4 (el segundo en BCD), un sumador 1+1 y una detección con 2 AND y 1 OR. Verificado con los 32 valores.' + ojo('En el texto el criterio de corrección se enuncia como «$A_{3\\text{-}0}$ mayor que 10», pero el circuito (que usa $A_3A_2+A_3A_1$) detecta $\\ge10$, que es lo correcto: el valor 10 también necesita corrección.'))

# ================================================================ 5.19 dos puertas con claves
def puertas(p1, p2):
    A1 = comp(5, p1)[0]                                    # lo que dibuja el libro: A = "0101", B = Clave P1, salida A>B
    A1_ok = comp(p1, 5)[0]                                 # lo que pide el enunciado (P1 >= 6)
    P = p1 >> 1
    pm3, _ = add4(P, 3); pr3, _ = add4(P, 13)
    ab2 = comp(p2, pm3)[1] | comp(p2, pm3)[2]
    ab3 = comp(p2, pr3)[0] | comp(p2, pr3)[1]
    return int(A1), int(A1_ok), int(ab2 and ab3)
ok519 = all(puertas(p1, p2)[1] == int(p1 >= 6) for p1 in range(10) for p2 in range(10)) and \
        all(puertas(p1, p2)[2] == (1 if abs(p2 - p1 // 2) <= 3 else 0) for p1 in range(6, 10) for p2 in range(16))
check('lb5.p519.corregido', ok519)
check('lb5.p519.libro_dibujado_al_reves', all(puertas(p1, 0)[0] == int(p1 < 5) for p1 in range(10)))
check('lb5.p519', ok519)
book('lb5.p519', False, 'comparador de P1 con las entradas A/B cambiadas')
ej('lb5-19', 'Recinto con dos puertas y claves ligadas', 'Libro · Cap. 5 · P5.19', 'msi,comparador,aritmetica', 'lb5.p519',
   'Para entrar en un recinto hay que pasar dos puertas, P1 y P2. En la P1 se introduce un dígito BCD mayor o igual que 6. En la P2, un número que esté a no más de tres unidades de la mitad del introducido en la P1 (si se introduce 8, hay que meter un número entre 1 —que es 4−3— y 7 —que es 4+3—). Diseña el circuito.',
   '**Dos condiciones independientes:** abrir P1 (un comparador) y abrir P2 (un intervalo, que son dos comparaciones). La puerta se abre si se cumplen las dos.',
   [('Puerta 1', 'Se necesita $P_1\\ge6$, es decir, $P_1>5$: un comparador de 4 bits con la constante $0101$.'),
    ('Puerta 2: dividir entre 2', 'Dividir entre 2 en binario puro es quitar el bit de menos peso: $P=P_{1\\,3\\text{-}1}$ (3 bits).'),
    ('Puerta 2: los dos extremos', 'Un sumador 4+4 calcula $P+3$ ($P+0011$) y otro $P-3$, que se obtiene sumando $13$ ($1101$), porque $-3\\equiv13 \\pmod{16}$. Dos comparadores de 4 bits comparan $P_2$ con cada extremo: $P_2\\le P+3$ (salidas «menor» o «igual») y $P_2\\ge P-3$ (salidas «mayor» o «igual»). La puerta 2 se abre si se cumplen las dos: 2 OR y 1 AND.'),
    ('Rango útil', 'Como $P_1\\ge6$, $P$ vale 3 o 4, así que $P-3$ es 0 o 1 y nunca «da la vuelta» a números negativos. Por eso basta con comparar en binario puro.'),
    ('Comprobación', 'El programa recorre $P_1\\in0..9$ y $P_2\\in0..15$ y confirma las dos condiciones.')],
   'Tres comparadores, dos sumadores 4+4, 3 puertas OR/AND. Con la corrección indicada abajo el circuito cumple el enunciado en todo el rango.' + ojo('En el esquema el comparador de la puerta 1 tiene la constante $0101$ en la entrada $A$ y la clave $P_1$ en la $B$, y se toma la salida $A>B$. Eso da «$5>P_1$», o sea, abriría la puerta para $P_1<5$, justo al revés de lo que dice el enunciado ($P_1\\ge6$). La solución es tomar la salida $A<B$ ($5<P_1$) o intercambiar las entradas. Comprobado por código.'))

# ================================================================ 5.20 tres personas, dos microinterruptores cada una
def leds(a, b_, c):
    eab, eac, ebc = int(a == b_), int(a == c), int(b_ == c)
    L3 = eab & ebc
    L2 = eab | eac | ebc
    L2S = (eab & (1 - eac)) | (eac & (1 - ebc)) | (ebc & (1 - eac))
    L1 = (1 - L3) & (1 - L2) & (1 - L2S)
    return L3, L2, L2S, L1
def leds_ref(a, b_, c):
    k = len({a, b_, c})
    return (int(k == 1), int(k <= 2), int(k == 2), int(k == 3))
ok520 = all(leds(a, b_, c) == leds_ref(a, b_, c) for a in range(4) for b_ in range(4) for c in range(4))
check('lb5.p520', ok520)
check('lb5.p520.L1_es_NOT_L2', all(leds(a, b_, c)[3] == 1 - leds(a, b_, c)[1] for a in range(4) for b_ in range(4) for c in range(4)))
ej('lb5-20', 'Tres personas y cuatro leds según cuántos números coinciden', 'Libro · Cap. 5 · P5.20', 'msi,comparador', 'lb5.p520',
   'Tres personas codifican con microinterruptores, cada una en dos bits, un número de 0 a 3. Diseña el circuito que active uno de los cuatro leds: L3 si los tres números son iguales, L2 si al menos dos son iguales, L2S si solo dos son iguales y L1 en el resto de casos.',
   '**Tres parejas posibles:** (A,B), (A,C) y (B,C). Si se comparan las tres parejas con comparadores de igualdad de 2 bits, cada led es una combinación sencilla de los tres resultados $e_{AB},e_{AC},e_{BC}$.',
   [('Comparar', 'Tres comparadores de 2 bits, usando solo la salida $A=B$.'),
    ('L3 y L2', '$L3=e_{AB}\\,e_{BC}$ (si $A=B$ y $B=C$, los tres son iguales). $L2=e_{AB}+e_{AC}+e_{BC}$ (al menos una pareja coincide).'),
    ('L2S', 'Solo una pareja coincide: $L2S=e_{AB}\\overline{e_{AC}}+e_{AC}\\overline{e_{BC}}+e_{BC}\\overline{e_{AC}}$ (3 AND, un OR y 2 inversores). Es más fácil de leer como «hay exactamente una pareja que coincide».'),
    ('L1', '$L1=\\overline{L3+L2+L2S}$, una NOR de tres entradas (o 3 inversores y 1 AND). Pero $L3$ y $L2S$ implican $L2$, así que $L1=\\overline{L2}$ basta: **un solo inversor**.'),
    ('Comprobación', 'Con las $4^3=64$ ternas, las cuatro salidas coinciden con la cuenta de cuántos valores distintos hay (1, 2 o 3).')],
   'Tres comparadores de 2 bits y unas pocas puertas. Verificado con las 64 ternas, y se ha comprobado que $L1=\\overline{L2}$.')

# ---------------------------------------------------------------- SALIDA
def finish():
    open(os.path.join(ROOT, 'src', 'libro5.dsl'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    bad = [c for c in CHK if not c['ok']]
    json.dump({'R': R, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results11.json'), 'w'), ensure_ascii=False)
    print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
finish()
