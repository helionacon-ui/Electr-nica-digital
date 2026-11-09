# -*- coding: utf-8 -*-
"""Capítulo 7 del libro de problemas (registros y contadores): simula cada circuito, verifica y genera src/libro7.dsl."""
import json, os, sys, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from l7_lib import *
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
def ojo(txt): return '\n\n@box ojo | Errata en el libro\n' + txt + '\n@end'
def cron(rows, title='', rh=34, w=8, grid=4):
    return '@fig cron ' + json.dumps({'signals': rows, 'title': title, 'rh': rh, 'w_slot': w, 'grid': grid}, ensure_ascii=False)
def b4(n): return format(n, '04b')
def sync(ck, init, nxt, edge='r'):
    """Registro síncrono: en cada flanco toma nxt(estado anterior). Devuelve estados por ranura."""
    q = init; seq = []; ed = set(edge_slots(ck, edge))
    for k in range(len(ck)):
        if k in ed: q = nxt(q)
        seq.append(q)
    return seq
QB = 'Q̄'

W('%% id=libro7'); W('%% group=ejer'); W('%% n=3.7'); W('%% title=Libro de problemas · Capítulo 7 · Registros y contadores')
W('%% short=Libro · Cap. 7 Registros y contadores'); W('%% sub=Veintidós problemas de registros, contadores síncronos y asíncronos, 74160/74163 y aplicaciones: cada circuito se ha simulado y comprobado.'); W()
W('@box idea | Cómo leer esta sección')
W('Son los problemas resueltos del capítulo 7 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras. Los esquemas del libro **no se copian**: cada circuito se describe en texto (qué entradas lleva cada puerta o multiplexor) y se simula con un modelo propio; los cronogramas y las tablas salen de esa simulación. La teoría está en [[t07|el tema 7]].')
W('')
W('Modelo de los contadores integrados que usa el capítulo (cuenta en cada flanco de subida del reloj):')
W('')
W(tab(['CLEAR', 'LOAD', 'ENP·ENT', 'Efecto en el flanco', 'RCO'], [
    ['0', '×', '×', 'borra a 0000 (sin esperar al reloj)', '0'],
    ['1', '0', '×', 'carga $D_3..D_0$', '—'],
    ['1', '1', '0', 'mantiene', '—'],
    ['1', '1', '1', 'cuenta $+1$ (74160: de 9 pasa a 0; 74163: de 15 pasa a 0)', '1 si el valor es el último (9 ó 15) y ENT=1']]))
W('')
W('El 74160 es un contador **BCD** (módulo 10) y el 74163 es un contador **binario** de cuatro bits (módulo 16). El borrado se trata como asíncrono, la carga es síncrona (necesita flanco) y las entradas de habilitación ENP y ENT se usan juntas como una sola.')
W('@end'); W()

def bus(drivers):
    v = [d for d in drivers if d is not None]
    if not v: return 'Z'
    return v[0] if all(x == v[0] for x in v) else 'X'

# ================================================================ 7.1 registro universal con multiplexores
def mux4(sel, a, b, c, d): return (a, b, c, d)[sel]
def reg71(n, s1, s0, e):
    q = [(n >> i) & 1 for i in range(4)]; E = [(e >> i) & 1 for i in range(4)]
    d = [mux4(2 * s1 + s0, q[i], 0, 1 - q[i], E[i]) for i in range(4)]
    return sum(d[i] << i for i in range(4))
ok = all(reg71(n, s1, s0, e) == [n, 0, n ^ 15, e][2 * s1 + s0] for n in range(16) for e in range(16) for s1 in (0, 1) for s0 in (0, 1))
check('lb7.p71', ok)
check('lb7.p71.bus_compartido', all(bus([(n >> i) & 1 if eo1 else None, (m >> i) & 1 if (1 - eo1) else None]) in (0, 1) for n in range(16) for m in range(16) for eo1 in (0, 1) for i in range(4)) and bus([1, 0]) == 'X')
ej('lb7-1', 'Registro universal de 4 bits con multiplexores 4:1', 'Libro · Cap. 7 · P7.1', 'registro,mux,tri-estado', 'lb7.p71',
   'Dibuja un registro de 4 bits con biestables D cuya operación se elige con dos líneas de control $S_1S_0$: $11$ carga en paralelo la entrada $E_3..E_0$, $10$ invierte el contenido, $01$ lo pone a cero de forma **síncrona** y $00$ lo deja como está. Añade una línea $EO$ (enable de salida) que ponga las salidas en alta impedancia mediante buffers triestado. Hay también una entrada de borrado asíncrono $\\overline{INICIO}$.',
   '**Un multiplexor delante de cada D.** El biestable D copia lo que le llegue; si lo que le llega es una de cuatro posibilidades elegidas por $S_1S_0$, se consigue cada operación sin tocar el biestable.',
   [('Qué lleva cada entrada del multiplexor', 'Para el bit $i$, el mux 4:1 recibe: entrada 0 → $Q_i$; entrada 1 → el valor constante 0; entrada 2 → $\\overline{Q_i}$; entrada 3 → $E_i$. Las líneas $S_1S_0$ van a las entradas de selección de **los cuatro multiplexores a la vez**.'),
    ('Por qué funciona', '$S_1S_0=00$: $D_i=Q_i$, y el flanco vuelve a escribir lo mismo (**inhibición**). $01$: $D_i=0$ (**borrado síncrono**, distinto del asíncrono $\\overline{INICIO}$, que no espera al reloj). $10$: $D_i=\\overline{Q_i}$ (**volteo**). $11$: $D_i=E_i$ (**carga**).'),
    ('Salida con triestados', 'Cada $Q_i$ pasa por un buffer triestado gobernado por $EO$: con $EO=1$ la salida muestra el valor y con $EO=0$ queda desconectada (Z), de modo que varios registros pueden compartir los mismos hilos de un bus.')],
   tab(['$S_1S_0$', 'Entrada del mux que se elige', '$D_i$', 'Operación'], [['00', '0', '$Q_i$', 'inhibición'], ['01', '1', '0', 'borrado síncrono'], ['10', '2', '$\\overline{Q_i}$', 'volteo'], ['11', '3', '$E_i$', 'carga en paralelo']])
   + '\n\nComprobado de forma exhaustiva: las $16\\cdot16\\cdot4=1024$ combinaciones de estado, entrada y selección coinciden con la descripción funcional (conservar, 0, $n\\oplus1111$, $E$).')

# ================================================================ 7.2 registro con rotación
def reg72(n, s1, s0, e):
    q = [(n >> i) & 1 for i in range(4)]; E = [(e >> i) & 1 for i in range(4)]
    # entradas del mux del bit i: 0:Q_i  1:Q_{i+1}  2:Q_{i-1}  3:E_i   (índices módulo 4)
    d = [mux4(2 * s1 + s0, q[i], q[(i + 1) % 4], q[(i - 1) % 4], E[i]) for i in range(4)]
    return sum(d[i] << i for i in range(4))
rotr = lambda n: (n >> 1) | ((n & 1) << 3)
rotl = lambda n: ((n << 1) & 15) | (n >> 3)
ok = all(reg72(n, s1, s0, e) == [n, rotr(n), rotl(n), e][2 * s1 + s0] for n in range(16) for e in range(16) for s1 in (0, 1) for s0 in (0, 1))
check('lb7.p72', ok)
check('lb7.p72.cuatro_rot', all((lambda m: [m := rotr(m) for _ in range(4)][-1])(n) == n for n in range(16)))
check('lb7.p72.doble', all(rotl(n) == (2 * n) % 15 for n in range(15)) and rotl(15) == 15)
seq72 = [0b1011];
for _ in range(4): seq72.append(rotl(seq72[-1]))
ej('lb7-2', 'Registro de 4 bits con desplazamientos circulares', 'Libro · Cap. 7 · P7.2', 'registro,mux,rotacion', 'lb7.p72',
   'Implementa un registro de 4 bits con biestables D y cuatro operaciones elegidas por $S_1S_0$: $11$ carga en paralelo; $10$ desplaza una posición **a la izquierda con recirculación** (el bit que sale por arriba entra por abajo); $01$ desplaza **a la derecha con recirculación**; $00$ inhibe.',
   '**Cada bit toma el valor de un vecino.** Desplazar es que $D_i$ valga el bit vecino de antes del flanco; recircular es que los extremos se cierren en anillo.',
   [('Qué lleva cada multiplexor', 'Para el bit $i$ (los índices se toman módulo 4): entrada 0 → $Q_i$; entrada 1 → $Q_{i+1}$ (el vecino de más peso: **derecha**); entrada 2 → $Q_{i-1}$ (el de menos peso: **izquierda**); entrada 3 → $E_i$. El bit 3 recibe $Q_0$ en la entrada 1 y el bit 0 recibe $Q_3$ en la entrada 2, y eso es la recirculación.'),
    ('Lectura de las operaciones', '$01$: cada $D_i=Q_{i+1}$, el contenido se mueve hacia el bit 0 y el bit $Q_0$ vuelve al bit 3 (rotación a la derecha). $10$: cada $D_i=Q_{i-1}$ y $Q_3$ vuelve a $Q_0$ (rotación a la izquierda).'),
    ('Propiedades comprobadas', 'Cuatro rotaciones seguidas devuelven el valor inicial. Rotar a la izquierda equivale a **multiplicar por 2 módulo 15** (con el 15 como punto fijo): por ejemplo $1011\\to0111\\to1110\\to1101\\to1011$ ($11\\to7\\to14\\to13\\to11$).')],
   'Rotación a la izquierda de $1011$ en cuatro flancos: ' + ' → '.join(b4(x) for x in seq72) + '.\n\n' +
   tab(['$S_1S_0$', 'Mux del bit $i$ elige', 'Operación'], [['00', '$Q_i$', 'inhibición'], ['01', '$Q_{i+1}$', 'rotación a la derecha'], ['10', '$Q_{i-1}$', 'rotación a la izquierda'], ['11', '$E_i$', 'carga en paralelo']])
   + '\n\nVerificado con las 1024 combinaciones de estado, entrada y selección.')

# ================================================================ 7.3 registro con dos buses bidireccionales
def bus(drivers):
    v = [d for d in drivers if d is not None]
    if not v: return 'Z'
    return v[0] if all(x == v[0] for x in v) else 'X'
def regbus(C, q, A_ext, B_ext):
    """Un bit. Triestados: A→D con C=1, B→D con C=0, Q→B con C=1, Q→A con C=0."""
    A = bus([A_ext, q if C == 0 else None]); B = bus([B_ext, q if C == 1 else None])
    D = A if C == 1 else B
    return A, B, D
ok = True
for C in (0, 1):
    for q in (0, 1):
        for x in (0, 1):
            # la fuente externa debe respetar el sentido: C=1 manda A, C=0 manda B
            A, B, D = regbus(C, q, x if C == 1 else None, x if C == 0 else None)
            ok &= (D == x) and ((B if C == 1 else A) == q) and A != 'X' and B != 'X'
check('lb7.p73', ok)
# error de uso: C=1 y alguien manda por B con otro valor -> conflicto
conf = [regbus(1, q, 0, 1 - q)[1] for q in (0, 1)]
check('lb7.p73.conflicto', conf == ['X', 'X'])
check('lb7.p73.alta_z', regbus(1, 0, 1, None)[0] == 1 and regbus(0, 0, None, 1)[0] == 0)
ej('lb7-3', 'Registro con dos buses bidireccionales', 'Libro · Cap. 7 · P7.3', 'registro,tri-estado,bus', 'lb7.p73',
   'Diseña un registro de 4 bits con dos buses de datos bidireccionales, $A_3..A_0$ y $B_3..B_0$. El registro se carga desde uno de los buses y se lee por el otro. Una línea $C$ fija el sentido: con $C=1$ la transferencia es de $A$ a $B$ y con $C=0$ de $B$ a $A$.',
   '**Un par de triestados por cada cara del biestable.** Se necesitan dos buffers que lleven datos hacia la entrada D (uno desde $A$ y otro desde $B$) y otros dos que saquen $Q$ hacia cada bus. Se habilitan por parejas para que nunca dos salidas empujen el mismo hilo.',
   [('Cableado por bit', 'Entrada D: un buffer desde $A_i$ habilitado con $C=1$ y otro desde $B_i$ habilitado con $C=0$ (la línea $C$ llega invertida al segundo). Salida $Q_i$: un buffer hacia $B_i$ habilitado con $C=1$ y otro hacia $A_i$ habilitado con $C=0$.'),
    ('Con $C=1$', 'El registro captura $A$ en el flanco y $Q$ se pone en $B$: transferencia $A\\to B$. El buffer $Q\\to A$ está en alta impedancia y por eso $A$ puede ser conducido desde fuera sin conflicto.'),
    ('Con $C=0$', 'Es la imagen en espejo: se captura $B$ y se muestra en $A$.'),
    ('Qué puede salir mal', 'El diseño **supone que quien conduce el bus cumple el sentido**. Si con $C=1$ otro dispositivo conduce $B$ con un valor distinto del que presenta $Q$, hay un cortocircuito lógico (conflicto). El modelo con valores $0$, $1$, $Z$ y $X$ lo detecta en los dos casos posibles.')],
   tab(['$C$', 'Se captura', 'Se muestra', 'Buffers activos'], [['1', '$A$', '$Q$ en $B$', '$A\\to D$ y $Q\\to B$'], ['0', '$B$', '$Q$ en $A$', '$B\\to D$ y $Q\\to A$']])
   + '\n\nSimulado con las ocho combinaciones de $C$, valor previo de $Q$ y dato externo: el dato llega siempre al registro y aparece en el otro bus, sin conflictos mientras se respete el sentido.')

# ================================================================ 7.4 registro con un único bus bidireccional
def regbus1(EL, q, ext):
    """Un bit con un solo bus D: EL=1 escribe (bus -> D, Q desconectada); EL=0 lee (Q -> bus)."""
    bus_v = bus([ext, q if EL == 0 else None])
    return bus_v, (bus_v if EL == 1 else None)
ok = True
for q in (0, 1):
    for x in (0, 1):
        v, d = regbus1(1, q, x); ok &= (v == x and d == x)
        v, d = regbus1(0, q, None); ok &= (v == q)
        ok &= regbus1(0, q, 1 - q)[0] == 'X'
check('lb7.p74', ok)
ej('lb7-4', 'Registro con un solo bus de datos', 'Libro · Cap. 7 · P7.4', 'registro,tri-estado,bus', 'lb7.p74',
   'Diseña un registro de 4 bits con **un único** bus de datos $D_3..D_0$ que sirve a la vez para escribirlo y para leerlo. La línea $E/\\overline L$ decide: a 1 el registro se carga desde el bus y a 0 vuelca su contenido sobre el bus.',
   '**Es el caso anterior con un solo bus**: cada bit del bus se conecta a la vez a la entrada del biestable (a través de un triestado) y a su salida (a través de otro).',
   [('Por bit', 'El buffer de escritura va del bus a la entrada D y se habilita con $E/\\overline L=1$. El buffer de lectura va de $Q$ al bus y se habilita con $E/\\overline L=0$ (llega invertido). Nunca están activos a la vez.'),
    ('Escritura', 'Con $E/\\overline L=1$ el bus es conducido por quien escribe y en el flanco el registro lo captura; $Q$ no se envía al bus.'),
    ('Lectura', 'Con $E/\\overline L=0$ el registro conduce el bus con su contenido y nadie más debe conducirlo. Durante la lectura también llega un flanco al reloj, pero el biestable captura lo que él mismo está poniendo en el bus, y por tanto no cambia.')],
   tab(['$E/\\overline L$', 'Operación', 'Quién conduce el bus'], [['1', 'se carga $D_i\\to Q_i$', 'el exterior'], ['0', 'se descarga $Q_i\\to D_i$', 'el registro']])
   + '\n\nLa lectura es idempotente: si el registro conduce el bus, lo que captura es lo que ya contenía. Comprobado para los dos valores de $Q$ y de dato externo, incluyendo el caso de conflicto (alguien más conduce el bus durante la lectura).')

# ================================================================ 7.5 contador de Johnson de 3 bits
CK75 = ckstr(8)
def johnson(q):
    q0, q1, q2 = q
    return (1 - q2, q0, q1)
S75 = sync(CK75, (0, 0, 0), johnson)
vals75 = []; q = (0, 0, 0)
for _ in range(8): vals75.append(q[2] * 4 + q[1] * 2 + q[0]); q = johnson(q)
check('lb7.p75', vals75 == [0, 1, 3, 7, 6, 4, 0, 1])
# estados no usados forman otro ciclo
a = (0, 1, 0); b = johnson(a); c = johnson(b)
check('lb7.p75.ciclo_extra', b == (1, 0, 1) and c == a)
# decodificación con una puerta de dos entradas
def lits(q, n=3):
    res = []
    for i in range(n):
        for j in range(i + 1, n):
            for vi in (0, 1):
                for vj in (0, 1):
                    m = [s for s in cyc if s[i] == vi and s[j] == vj]
                    if m == [q]: res.append((i, vi, j, vj))
    return res
cyc = []; q = (0, 0, 0)
for _ in range(6): cyc.append(q); q = johnson(q)
check('lb7.p75.decod2', all(lits(s) for s in cyc))
def lit_txt(t):
    i, vi, j, vj = t
    return ('$Q_%d$' if vi else '$\\overline{Q_%d}$') % i + '·' + ('$Q_%d$' if vj else '$\\overline{Q_%d}$') % j
dec75 = [[b3(s) if False else '%d%d%d' % (s[2], s[1], s[0]), lit_txt(lits(s)[0])] for s in cyc]
ej('lb7-5', 'Contador de Johnson de tres bits', 'Libro · Cap. 7 · P7.5', 'contador,johnson,cronograma', 'lb7.p75',
   'Tres biestables D con el mismo reloj están enlazados así: $D_0=\\overline{Q_2}$, $D_1=Q_0$, $D_2=Q_1$. Completa el cronograma partiendo de $Q_2Q_1Q_0=000$ e indica de qué contador se trata.',
   '**Un registro de desplazamiento realimentado con el último bit negado.** Cada bit copia al anterior y el primero recibe lo contrario del último, de modo que el registro se va llenando de unos y después de ceros.',
   [('Cada flanco', 'El contenido se desplaza una posición hacia $Q_2$ y entra por $Q_0$ el complemento de lo que salía por $Q_2$. Partiendo de 000 los unos entran uno a uno (001, 011, 111) y a continuación los ceros (110, 100, 000).'),
    ('Qué contador es', 'Es un **contador de Johnson** (o de anillo retorcido) de 3 bits: $2\\cdot3=6$ estados de los $2^3=8$ posibles, **módulo 6**. Entre dos estados consecutivos cambia un solo bit.'),
    ('Estados sobrantes', 'Los estados 010 y 101 no pertenecen a la secuencia y forman un ciclo aparte (010 → 101 → 010). Si el contador arranca en uno de ellos no entra solo en la secuencia útil; hay que inicializarlo.')],
   cron([['Ck', CK75], ['Q0', bits(S75, 0)], ['Q1', bits(S75, 1)], ['Q2', bits(S75, 2)]], 'Contador de Johnson de 3 bits', 34, w=8, grid=8)
   + '\n\nSecuencia $Q_2Q_1Q_0$: ' + ' → '.join('%d%d%d' % (s[2], s[1], s[0]) for s in cyc + [cyc[0]]) + '.\n\n'
   + 'Cada estado se identifica con una puerta de **solo dos entradas** (por ser un código con un único cambio entre estados):\n\n'
   + tab(['Estado', 'Decodificador'], dec75))

# ================================================================ 7.6 contadores asíncronos con D
CK76 = ckstr(8)
FF1 = [(('ck', 'r'), lambda q: 1 - q[0]), (('q', 0, 'r'), lambda q: 1 - q[1])]
S76a, _ = ripple(FF1, CK76, [0, 0])
seq76a = [val(s) for s in S76a]
sa = []; [sa.append(x) for x in seq76a if not sa or sa[-1] != x]
check('lb7.p76.c1', all(sa[i] == [0, 3, 2, 1][i % 4] for i in range(len(sa))) and len(sa) >= 5)
FF2 = [(('ck', 'r'), lambda q: 1 - q[0]), (('ck', 'f'), lambda q: q[0])]
S76b, _ = ripple(FF2, CK76, [0, 0])
sb = []; [sb.append(val(x)) for x in S76b if not sb or sb[-1] != val(x)]
check('lb7.p76.c2', sb[:9] == [0, 1, 3, 2, 0, 1, 3, 2, 0] and all(sb[i] == [0, 1, 3, 2][i % 4] for i in range(len(sb))))
check('lb7.p76', all(c['ok'] for c in CHK if c['id'] in ('lb7.p76.c1', 'lb7.p76.c2')))
ej('lb7-6', 'Dos contadores con biestables D: uno asíncrono y otro «aberrante»', 'Libro · Cap. 7 · P7.6', 'contador,asincrono,cronograma', 'lb7.p76',
   'Completa los cronogramas de dos circuitos de dos biestables D e indica qué secuencia generan. **Circuito 1:** cada biestable tiene $D=\\overline Q$ (se carga con lo contrario de lo que tenía); el primero recibe $Ck$ y el segundo recibe $Q_0$ como reloj, ambos activos por flanco de subida. **Circuito 2:** el primero es igual (D $=\\overline{Q_0}$, flanco de subida de $Ck$); el segundo tiene $D=Q_0$ y es activo por **flanco de bajada** de $Ck$.',
   '**Hay que preguntar a cada biestable qué hace y cuándo lo hace.** Lo primero lo dice el valor de D; lo segundo, la señal que mueve su reloj.',
   [('Circuito 1 (asíncrono)', '$Q_0$ cambia en cada flanco de subida de $Ck$. $Q_1$ cambia en cada flanco de subida de **$Q_0$**, que no es el reloj general: por eso el circuito es asíncrono. Como los flancos de subida de $Q_0$ llegan cada dos relojes, $Q_1$ cambia más despacio.'),
    ('Secuencia del circuito 1', 'En el primer flanco $Q_0$ pasa de 0 a 1 y arrastra a $Q_1$, que también pasa a 1: se va de 00 a **11**. Después 10, 01, 00: es un contador **descendente de módulo 4** ($Q_1Q_0$: 00, 11, 10, 01, 00…).'),
    ('Circuito 2', '$Q_0$ cambia en cada flanco de subida; $Q_1$ copia a $Q_0$ en cada flanco de **bajada**. Con medio periodo de desfase, la secuencia es 00, 01, 11, 10, 00…: el **código Gray** de dos bits. Cada cambio de estado tiene lugar en un flanco distinto, subida o bajada.'),
    ('Valoración', 'Los biestables del circuito 2 son síncronos pero respecto de **flancos diferentes** del mismo reloj. El circuito funciona, pero es el tipo de truco que se evita en un diseño síncrono: su interés es teórico.')],
   cron([['Ck', CK76], ['Q0', bits(S76a, 0)], ['Q1', bits(S76a, 1)]], 'Circuito 1: contador descendente asíncrono', 30, grid=8)
   + '\n\n' + cron([['Ck', CK76], ['Q0', bits(S76b, 0)], ['Q1', bits(S76b, 1)]], 'Circuito 2: secuencia Gray de dos bits', 30, grid=4)
   + '\n\nSecuencia $Q_1Q_0$ del circuito 1: ' + ' → '.join(b4(x)[2:] for x in sa[:5]) + '. Del circuito 2 (un estado por cada medio periodo): ' + ' → '.join(b4(x)[2:] for x in sb[:5]) + '.')

# ================================================================ 7.7 contador asíncrono con línea TIPO
CK77 = ckstr(9)
res77 = {}
for tipo in (1, 0):
    ffs = [(('ck', 'f'), (lambda q, t=tipo: q[0] ^ t)), (('q', 0, 'f'), lambda q: 1 - q[1]), (('q', 1, 'f'), lambda q: 1 - q[2])]
    S, _ = ripple(ffs, CK77, [0, 0, 0]); res77[tipo] = S
v1 = []; [v1.append(val(x)) for x in res77[1] if not v1 or v1[-1] != val(x)]
v0 = set(val(x) for x in res77[0])
check('lb7.p77', v1 == [0, 1, 2, 3, 4, 5, 6, 7, 0, 1] and v0 == {0})
ej('lb7-7', 'Contador asíncrono con una línea TIPO', 'Libro · Cap. 7 · P7.7', 'contador,asincrono,cronograma,jk', 'lb7.p77',
   'Tres biestables J‑K activos por flanco de bajada están encadenados: el primero recibe $Ck$, el segundo recibe $Q_0$ y el tercero recibe $Q_1$ como reloj. Las entradas $J_1=K_1=J_2=K_2=1$, mientras que $J_0=K_0=TIPO$. Completa el cronograma para $TIPO=1$ y para $TIPO=0$ e indica la secuencia en cada caso.',
   '**Con $J=K=1$ un J‑K voltea en cada flanco; con $J=K=0$ no hace nada.** El primer biestable manda: si no voltea, tampoco lo harán los siguientes, porque no recibirán flancos.',
   [('$TIPO=1$', 'Los tres biestables voltean. $Q_0$ cambia en cada bajada de $Ck$; $Q_1$ lo hace en cada bajada de $Q_0$ y $Q_2$ en cada bajada de $Q_1$. Al ser flancos de bajada encadenados el conjunto cuenta **hacia arriba**: 000, 001, 010, …, 111, 000. Es un **contador asíncrono ascendente de módulo 8**.'),
    ('$TIPO=0$', '$J_0=K_0=0$: el primero **mantiene** su valor, $Q_0$ no cambia y el segundo no recibe flancos. Como tampoco los recibe el tercero, el contador **se queda donde estaba** (aquí, en 000).'),
    ('Resumen', 'La línea TIPO funciona como un **enable** de la cuenta: con TIPO a 0 el contador está parado y con TIPO a 1 cuenta en binario natural.')],
   cron([['Ck', CK77], ['Q0', bits(res77[1], 0)], ['Q1', bits(res77[1], 1)], ['Q2', bits(res77[1], 2)]], 'TIPO = 1: cuenta ascendente módulo 8', 30, grid=8)
   + '\n\n' + cron([['Ck', CK77], ['Q0', bits(res77[0], 0)], ['Q1', bits(res77[0], 1)], ['Q2', bits(res77[0], 2)]], 'TIPO = 0: el contador no cuenta', 30, grid=8))

# ================================================================ 7.8 contador BCD síncrono con J-K
def jk_from(q, qn):
    if q == 0 and qn == 0: return (0, 'X')
    if q == 0 and qn == 1: return (1, 'X')
    if q == 1 and qn == 0: return ('X', 1)
    return ('X', 0)
nxt78 = {n: (n + 1) % 10 for n in range(10)}
tab78 = {}
for n in range(10):
    m = nxt78[n]; row = []
    for i in (3, 2, 1, 0):
        row += list(jk_from((n >> i) & 1, (m >> i) & 1))
    tab78[n] = row
# tabla impresa en el libro (J3 K3 J2 K2 J1 K1 J0 K0), filas 0..9
book78 = {0: '0X 0X 0X 1X', 1: '0X 0X 1X X1', 2: '0X 0X X0 1X', 3: '0X 1X X1 X1', 4: '0X X0 0X 1X', 5: '0X X0 1X X1', 6: '0X X0 X0 1X', 7: '1X X1 X1 X1', 8: 'X0 0X 0X 1X', 9: 'X1 0X 0X X1'}
def pairs(row): return ' '.join(''.join(str(x) for x in row[i:i + 2]) for i in range(0, 8, 2))
# la fila 3 del libro: 0011->0100: J3=0 K3=X, J2=1 K2=X, J1=X K1=1, J0=X K0=1
book78[3] = '0X 1X X1 X1'; book78[1] = '0X 0X 1X X1'
check('lb7.p78.tabla', all(pairs(tab78[n]) == book78[n] for n in range(10)), {n: pairs(tab78[n]) for n in range(10)})
def Q(n, i): return (n >> i) & 1
simp = {'J3': lambda n: Q(n, 2) & Q(n, 1) & Q(n, 0), 'K3': lambda n: Q(n, 0), 'J2': lambda n: Q(n, 1) & Q(n, 0), 'K2': lambda n: Q(n, 1) & Q(n, 0),
        'J1': lambda n: (1 - Q(n, 3)) & Q(n, 0), 'K1': lambda n: Q(n, 0), 'J0': lambda n: 1, 'K0': lambda n: 1}
ok = True
for n in range(10):
    row = dict(zip(['J3', 'K3', 'J2', 'K2', 'J1', 'K1', 'J0', 'K0'], tab78[n]))
    for k, f in simp.items():
        if row[k] != 'X' and row[k] != f(n): ok = False
check('lb7.p78.simplificadas', ok)
def jkstep(n):
    nn = 0
    for i in range(4):
        J = simp['J%d' % i](n); K = simp['K%d' % i](n); q = Q(n, i)
        nn |= (J & (1 - q) | (1 - K) & q) << i
    return nn
cyc78 = [0]
for _ in range(10): cyc78.append(jkstep(cyc78[-1]))
check('lb7.p78.ciclo', cyc78 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
inval = {n: [n] for n in range(10, 16)}
for n in range(10, 16):
    while inval[n][-1] > 9: inval[n].append(jkstep(inval[n][-1]))
check('lb7.p78.autocorrige', all(len(v) <= 3 for v in inval.values()) and inval[10] == [10, 11, 4] and inval[14] == [14, 15, 0])
book('lb7.p78.canon', False, 'En las formas canónicas el libro rotula dos veces J3: la segunda (Σ(3)) es J2.')
rows78 = [[b4(n)] + [str(x) for x in tab78[n]] for n in range(10)]
ej('lb7-8', 'Contador BCD síncrono ascendente con biestables J‑K', 'Libro · Cap. 7 · P7.8', 'contador,sincrono,diseño,jk', 'lb7.p78',
   'Diseña un contador síncrono ascendente BCD (0, 1, …, 9, 0, …) con biestables J‑K activos por flanco de subida.',
   '**Método de diseño síncrono:** se escribe la tabla de estados (estado actual → siguiente), se traduce a las entradas J y K que hacen falta en cada biestable mediante la tabla de excitación, se simplifica con Karnaugh y se cablean las funciones. Los seis estados 1010…1111 no existen en BCD y se toman como indiferentes.',
   [('Tabla de excitación del J‑K', 'Para cada biestable: $0\\to0$ pide $J=0,K=\\times$; $0\\to1$ pide $J=1,K=\\times$; $1\\to0$ pide $J=\\times,K=1$; $1\\to1$ pide $J=\\times,K=0$.'),
    ('Tabla del contador', 'Se calcula J y K de cada bit para cada una de las diez filas del BCD (tabla del resultado). Las seis filas restantes valen $\\times$ en todas las entradas.'),
    ('Simplificación', 'Con Karnaugh y las indiferencias: $J_3=Q_2Q_1Q_0$, $K_3=Q_0$, $J_2=K_2=Q_1Q_0$, $J_1=\\overline{Q_3}Q_0$, $K_1=Q_0$, $J_0=K_0=1$. El bit 0 siempre voltea y los demás voltean cuando todos los de menor peso valen 1, con la salvedad de que $Q_1$ no debe subir cuando $Q_3=1$ (para no pasar de 9 a 10).'),
    ('Comprobación', 'Se ha simulado el contador con esas ecuaciones: 0, 1, …, 9, 0. Además se ha comprobado qué pasa en los estados no usados: **todos entran solos en la secuencia** en un máximo de dos ciclos (10 → 11 → 4; 12 → 13 → 4; 14 → 15 → 0): el contador es **autocorrector**. Es una propiedad que el libro no analiza.')],
   tab(['$Q_3Q_2Q_1Q_0$', '$J_3$', '$K_3$', '$J_2$', '$K_2$', '$J_1$', '$K_1$', '$J_0$', '$K_0$'], rows78)
   + '\n\nFunciones: $J_3=Q_2Q_1Q_0$; $K_3=Q_0$; $J_2=K_2=Q_1Q_0$; $J_1=\\overline{Q_3}\\,Q_0$; $K_1=Q_0$; $J_0=K_0=1$.\n\n'
   + 'Estados no usados: ' + '; '.join(' → '.join(str(x) for x in v) for v in inval.values()) + '.'
   + ojo('En las formas canónicas el libro escribe dos veces «J3»: la segunda lista ($\\Sigma(3)$) corresponde a $J_2$, como indican la tabla y el diagrama de Karnaugh.'))

# ================================================================ 7.9 contador Gray síncrono mod 16
gray = lambda n: n ^ (n >> 1)
inv_gray = {gray(n): n for n in range(16)}
nxt79 = {gray(n): gray((n + 1) % 16) for n in range(16)}
tab79 = {}
for p in range(16):
    m = nxt79[p]; row = []
    for i in (3, 2, 1, 0): row += list(jk_from((p >> i) & 1, (m >> i) & 1))
    tab79[p] = row
J79 = {'J3': [4], 'K3': [8], 'J2': [2], 'K2': [14], 'J1': [1, 13], 'K1': [7, 11], 'J0': [0, 6, 10, 12], 'K0': [3, 5, 9, 15]}
ok = True
for k, ms in J79.items():
    col = {'J3': 0, 'K3': 1, 'J2': 2, 'K2': 3, 'J1': 4, 'K1': 5, 'J0': 6, 'K0': 7}[k]
    ones = [p for p in range(16) if tab79[p][col] == 1]
    if ones != ms: ok = False; print('Gray', k, ones, ms)
check('lb7.p79.canonicas', ok)
def L(p, i): return (p >> i) & 1
simp79 = {'J3': lambda p: (1 - L(p, 3)) * 0 + L(p, 2) & (1 - L(p, 1)) & (1 - L(p, 0)),
          'K3': lambda p: (1 - L(p, 2)) & (1 - L(p, 1)) & (1 - L(p, 0)),
          'J2': lambda p: (1 - L(p, 3)) & L(p, 1) & (1 - L(p, 0)),
          'K2': lambda p: L(p, 3) & L(p, 1) & (1 - L(p, 0)),
          'J1': lambda p: (L(p, 3) & L(p, 2) & L(p, 0)) | ((1 - L(p, 3)) & (1 - L(p, 2)) & L(p, 0)),
          'K1': lambda p: ((1 - L(p, 3)) & L(p, 2) & L(p, 0)) | (L(p, 3) & (1 - L(p, 2)) & L(p, 0)),
          'J0': lambda p: 1 - (L(p, 3) ^ L(p, 2) ^ L(p, 1)),
          'K0': lambda p: L(p, 3) ^ L(p, 2) ^ L(p, 1)}
def step79(p):
    nn = 0
    for i in range(4):
        Jv = simp79['J%d' % i](p); Kv = simp79['K%d' % i](p); q = L(p, i)
        nn |= ((Jv & (1 - q)) | ((1 - Kv) & q)) << i
    return nn
c79 = [0]
for _ in range(16): c79.append(step79(c79[-1]))
check('lb7.p79.ciclo', c79 == [gray(n % 16) for n in range(17)])
check('lb7.p79.un_bit', all(bin(c79[i] ^ c79[i + 1]).count('1') == 1 for i in range(16)))
check('lb7.p79.paridad', all(simp79['K0'](p) == (L(p, 3) ^ L(p, 2) ^ L(p, 1)) and simp79['J0'](p) == 1 - simp79['K0'](p) for p in range(16)) and all(tab79[p][7] in ('X', simp79['K0'](p)) and tab79[p][6] in ('X', simp79['J0'](p)) for p in range(16)))
rows79 = [[b4(p), b4(nxt79[p])] + [str(x) for x in tab79[p]] for p in sorted(nxt79, key=lambda p: inv_gray[p])]
ej('lb7-9', 'Contador Gray síncrono de módulo 16', 'Libro · Cap. 7 · P7.9', 'contador,sincrono,diseño,gray,jk', 'lb7.p79',
   'Diseña un contador síncrono ascendente de módulo 16 que recorra los estados en código Gray, con biestables J‑K.',
   '**Mismo método que el contador BCD, con otra tabla de estados.** Cada estado pasa al siguiente código Gray (0000, 0001, 0011, 0010, 0110, …, 1000, 0000). Como hay 16 estados, no queda ninguna indiferencia en las filas: solo las que aporta la tabla de excitación del J‑K.',
   [('Tabla de estados y excitación', 'Se asigna a cada estado el siguiente de la secuencia Gray y se calculan J y K de cada bit con la misma tabla de excitación del problema anterior.'),
    ('Funciones', 'Las formas canónicas ($\\Sigma$ de las filas, numeradas por el valor binario del estado) son $J_3=\\Sigma(4)$, $K_3=\\Sigma(8)$, $J_2=\\Sigma(2)$, $K_2=\\Sigma(14)$, $J_1=\\Sigma(1,13)$, $K_1=\\Sigma(7,11)$, $J_0=\\Sigma(0,6,10,12)$ y $K_0=\\Sigma(3,5,9,15)$. Con las indiferencias salen: $J_3=Q_2\\overline{Q_1}\\,\\overline{Q_0}$, $K_3=\\overline{Q_2}\\,\\overline{Q_1}\\,\\overline{Q_0}$, $J_2=\\overline{Q_3}Q_1\\overline{Q_0}$, $K_2=Q_3Q_1\\overline{Q_0}$, $J_1=Q_3Q_2Q_0+\\overline{Q_3}\\,\\overline{Q_2}Q_0$, $K_1=\\overline{Q_3}Q_2Q_0+Q_3\\overline{Q_2}Q_0$ y los de $J_0$ y $K_0$ con cuatro términos cada uno.'),
    ('Una simplificación más', 'Los cuatro términos de $J_0$ y de $K_0$ son los de la **paridad** de $Q_3Q_2Q_1$: $K_0=Q_3\\oplus Q_2\\oplus Q_1$ y $J_0=\\overline{K_0}$. Es lógico: en una secuencia Gray el bit menos significativo cambia siempre que haga falta mantener la paridad total, y se comprueba al simular. (Es una observación propia, no del libro.)'),
    ('Comprobación', 'Con las funciones simplificadas el contador recorre los 16 estados en el orden Gray y vuelve al inicio; entre dos estados consecutivos cambia exactamente un bit.')],
   tab(['$Q_3..Q_0$ (t)', '$Q_3..Q_0$ (t+1)', '$J_3$', '$K_3$', '$J_2$', '$K_2$', '$J_1$', '$K_1$', '$J_0$', '$K_0$'], rows79)
   + '\n\nSecuencia: ' + ' → '.join(b4(x) for x in c79) + '.')

# ================================================================ 7.10 mod 60, mod 1000, mod 12 con 74160/74163
# --- módulo 60
u = Cnt(10); t = Cnt(10); seq60 = []
for k in range(130):
    seq60.append(t.q * 10 + u.q)
    ru = u.rco(1); load_t = 0 if (t.q == 5 and u.q == 9) else 1       # NAND(Q2,Q0 decenas, RCO unidades) a LOAD (decenas, D=0)
    tn = (t.clk, dict(load=load_t, en=ru, d=0)); un = (u.clk, dict())
    tn[0](**tn[1]); un[0](**un[1])
check('lb7.p710.mod60', seq60 == [k % 60 for k in range(130)])
u_ = Cnt(10); t_ = Cnt(10); sin_rco = []
for _k in range(60):
    sin_rco.append(t_.q * 10 + u_.q); ru_ = u_.rco(1); t_.clk(load=0 if t_.q == 5 else 1, en=ru_, d=0); u_.clk()
check('lb7.p710.sin_rco', sin_rco[48:54] == [48, 49, 50, 1, 2, 3] and 59 not in sin_rco)
book('lb7.p710.50a00', False, 'precisión: sin el RCO el contador pasa de 50 a 01, no a 00')
# --- módulo 1000
cs = [Cnt(10), Cnt(10), Cnt(10)]; seq1000 = []                       # unidades, decenas, centenas
for k in range(2100):
    seq1000.append(cs[2].q * 100 + cs[1].q * 10 + cs[0].q)
    r0 = cs[0].rco(1); r1 = cs[1].rco(r0)
    cs[2].clk(en=r0 & r1 & (cs[2].q is not None)) if False else None
    e1 = r0; e2 = r0 & (1 if cs[1].q == 9 else 0)
    cs[0].clk(); cs[1].clk(en=e1); cs[2].clk(en=e2)
check('lb7.p710.mod1000', seq1000 == [k % 1000 for k in range(2100)])
# --- módulo 12, opción A (dos 74160) y opción B (74163 + 74185)
u = Cnt(10); t = Cnt(10); seq12a = []
for k in range(40):
    seq12a.append(t.q * 10 + u.q)
    load = 0 if ((t.q & 1) and (u.q & 1)) else 1                    # NAND(Q0 decenas, Q0 unidades) a los dos LOAD
    ru = u.rco(1); tq = Cnt(10, t.q); uq = Cnt(10, u.q)
    t.clk(load=load, en=ru, d=0); u.clk(load=load, d=0)
check('lb7.p710.mod12a', seq12a == [k % 12 for k in range(40)])
c = Cnt(16); seq12b = []
for k in range(40):
    seq12b.append(c.q)
    load = 0 if (c.q & 0b1011) == 0b1011 else 1                       # NAND(Q3,Q1,Q0) = decodifica 1011
    c.clk(load=load, d=0)
check('lb7.p710.mod12b', seq12b == [k % 12 for k in range(40)])
bcd = lambda v: ((v // 10) << 4) | (v % 10)
check('lb7.p710.bcd', all(bcd(v) & 1 == v & 1 for v in range(12)) and [bcd(v) for v in range(10, 12)] == [0x10, 0x11])
ej('lb7-10', 'Contadores módulo 60, módulo 1000 y módulo 12 con circuitos integrados', 'Libro · Cap. 7 · P7.10', 'contador,74160,74163,modulo', 'lb7.p710',
   'Con contadores síncronos BCD 74160 diseña un contador de **módulo 60**; haz lo mismo para uno de **módulo 1000** y otro de **módulo 12** en BCD. Para el módulo 12 estudia también una versión con un 74163 binario y un convertidor.',
   '**Se encadenan contadores** de modo que cada uno cuente solo cuando todos los anteriores están en su último valor (conexión de RCO a ENP·ENT), y se recorta la cuenta cargando 0 cuando se llega al valor que se quiere evitar.',
   [('Módulo 60', 'Dos 74160: **unidades** (0 a 9) y **decenas**. Las decenas cuentan solo cuando las unidades valen 9 (RCO a ENP·ENT). Hay que impedir que lleguen a 6: una NAND de $Q_2$ y $Q_0$ de las decenas (valor 5) y del RCO de las unidades (valor 9) detecta 59 y se lleva a LOAD de las decenas, que carga 0 con el siguiente flanco. Así después de 59 se pasa a 00, y no a 60.'),
    ('Qué pasa si falta el RCO en la NAND', 'Si la puerta solo mirase el valor 5 de las decenas, el contador **no llegaría nunca a 51**: al llegar a 50 las decenas cargarían 0 en el flanco siguiente mientras las unidades siguen contando, y la secuencia pasaría de 50 a **01** (la cuenta quedaría en 1…50). El libro dice «de 50 a 00»; la simulación da 01. El RCO asegura que se espera a que las unidades lleguen a 9.'),
    ('Módulo 1000', 'Tres 74160 en serie y sin recorte (todos son módulo 10): unidades siempre habilitadas; decenas con RCO de unidades; **centenas con RCO·RCO**. No hace falta usar LOAD. Una propiedad curiosa del cronograma: el valor del contador coincide con el **número de flancos recibidos**, porque al llegar el primer flanco el contador ya vale 000 y pasa a 001.'),
    ('Módulo 12, opción A', 'Dos 74160 con una NAND de $Q_0$ de decenas y $Q_0$ de unidades (valor 11). Su salida va a los dos LOAD (con $D=0000$). Las decenas cuentan solo con el RCO de las unidades. Secuencia 00, 01, …, 09, 10, 11, 00.'),
    ('Módulo 12, opción B', 'Un 74163 binario con una NAND de $Q_3Q_1Q_0$ (valor 1011) que carga 0. Solo hace falta un integrado, pero la salida está en **binario** (0000 a 1011) y no en BCD. Para visualizarla en dos dígitos hay que convertirla con un conversor binario‑BCD (74185): para valores hasta 11 el bit menos significativo pasa sin cambios, porque 10 es par.')],
   tab(['Contador', 'Integrados', 'Recorte', 'Secuencia'], [['módulo 60', '2 × 74160', 'NAND ($Q_2$, $Q_0$ decenas, RCO unidades) → LOAD decenas', '00 … 59, 00'], ['módulo 1000', '3 × 74160', 'ninguno', '000 … 999, 000'], ['módulo 12 (A)', '2 × 74160', 'NAND ($Q_0$ dec., $Q_0$ uni.) → LOAD ambos', '00 … 11, 00'], ['módulo 12 (B)', '74163 + conversor', 'NAND ($Q_3,Q_1,Q_0$) → LOAD', '0000 … 1011, 0000']])
   + '\n\nSimulados los cuatro circuitos durante varios ciclos (130 flancos el de 60, 2100 el de 1000, 40 los de 12): el valor coincide en cada flanco con el contador teórico módulo $N$.')

# ================================================================ 7.11 reloj digital
def clock_sim(start, ticks, with_ms=True):
    """Reloj completo con 74160 (ms: 3, seg: 2, min: 2, horas: 2) + biestable T de PM. start = (h,m,s,ms,pm)."""
    h, mi, s, ms, pm = start
    C = {'m0': Cnt(10, ms % 10), 'm1': Cnt(10, (ms // 10) % 10), 'm2': Cnt(10, ms // 100),
         's0': Cnt(10, s % 10), 's1': Cnt(10, s // 10), 'n0': Cnt(10, mi % 10), 'n1': Cnt(10, mi // 10),
         'h0': Cnt(10, h % 10), 'h1': Cnt(10, h // 10)}
    PM = pm; log = []
    for k in range(ticks):
        c = C
        r = lambda x: x.rco(1)
        en_ms = r(c['m0']) & r(c['m1']) & r(c['m2'])                    # fin de la cuenta de milésimas
        en_s0 = en_ms
        en_s1 = en_s0 & r(c['s0'])
        s_fin = en_s1 & (1 if (c['s1'].q == 5) else 0)                  # 59 segundos y 999 ms
        en_n0 = s_fin
        en_n1 = en_n0 & r(c['n0'])
        n_fin = en_n1 & (1 if c['n1'].q == 5 else 0)
        en_h0 = n_fin
        en_h1 = en_h0 & r(c['h0'])
        h12 = 1 if (c['h1'].q == 1 and (c['h0'].q & 2)) else 0         # valor 12 (decenas Q0, unidades Q1)
        log.append((c['h1'].q * 10 + c['h0'].q, c['n1'].q * 10 + c['n0'].q, c['s1'].q * 10 + c['s0'].q, c['m2'].q * 100 + c['m1'].q * 10 + c['m0'].q, PM))
        # flanco: se evalúan todas las entradas antes de actualizar
        loads = dict(s1=0 if s_fin else 1, n1=0 if n_fin else 1, h=0 if h12 else 1)
        if h12: PM ^= 1
        e_m1 = r(c['m0']); e_m2 = r(c['m0']) & r(c['m1'])
        c['m0'].clk(); c['m1'].clk(en=e_m1); c['m2'].clk(en=e_m2)
        c['s0'].clk(en=en_s0); c['s1'].clk(load=loads['s1'], en=en_s1, d=0)
        c['n0'].clk(en=en_n0); c['n1'].clk(load=loads['n1'], en=en_n1, d=0)
        c['h0'].clk(load=loads['h'], en=en_h0, d=0); c['h1'].clk(load=loads['h'], en=en_h1, d=0)
    return log
# (1) las milésimas dan una vuelta cada 1000 flancos
l1 = clock_sim((0, 0, 0, 0, 0), 2005)
check('lb7.p711.ms', all(x[3] == k % 1000 for k, x in enumerate(l1)) and l1[1000][2] == 1 and l1[2000][2] == 2)
# (2) casos límite: precargando justo antes de cada desbordamiento
def avanza(start, ticks): return clock_sim(start, ticks)[-1]
ok = True
ok &= clock_sim((0, 0, 0, 995, 0), 10)[-1][:4] == (0, 0, 1, 4)
ok &= clock_sim((0, 0, 59, 995, 0), 10)[-1][:4] == (0, 1, 0, 4)
ok &= clock_sim((0, 59, 59, 995, 0), 10)[-1][:4] == (1, 0, 0, 4)
ok &= clock_sim((9, 59, 59, 995, 0), 10)[-1][:4] == (10, 0, 0, 4)
l_noon = clock_sim((11, 59, 59, 995, 0), 10)
ok &= [x[0] for x in l_noon][-1] == 0 and l_noon[-1][4] == 1 and l_noon[0][4] == 0
l_mid = clock_sim((11, 59, 59, 995, 1), 10)
ok &= l_mid[-1][4] == 0
check('lb7.p711.desbordes', ok, (l_noon[-1], l_mid[-1]))
# (3) un día entero a nivel de segundos (reloj de 1 Hz): 86400 flancos con el contador de horas
def clock_sec(ticks):
    c = {k: Cnt(10) for k in ('s0', 's1', 'n0', 'n1', 'h0', 'h1')}; PM = 0; log = []
    for _ in range(ticks):
        log.append((c['h1'].q * 10 + c['h0'].q, c['n1'].q * 10 + c['n0'].q, c['s1'].q * 10 + c['s0'].q, PM))
        r = lambda x: x.rco(1)
        en_s1 = r(c['s0']); s_fin = en_s1 & (c['s1'].q == 5)
        en_n1 = s_fin & r(c['n0']); n_fin = en_n1 & (c['n1'].q == 5)
        en_h1 = n_fin & r(c['h0']); h12 = 1 if (c['h1'].q == 1 and (c['h0'].q & 2)) else 0
        if h12: PM ^= 1
        c['s0'].clk(); c['s1'].clk(load=0 if s_fin else 1, en=en_s1, d=0)
        c['n0'].clk(en=s_fin); c['n1'].clk(load=0 if n_fin else 1, en=en_n1, d=0)
        c['h0'].clk(load=0 if h12 else 1, en=n_fin, d=0); c['h1'].clk(load=0 if h12 else 1, en=en_h1, d=0)
    return log
dia = clock_sec(86400 + 5)
tiempo = lambda k: ((k // 3600) % 12 if True else 0, (k // 60) % 60, k % 60)
okd = True; marca = 0
for k, (h, mi, s, pm) in enumerate(dia):
    exp_h = (k // 3600) % 12
    if k == 0: continue
    # el valor 12 solo aparece durante un flanco (el de las 12:00:00); se ignora esa fila
    if (h, mi, s) != ((k // 3600) % 12, (k // 60) % 60, k % 60) and not (h == 12 and mi == 0 and s == 0 and k % 43200 == 0):
        okd = False; print('dia', k, (h, mi, s)); break
check('lb7.p711.dia', okd)
pm_ok = all(dia[k][3] == ((k - 1) // 43200) % 2 for k in range(2, 86400))
check('lb7.p711.pm_12h', pm_ok)
ej('lb7-11', 'Reloj digital de 12 horas con un reloj de 1 kHz', 'Libro · Cap. 7 · P7.11', 'contador,74160,aplicacion,reloj', 'lb7.p711',
   'Diseña un reloj partiendo de una señal de 1 kHz y visualiza horas, minutos y segundos en displays de siete segmentos. Añade una indicación AM/PM.',
   '**Una cadena de divisores:** cada contador cuenta solo cuando el anterior ha llegado a su último valor y ahí se pone a cero para empezar de nuevo. Todos los contadores comparten el mismo reloj de 1 kHz y se encadenan con los **enables**, no con relojes distintos (diseño síncrono).',
   [('Milésimas', 'Tres 74160 en serie forman un contador de **módulo 1000**: 1000 flancos a 1 kHz son 1 s. Su fin de cuenta $RCO\\cdot RCO\\cdot RCO$ vale 1 una vez por segundo y es el enable de los segundos.'),
    ('Segundos y minutos', 'Cada pareja de 74160 es un **módulo 60** como el del problema anterior: unidades hasta 9; decenas hasta 5. Para que una pareja cuente deben cumplirse a la vez el enable de la anterior, el fin de las unidades (9) y las decenas (5) cuando toca saltar.'),
    ('Una misma puerta, dos usos', 'La puerta AND que detecta «decenas = 5, unidades = 9 y enable de la etapa anterior» sirve dos veces: da el **enable** de la etapa siguiente (minutos suman uno más) y, invertida, el **LOAD** de las decenas propias, que cargan 0 en ese mismo flanco. Es decir, cada contador se pone a cero justo cuando el siguiente cuenta.'),
    ('Horas y AM/PM', 'Para las horas se decodifica el valor 12 (decenas $Q_0$ y unidades $Q_1$) y se lleva, invertido, a los LOAD de las dos cifras. Es el recorte a módulo 12: el valor 12 solo existe durante un flanco y se pasa a 00. Esa misma señal se lleva a un **biestable T** cuyo estado es la indicación PM, que cambia cada 12 horas.'),
    ('Comprobación', 'Se ha simulado el circuito completo (9 contadores y el biestable T) en los instantes críticos precargando justo antes de cada desbordamiento: milésimas, segundos, minutos, horas, y paso por las 12 en los dos sentidos (AM→PM y PM→AM). Además, un día entero con reloj de 1 Hz (86 400 flancos) sale exacto.')],
   tab(['Etapa', 'Contador', 'Cuenta cuando…', 'Recorte'], [['milésimas', '3 × 74160', 'siempre', 'ninguno (mod 1000)'], ['segundos', '2 × 74160', 'RCO·RCO·RCO de milésimas', '59 → 00'], ['minutos', '2 × 74160', 'fin de segundos (59 s y 999 ms)', '59 → 00'], ['horas', '2 × 74160', 'fin de minutos', '12 → 00 (módulo 12) y toggle de PM']])
   + '\n\nEjemplo de paso por mediodía (milésimas en la última columna, de $11{:}59{:}59.995$ AM): ' + ' · '.join('%02d:%02d:%02d.%03d %s' % (x[0], x[1], x[2], x[3], 'PM' if x[4] else 'AM') for x in l_noon[4:9]) + '.'
   + '\n\nSe observa que el 12 aparece un solo milisegundo antes de volver a 00; la indicación PM cambia en ese flanco y no se vuelve a tocar durante 12 horas.')

exec(open(os.path.join(HERE, 'gen_libro7b.py'), encoding='utf-8').read())

# ---------------------------------------------------------------- SALIDA
def finish():
    open(os.path.join(ROOT, 'src', 'libro7.dsl'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    bad = [c for c in CHK if not c['ok']]
    json.dump({'R': R, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results13.json'), 'w'), ensure_ascii=False)
    print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
    for d in DIFF: print('  -', d)
finish()
