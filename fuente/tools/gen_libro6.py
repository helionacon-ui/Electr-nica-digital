# -*- coding: utf-8 -*-
"""Capítulo 6 del libro de problemas (biestables): simula cada dispositivo, verifica y genera src/libro6.dsl."""
import json, os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from l6_sim import *
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
def cron(rows, title='', rh=40, w=12, grid=4):
    return '@fig cron ' + json.dumps({'signals': rows, 'title': title, 'rh': rh, 'w_slot': w, 'grid': grid}, ensure_ascii=False)
def marks(*conds):
    n = len(conds[0]); return ''.join('#' if all(c[i] == '1' for c in conds) else '.' for i in range(n))
QB = 'Q̄'

W('%% id=libro6'); W('%% group=ejer'); W('%% n=3.6'); W('%% title=Libro de problemas · Capítulo 6 · Biestables')
W('%% short=Libro · Cap. 6 Biestables'); W('%% sub=Quince problemas de cronogramas y análisis de biestables R‑S, J‑K, D, T, maestro/esclavo y latch: cada cronograma sale de una simulación con puertas.'); W()
W('@box idea | Cómo se leen los cronogramas de esta sección')
W('Son los problemas resueltos del capítulo 6 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y con entradas dibujadas sobre una **cuadrícula de ranuras de tiempo** (cada línea vertical está separada cuatro ranuras; un semiperíodo de reloj son 4 ranuras). La teoría está en [[t06|el tema 6]].')
W('')
W('Convenio de los dibujos:')
W('- **Banda gris clara**: valor desconocido a priori (la salida se ha parado, pero no se sabe en qué valor).')
W('- **Banda gris oscura**: carrera (la salida bascula sin parar mientras dura la condición).')
W('- **Trazo grueso**: entrada prohibida en ese momento.')
W('- En un flanco se toma el valor de las entradas **justo antes** de él.')
W('')
W('Cada latch (R‑S, J‑K, D, y los maestros/esclavos) se ha simulado como una red de puertas NAND: las puertas se disparan en cualquier orden y, si el resultado final depende de quién gana, la salida se marca como desconocida. Las carreras se detectan cuando la combinación J=K=1 realimenta la salida mientras el nivel está activo. Los flip‑flops por flanco se simulan con su tabla de excitación. Así los cronogramas no se dibujan a mano: salen del simulador y se contrastan con el razonamiento. Si el libro tiene un fallo, aparece en un recuadro de errata.')
W('@end'); W()

def lv(s): return [int(c) for c in s]
# ---------------------------------------------------------------- entradas comunes a 6.3 – 6.6
CK36 = runs([(0, 4)] + [(1, 4), (0, 4)] * 4)
X36 = runs([(0, 11), (1, 15), (0, 10)])
Y36 = runs([(0, 13), (1, 5), (0, 4), (1, 14)])
assert len(CK36) == len(X36) == len(Y36) == 36

# ================================================================ 6.1 R-S asíncrona NAND
SbA = runs([(1, 3), (0, 3), (1, 4), (0, 4), (1, 5), (0, 1)]); RbA = runs([(1, 10), (0, 9), (1, 1)])
SbB = '11110001111111000111'; RbB = '11111111110000000111'
assert len(SbA) == len(RbA) == len(SbB) == len(RbB) == 20
def rsn(Sb, Rb):
    q, qb = simulate(rsn_step, (0, 1), [(int(a), int(b)) for a, b in zip(Sb, Rb)], [0, 1]); return q, qb
qA, qbA = rsn(SbA, RbA); qB, qbB = rsn(SbB, RbB)
expA = '000' + '1' * 11 + '0' * 5 + '1'; expbA = '111' + '0' * 7 + '1' * 9 + '0'
expB = '0000' + '111111' + '0000' + '111' + 'xxx'; expbB = '1111' + '0000' + '00' + '1111' + '111' + 'xxx'
check('lb6.p61', qA == expA and qbA == expbA and qB == expB and qbB == expbB, (qA, qbA, qB, qbB))
pA = marks(inv(SbA), inv(RbA)); pB = marks(inv(SbB), inv(RbB))
R['p61'] = dict(A=[qA, qbA], B=[qB, qbB])
ej('lb6-1', 'Báscula R‑S asíncrona con puertas NAND', 'Libro · Cap. 6 · P6.1', 'biestable,rs,cronograma', 'lb6.p61',
   'Completa los dos cronogramas de una báscula R‑S asíncrona hecha con dos puertas NAND (entradas activas en bajo, $\\overline S$ y $\\overline R$). Marca con trazo grueso cuándo la entrada está prohibida y en gris cuándo no se puede saber el valor de salida.\n\n'
   + cron([['S̄', SbA], ['R̄', RbA]], 'Primer cronograma: entradas') + '\n\n' + cron([['S̄', SbB], ['R̄', RbB]], 'Segundo cronograma: entradas'),
   '**Una tabla de cuatro filas basta.** Con $Q=\\overline{\\overline S\\cdot\\overline Q}$ y $\\overline Q=\\overline{\\overline R\\cdot Q}$: $\\overline S\\,\\overline R=11$ mantiene; $01$ pone Q a 1; $10$ pone Q a 0; $00$ es la combinación prohibida y deja **las dos salidas a 1**.',
   [('Reglas', tab(['$\\overline S$', '$\\overline R$', 'Operación', 'Q', '$\\overline Q$'], [[1, 1, 'mantiene', 'Q', '$\\overline Q$'], [0, 1, 'puesta a 1', 1, 0], [1, 0, 'puesta a 0', 0, 1], [0, 0, 'prohibida', 1, 1]])),
    ('Primer cronograma', 'Q se pone a 1 con el primer pulso bajo de $\\overline S$ y se mantiene. Cuando $\\overline R$ baja mientras $\\overline S$ también está bajo, la entrada es prohibida y las dos salidas valen 1 (trazo grueso). En cuanto $\\overline S$ sube y $\\overline R$ sigue bajo, Q pasa a 0: sale de la prohibida por **un solo lado**, y el resultado es único. Al final, $\\overline R$ sube y $\\overline S$ baja: Q vuelve a 1.'),
    ('Segundo cronograma', 'Tras la puesta a 1 y la puesta a 0, las dos entradas bajan **a la vez** (prohibida: $Q=\\overline Q=1$) y después suben también **a la vez**. Las dos puertas ven ahora «1, 1» y compiten: la que gane se queda a 0 y la otra a 1, pero no se sabe cuál. La salida queda desconocida (banda gris) hasta la siguiente puesta a 0 o a 1.'),
    ('Qué enseña', 'Pasar de $00$ a $11$ por un solo lado es seguro; hacerlo por los dos a la vez deja la báscula en un estado imprevisible. Sea cual sea el estropicio (prohibida, desconocida), una orden clara de puesta a 0 o a 1 devuelve la báscula a la normalidad.')],
   cron([['S̄', SbA], ['R̄', RbA], ['Q', qA, pA], [QB, qbA, pA]], 'Cronograma 1', 34) + '\n\n' + cron([['S̄', SbB], ['R̄', RbB], ['Q', qB, pB], [QB, qbB, pB]], 'Cronograma 2', 34)
   + '\n\nEn el primero toda la evolución es determinista (con una fase prohibida); en el segundo, la salida queda desconocida tras salir de la prohibida por los dos lados a la vez.')

# ================================================================ 6.2 J-K asíncrona
cases62 = {'A': ([(0, 2), (1, 3), (0, 4), (1, 3), (0, 5), (1, 3), (0, 4)], [(0, 12), (1, 4), (0, 5), (1, 3)]),
           'B': ([(0, 3), (1, 3), (0, 3), (1, 3), (0, 7), (1, 4), (0, 3)], [(0, 14), (1, 12)]),
           'C': ([(0, 2), (1, 3), (0, 3), (1, 3), (0, 5), (1, 5), (0, 5)], [(0, 12), (1, 9), (0, 5)])}
res62 = {}
for k, (j, kk) in cases62.items():
    J = runs(j); K = runs(kk); assert len(J) == len(K)
    q, qb = simulate(latch_step('jk'), LATCH_INIT, [(int(a), int(b), 1) for a, b in zip(J, K)], [2, 3], jk_race)
    res62[k] = (J, K, q, qb)
e62 = {'A': '00' + '1' * 10 + '0' * 5 + '1' * 4 + '000',
       'B': '000' + '1' * 11 + '0' * 5 + 'rrrr' + '000',
       'C': '00' + '1' * 10 + '0' * 4 + 'rrrrr' + 'xxxxx'}
check('lb6.p62', all(res62[k][2] == e62[k] and res62[k][3] == inv(e62[k]) for k in 'ABC'), {k: res62[k][2] for k in 'ABC'})
check('lb6.p62.A_sin_11', not any(a == '1' and b == '1' for a, b in zip(res62['A'][0], res62['A'][1])))
R['p62'] = {k: v for k, v in res62.items()}
f62 = lambda k, t: cron([['J', res62[k][0]], ['K', res62[k][1]], ['Q', res62[k][2]], [QB, res62[k][3]]], t, 34)
f62i = lambda k, t: cron([['J', res62[k][0]], ['K', res62[k][1]]], t)
ej('lb6-2', 'Báscula J‑K asíncrona: normal, con carreras y con indeterminación', 'Libro · Cap. 6 · P6.2', 'biestable,jk,carreras,cronograma', 'lb6.p62',
   'Completa los tres cronogramas de una báscula J‑K **asíncrona** (sin reloj: J y K actúan directamente sobre la salida). Señala dónde hay carreras (gris oscuro) y dónde la salida queda desconocida (gris claro).\n\n'
   + f62i('A', 'Cronograma 1: entradas') + '\n\n' + f62i('B', 'Cronograma 2: entradas') + '\n\n' + f62i('C', 'Cronograma 3: entradas'),
   '**Sin reloj no hay nada que la proteja:** un J‑K asíncrono con $J=K=1$ realimenta su propia salida y bascula sin parar. Eso es una carrera. Cuando termina, si lo hace en $00$, la salida queda parada en un valor desconocido; si termina en $10$ o $01$, el valor es el de esa orden.',
   [('Reglas', tab(['J', 'K', 'Efecto'], [[0, 0, 'mantiene'], [1, 0, 'Q = 1'], [0, 1, 'Q = 0'], [1, 1, 'carrera: Q bascula continuamente']])),
    ('Cronograma 1', 'Nunca coinciden J y K: la evolución es normal. Cada pulso de J pone Q a 1 y cada pulso de K lo pone a 0; los pulsos de J con Q ya a 1 no cambian nada.'),
    ('Cronograma 2', 'En la parte final J sube mientras K sigue a 1: $JK=11$ y la salida entra en carreras. Cuando J baja queda $JK=01$ y Q se queda en **0**, sin ambigüedad: se sale de la carrera por un solo lado. En el dibujo el basculeo se ve lento y ordenado, pero en realidad se produce a una frecuencia de megahercios, con efectos muy malos sobre el resto del circuito.'),
    ('Cronograma 3', 'Se repite la carrera, pero ahora J y K bajan **a la vez** (de $11$ a $00$). No se sabe en qué momento exacto se paró la oscilación, así que la salida queda parada en un valor desconocido hasta la siguiente orden. Evolución completa: normal, mala (carreras), peor (indeterminación) y, con una orden nueva, otra vez normal.')],
   f62('A', 'Cronograma 1') + '\n\n' + f62('B', 'Cronograma 2') + '\n\n' + f62('C', 'Cronograma 3')
   + '\n\nLas dos salidas son siempre complementarias salvo en las bandas grises, donde ninguna de las dos tiene un valor utilizable.')

# ================================================================ 6.3 R-S por nivel
def level_rs(g_active_high, kind='rs', X=X36, Y=Y36, CK=CK36):
    inp = [(int(x), int(y), int(c) if g_active_high else 1 - int(c)) for x, y, c in zip(X, Y, CK)]
    return simulate(latch_step(kind), LATCH_INIT, inp, [2, 3], jk_race if kind == 'jk' else (lambda i: False)), inp
(qNA, qbNA), inA = level_rs(True); (qNB, qbNB), inB = level_rs(False)
e63A = '0' * 12 + '1111' + 'xxxx' + '1111' + 'xxxx' + '0' * 8; e63B = '0' * 11 + '1' * 15 + '0' * 10
check('lb6.p63', qNA == e63A and qNB == e63B, (qNA, qNB))
pNA = marks(X36, Y36, CK36); pNB = marks(X36, Y36, inv(CK36))
R['p63'] = dict(NA=qNA, NB=qNB)
ej('lb6-3', 'R‑S síncrona por nivel alto y por nivel bajo', 'Libro · Cap. 6 · P6.3', 'biestable,rs,nivel,cronograma', 'lb6.p63',
   'Completa el cronograma de dos biestables R‑S síncronos: $Q_{NA}$, activo con el reloj a nivel alto, y $Q_{NB}$, activo con el reloj a nivel bajo.\n\n' + cron([['Ck', CK36], ['S', X36], ['R', Y36]], 'Entradas'),
   '**Un síncrono por nivel es un asíncrono con una puerta que se abre y se cierra.** Mientras el reloj está en su nivel activo, S y R actúan como en la báscula asíncrona; fuera de él, la salida se mantiene. Se usa la realización clásica con NAND: con $S=R=1$ activos las dos salidas valen 1 (prohibido).',
   [('Nivel alto ($Q_{NA}$)', 'Primer pulso: $S=0$, $R=0$, se mantiene (0). Segundo pulso: S pasa a 1 y R a 1 un poco después: primero Q=1 y luego **prohibido** (trazo grueso). Al bajar el reloj, la puerta se cierra con $S=R=1$: las dos salidas quedan desconocidas (gris). El tercer pulso empieza con $S=1$, $R=0$: Q=1; de nuevo R sube y sale otra prohibida, que al cerrar el reloj deja otra vez la salida desconocida. En el cuarto pulso $S=0$, $R=1$ y Q se pone a 0.'),
    ('Nivel bajo ($Q_{NB}$)', 'Es lo mismo con el reloj invertido. Q pasa a 1 cuando $S=1$ y $R=0$ con el reloj a nivel bajo. Cuando R sube aparece una prohibida breve (las dos salidas a 1) que se deshace por un solo lado (R baja) y Q sigue en 1. Después, con el reloj bajo, vuelve a haber $S=R=1$, y termina por un solo lado (cae S): Q pasa a 0 sin ambigüedad. Como las dos prohibidas **terminan por un solo lado**, la salida no queda desconocida.'),
    ('Qué enseña', 'Añadir sincronismo por nivel a un R‑S no lo mejora, lo empeora: hay más ocasiones de situaciones prohibidas y de indeterminación a la salida.')],
   cron([['Ck', CK36], ['S', X36], ['R', Y36], ['Q_NA', qNA, pNA], ['Q_NB', qNB, pNB]], 'R‑S por nivel', 34, w=10)
   + '\n\nTrazo grueso: entrada prohibida con la puerta abierta. Gris claro: salida desconocida a priori.')

# ================================================================ 6.4 R-S por flanco
qUp = edge_ff('rs', CK36, X36, Y36, 'r'); qDn = edge_ff('rs', CK36, X36, Y36, 'f')
check('lb6.p64', qUp == '0' * 12 + '1' * 16 + '0' * 8 and qDn == '0' * 16 + 'x' * 16 + '0' * 4, (qUp, qDn))
R['p64'] = dict(up=qUp, dn=qDn)
ej('lb6-4', 'R‑S síncrona por flanco ascendente y por flanco descendente', 'Libro · Cap. 6 · P6.4', 'biestable,rs,flanco,cronograma', 'lb6.p64',
   'Con las mismas entradas que el problema anterior, completa el cronograma de dos biestables R‑S síncronos por flanco: $Q_\\uparrow$ (flanco de subida) y $Q_\\downarrow$ (flanco de bajada).',
   '**En un flanco solo importa una cosa:** el valor de $S$ y $R$ justo antes de él. Si es $00$, mantiene; $10$ pone a 1; $01$ pone a 0; $11$ deja la salida **desconocida** hasta el siguiente flanco que dé una orden clara.',
   [('Flanco de subida', 'Los cuatro flancos de subida encuentran $SR=00$ (mantiene), $10$ (pone a 1), $10$ (sigue a 1) y $01$ (pone a 0). Ninguno coincide con $11$, así que la evolución es normal.'),
    ('Flanco de bajada', 'Los cuatro flancos de bajada encuentran $SR=00$ (mantiene), $11$, $11$ y $01$. Con el primer $11$ la salida queda desconocida y con el segundo sigue desconocida; solo se aclara con el último flanco, que trae $S=0$, $R=1$ y pone Q a 0.'),
    ('Qué enseña', 'Al añadir el sincronismo por flanco a un R‑S, toda situación prohibida genera directamente una salida indeterminada. El sincronismo ha **degradado** al R‑S.')],
   cron([['Ck', CK36], ['S', X36], ['R', Y36], ['Q↑', qUp], ['Q↓', qDn]], 'R‑S por flanco', 34, w=10)
   + '\n\nGris claro: salida desconocida a priori. Los flancos de bajada de este ejemplo son justo los que caen sobre $SR=11$.')

# ================================================================ 6.5 J-K por nivel
(jNA, jbNA), _ = level_rs(True, 'jk'); (jNB, jbNB), _ = level_rs(False, 'jk')
e65A = '0' * 12 + '1' + 'rrr' + 'xxxx' + '11' + 'rr' + 'xxxx' + '0' * 8
e65B = '0' * 11 + '1' * 5 + 'rr' + '1' * 6 + 'rr' + '0' * 10
check('lb6.p65', jNA == e65A and jNB == e65B, (jNA, jNB))
R['p65'] = dict(NA=jNA, NB=jNB)
ej('lb6-5', 'J‑K síncrona por nivel alto y por nivel bajo', 'Libro · Cap. 6 · P6.5', 'biestable,jk,nivel,cronograma', 'lb6.p65',
   'Con las mismas entradas ($J$ en lugar de $S$ y $K$ en lugar de $R$), completa el cronograma de dos J‑K síncronos por nivel: $Q_{NA}$ (nivel alto) y $Q_{NB}$ (nivel bajo).\n\n' + cron([['Ck', CK36], ['J', X36], ['K', Y36]], 'Entradas'),
   '**$JK=11$ ya no es «prohibida» sino «bascula».** Pero si el nivel activo dura más que el retardo de las puertas, la salida cambia más de una vez: carrera. Al terminar el nivel, la salida queda parada en un valor imposible de predecir.',
   [('Nivel alto ($Q_{NA}$)', 'Con $J=1$, $K=0$ al principio del segundo pulso, Q pasa a 1; cuando K sube se da $JK=11$ con el reloj alto: **carrera** durante el resto del nivel; al bajar el reloj, la salida queda desconocida. En el siguiente pulso, $J=1$, $K=0$ pone Q a 1 de forma determinista y poco después K sube otra vez: otra carrera y otra indeterminación. Al final, con $J=0$, $K=1$, Q a 0.'),
    ('Nivel bajo ($Q_{NB}$)', 'La primera vez que coinciden $J=K=1$ con el reloj bajo (carrera breve) se sale con $J=1$, $K=0$ y Q queda a 1. La segunda vez termina con $J=0$, $K=1$ y Q se pone a 0: las dos carreras se resuelven por un solo lado.'),
    ('Qué enseña', 'Igual que con el R‑S, el sincronismo por nivel degrada al J‑K: aparece la indeterminación con mucha más facilidad.')],
   cron([['Ck', CK36], ['J', X36], ['K', Y36], ['Q_NA', jNA], ['Q_NB', jNB]], 'J‑K por nivel', 34, w=10)
   + '\n\nGris oscuro: carreras. Gris claro: salida desconocida a priori.')

# ================================================================ 6.6 J-K por flanco
jUp = edge_ff('jk', CK36, X36, Y36, 'r'); jDn = edge_ff('jk', CK36, X36, Y36, 'f')
check('lb6.p66', jUp == '0' * 12 + '1' * 16 + '0' * 8 and jDn == '0' * 16 + '1' * 8 + '0' * 12 and 'x' not in jUp + jDn, (jUp, jDn))
R['p66'] = dict(up=jUp, dn=jDn)
book('lb6.p66.ojo', False, 'el comentario del libro dice «J-K síncrono por nivel» donde quiere decir por flanco')
ej('lb6-6', 'J‑K síncrona por flanco ascendente y descendente', 'Libro · Cap. 6 · P6.6', 'biestable,jk,flanco,cronograma', 'lb6.p66',
   'Completa el cronograma de dos J‑K síncronos por flanco: $Q_\\uparrow$ (flanco de subida) y $Q_\\downarrow$ (flanco de bajada), con las mismas entradas que el problema anterior.',
   '**Un flanco es un instante, y un instante no puede tener carrera.** En cada flanco se mira $JK$ y se aplica la tabla (00 mantiene, 10 pone a 1, 01 pone a 0, 11 invierte). Entre flancos, la salida no se entera de nada.',
   [('Flanco de subida', 'Los cuatro flancos de subida encuentran $JK=00$, $10$, $10$ y $01$: nada, Q a 1, Q sigue a 1 y Q a 0. La salida sube en el primer flanco con $J=1$ y baja en el último.'),
    ('Flanco de bajada', 'Aquí llegan $JK=00$, $11$, $11$ y $01$: nada, **inversión** (Q pasa a 1), **inversión** (Q vuelve a 0, de ahí el pulso corto) y 0. Es la única vez en el capítulo en que el $11$ hace algo con sentido.'),
    ('Qué enseña', 'El sincronismo por flanco le ha sentado bien al J‑K: **no hay carreras ni indeterminaciones**, solo una inversión por flanco con $JK=11$. Es el J‑K que se usa en la práctica; el R‑S y el J‑K por nivel y el R‑S por flanco solo tienen interés teórico.')],
   cron([['Ck', CK36], ['J', X36], ['K', Y36], ['Q↑', jUp], ['Q↓', jDn]], 'J‑K por flanco', 34, w=10)
   + ojo('El primer comentario del libro afirma que «el J‑K síncrono por nivel no presenta situaciones ni de carreras ni indeterminadas». Es al revés: el J‑K por nivel del problema anterior sí las presenta; lo que no las tiene es el J‑K **por flanco**. Es una errata de palabra.'))

# ================================================================ 6.7 maestro/esclavo
CK67 = runs([(0, 4)] + [(1, 4), (0, 4)] * 5); J67 = runs([(0, 5), (1, 12), (0, 9), (1, 18)]); K67 = runs([(0, 19), (1, 19), (0, 6)])
assert len(CK67) == len(J67) == len(K67) == 44
qmA, qsA = ms_sim('jk', 'A', J67, K67, CK67); qmB, qsB = ms_sim('jk', 'B', J67, K67, CK67)
eA = edge_ff('jk', CK67, J67, K67, 'f'); eB = edge_ff('jk', CK67, J67, K67, 'r')
e_qmA = '0' * 5 + '1' * 15 + '0' * 8 + '1' * 8 + '0' * 8; e_qsA = '0' * 8 + '1' * 16 + '0' * 8 + '1' * 8 + '0' * 4
e_qmB = '0' * 8 + '1' * 11 + '0' * 7 + '1' * 6 + '0' * 8 + '1' * 4; e_qsB = '0' * 12 + '1' * 8 + '0' * 8 + '1' * 8 + '0' * 8
dif = [i for i in range(44) if qsA[i] != eA[i]]
check('lb6.p67', (qmA, qsA, qmB, qsB) == (e_qmA, e_qsA, e_qmB, e_qsB), (qmA, qsA, qmB, qsB))
check('lb6.p67.eq_flanco', qsB == eB and dif and dif[0] == 40 and all(qsA[i] == eA[i] for i in range(40)), dif)
R['p67'] = dict(A=[qmA, qsA, eA], B=[qmB, qsB, eB])
ej('lb6-7', 'Maestro/esclavo J‑K en sus dos versiones', 'Libro · Cap. 6 · P6.7', 'biestable,jk,maestro-esclavo,cronograma', 'lb6.p67',
   'Completa el cronograma de dos biestables J‑K maestro/esclavo. En el primero (versión A) el maestro es activo con el reloj a nivel alto y el esclavo a nivel bajo; en el segundo (versión B), al revés.\n\n'
   'El maestro es un R‑S síncrono por nivel cuyas entradas son $S_M=J\\cdot\\overline{Q_S}$ y $R_M=K\\cdot Q_S$; el esclavo es otro R‑S síncrono por nivel, con el nivel contrario, cuyas entradas son $S_S=Q_M$ y $R_S=\\overline{Q_M}$. La salida del conjunto es $Q_S$.\n\n'
   + cron([['Ck', CK67], ['J', J67], ['K', K67]], 'Entradas', 34, w=9),
   '**El maestro piensa y el esclavo copia.** En cada semiperíodo solo uno de los dos está abierto: mientras el maestro mira a J y K, el esclavo duerme, y al revés. Las dos tareas se separan en el tiempo, y por eso no hay carreras ni indeterminaciones.',
   [('Qué hace el maestro', 'Con $JK=00$ mantiene $Q_M$. Con $JK=11$ **toma el opuesto del esclavo**: $Q_M=\\overline{Q_S}$ (por eso se realimenta $Q_S$). Con $10$ y $01$ se pone a 1 o a 0 si el esclavo no lo tiene ya así.'),
    ('Versión A', 'El maestro mira durante el nivel alto; el esclavo copia durante el nivel bajo siguiente. $Q_M$ sube en el primer pulso (con $J=1$), el esclavo lo copia al bajar el reloj, $Q_M$ baja con $K=1$, el esclavo lo copia, etc. La salida $Q_S$ cambia en los flancos de bajada.'),
    ('Versión B', 'Igual con los niveles intercambiados. La salida $Q_S$ cambia en los flancos de subida y es **idéntica** a la de un J‑K por flanco ascendente. En el dibujo se ha superpuesto $Q_\\uparrow$ para comprobarlo.'),
    ('El caso difícil', 'En el último pulso alto de la versión A cambian J y K **durante el nivel activo del maestro**: primero $JK=11$ (el maestro toma el opuesto de $Q_S=1$, es decir, 0) y luego $JK=10$. Con $JK=10$: $S_M=1\\cdot\\overline{Q_S}=0$ y $R_M=0\\cdot Q_S=0$, el maestro **mantiene su 0**, y por eso $Q_S$ copia 0, no 1. Un J‑K por flanco de bajada habría visto $JK=10$ en el flanco y habría puesto 1: ahí **no coinciden**. La equivalencia M/S ≡ J‑K por flanco solo es obligada si J y K no cambian durante el nivel activo del maestro.')],
   cron([['Ck', CK67], ['J', J67], ['K', K67], ['Q_M (A)', qmA], ['Q_S (A)', qsA], ['Q↓ (J‑K)', eA], ['Q_M (B)', qmB], ['Q_S (B)', qsB], ['Q↑ (J‑K)', eB]], 'Maestro/esclavo', 30, w=9)
   + '\n\nLa salida del conjunto es la del esclavo. En la versión A, $Q_S$ y $Q_\\downarrow$ solo difieren en el último tramo (el caso difícil); en la versión B coinciden siempre.')

# ================================================================ 6.8 maestro/esclavo, dos entradas
CK68 = runs([(0, 2), (1, 4), (0, 4), (1, 4), (0, 4), (1, 4), (0, 5), (1, 5)])
J68a = runs([(1, 4), (0, 8), (1, 9), (0, 4), (1, 4), (0, 3)]); K68a = runs([(0, 12), (1, 9), (0, 11)])
J68b = runs([(1, 9), (0, 16), (1, 1), (0, 6)]); K68b = runs([(0, 9), (1, 12), (0, 2), (1, 5), (0, 4)])
assert all(len(s) == 32 for s in (CK68, J68a, K68a, J68b, K68b))
m1, s1 = ms_sim('jk', 'B', J68a, K68a, CK68); u1 = edge_ff('jk', CK68, J68a, K68a, 'r')
m2, s2 = ms_sim('jk', 'A', J68b, K68b, CK68); d2 = edge_ff('jk', CK68, J68b, K68b, 'f')
check('lb6.p68', m1 == '1' * 14 + '0' * 11 + '1' * 7 and s1 == '00' + '1' * 16 + '0' * 9 + '1' * 5 and m2 == '00' + '1' * 8 + '0' * 22 and s2 == '0' * 6 + '1' * 8 + '0' * 18, (m1, s1, m2, s2))
check('lb6.p68.equivalencia', s1 == u1 and s2 == d2, (u1, d2))
R['p68'] = dict(a=[m1, s1, u1], b=[m2, s2, d2])
ej('lb6-8', 'Dos maestros/esclavos J‑K y sus equivalentes por flanco', 'Libro · Cap. 6 · P6.8', 'biestable,jk,maestro-esclavo,cronograma', 'lb6.p68',
   'Completa los dos cronogramas con cuidado. En el primero el maestro es activo con el reloj a nivel bajo y el esclavo a nivel alto; en el segundo, al revés. Añade en cada uno la salida del J‑K síncrono por flanco que corresponda.\n\n'
   + cron([['Ck', CK68], ['J', J68a], ['K', K68a]], 'Cronograma 1: entradas', 34, w=10) + '\n\n' + cron([['Ck', CK68], ['J', J68b], ['K', K68b]], 'Cronograma 2: entradas', 34, w=10),
   '**Hay que ir paso a paso** porque el maestro depende de la salida del esclavo y el esclavo del maestro: $S_M=J\\overline{Q_S}$, $R_M=K\\,Q_S$. No se resuelve primero todo el maestro y luego todo el esclavo, sino a la vez, semiperíodo a semiperíodo.',
   [('Cronograma 1', 'El maestro (nivel bajo) ve a $J=1$ al principio y pone $Q_M=1$; el esclavo lo copia en el primer nivel alto. Con $JK=11$ en el nivel bajo siguiente, el maestro toma el opuesto del esclavo (0), y el esclavo lo copia después. Luego queda a 0 hasta que J sube con $K=0$. La salida $Q_S$ cambia **en los flancos de subida**.'),
    ('Cronograma 2', 'Maestro de nivel alto. Pone $Q_M=1$ mientras J vale 1 y K 0, y se pone a 0 cuando K sube. El esclavo copia en el nivel bajo siguiente; los pequeños pulsos de J y K que caen con el maestro cerrado no tienen ningún efecto. $Q_S$ cambia **en los flancos de bajada**.'),
    ('Equivalencias', 'Un maestro/esclavo con maestro de nivel bajo equivale a un J‑K por flanco ascendente, y con maestro de nivel alto a un J‑K por flanco descendente: en los dos cronogramas la salida del esclavo y la del J‑K por flanco coinciden. Pero eso solo vale mientras J y K no cambien durante el nivel activo del maestro.')],
   cron([['Ck', CK68], ['J', J68a], ['K', K68a], ['Q_M', m1], ['Q_S', s1], ['Q↑', u1]], 'Cronograma 1: maestro bajo, esclavo alto', 34, w=10) + '\n\n'
   + cron([['Ck', CK68], ['J', J68b], ['K', K68b], ['Q_M', m2], ['Q_S', s2], ['Q↓', d2]], 'Cronograma 2: maestro alto, esclavo bajo', 34, w=10))

# ================================================================ 6.9 D por flanco y latch
CK69 = runs([(0, 4)] + [(1, 4), (0, 4)] * 6)
D69 = runs([(0, 6), (1, 8), (0, 5), (1, 3), (0, 4), (1, 8), (0, 3), (1, 2), (0, 8), (1, 5)]); assert len(CK69) == len(D69) == 52
dU = edge_ff('d', CK69, D69, '', 'r'); dD = edge_ff('d', CK69, D69, '', 'f')
EN = runs([(0, 3), (1, 10), (0, 13), (1, 7), (0, 6), (1, 10)])
D2 = runs([(1, 3), (0, 2), (1, 2), (0, 1), (1, 3), (0, 2), (1, 3), (0, 2), (1, 3), (0, 2), (1, 3), (0, 2), (1, 2), (0, 1), (1, 2),
           (0, 2), (1, 2), (0, 1), (1, 1), (0, 2), (1, 2), (0, 1), (1, 3), (0, 1), (1, 1)]); assert len(EN) == len(D2) == 49, (len(EN), len(D2))
qL = ''; hold = '0'
for e, d in zip(EN, D2):
    if e == '1': hold = d
    qL += hold
gl, _ = simulate(latch_step('rs'), LATCH_INIT, [(int(d), 1 - int(d), int(e)) for d, e in zip(D2, EN)], [2, 3])
check('lb6.p69', dU == '0' * 12 + '1' * 24 + '0' * 16 and dD == '0' * 8 + '1' * 8 + '0' * 16 + '1' * 8 + '0' * 8 + '1' * 4 and qL == gl, (dU, dD, qL, gl))
check('lb6.p69.sin_indeterminacion', 'x' not in dU + dD + qL)
R['p69'] = dict(up=dU, dn=dD, latch=qL)
ej('lb6-9', 'Báscula D por flanco y latch D por nivel', 'Libro · Cap. 6 · P6.9', 'biestable,d,latch,cronograma', 'lb6.p69',
   'Completa los cronogramas de una báscula D síncrona por flanco (de subida, $Q_\\uparrow$, y de bajada, $Q_\\downarrow$) y de una báscula D síncrona por nivel (un latch o cerrojo, $Q_{NA}$) cuya señal de reloj es una línea ENABLE aperiódica.\n\n'
   + cron([['Ck', CK69], ['D', D69]], 'Por flanco: entradas', 30, w=7) + '\n\n' + cron([['Enable', EN], ['D', D2]], 'Latch: entradas', 30, w=7),
   '**Una báscula D no puede tener situaciones prohibidas ni indeterminadas** sea cual sea el sincronismo: solo tiene una entrada. Por flanco copia a D en ese instante; por nivel copia a D mientras esté abierta y lo guarda cuando se cierra.',
   [('Por flanco', 'Se anota el valor de D justo antes de cada flanco: en $Q_\\uparrow$ sale 0, 1, 1, 1, **0** (D baja justo antes del quinto flanco) y 0; en $Q_\\downarrow$ sale 1, 0, 0, 1, 0, 1. Los cambios de D entre flancos no se ven.'),
    ('Latch', 'Mientras ENABLE vale 1 la salida **sigue** a D, con todos sus pulsos cortos; cuando ENABLE baja, la salida se queda con el último valor de D. Se parece a la anterior solo en el nombre: aquí cada glitch de D con ENABLE alto llega a la salida.'),
    ('Comprobación', 'El latch D se simuló también como un R‑S con puertas NAND con $S=D$, $R=\\overline D$ y una puerta de habilitación: da la misma salida. Y no hay indeterminaciones, porque $S$ y $R$ nunca valen 1 a la vez.')],
   cron([['Ck', CK69], ['D', D69], ['Q↑', dU], ['Q↓', dD]], 'D por flanco', 30, w=7) + '\n\n' + cron([['Enable', EN], ['D', D2], ['Q_NA', qL]], 'Latch D (ENABLE aperiódica)', 30, w=7)
   + '\n\nUna línea ENABLE aperiódica y no un reloj: por eso se habla de latch o cerrojo, y no de biestable.')

# ================================================================ 6.10 R-S y J-K, todos los tipos
CK610 = runs([(0, 2), (1, 4), (0, 4), (1, 4), (0, 4), (1, 4), (0, 5), (1, 5)])
JS = runs([(1, 8), (0, 17), (1, 3), (0, 4)]); KR = runs([(0, 8), (1, 11), (0, 2), (1, 5), (0, 6)])
assert len(CK610) == len(JS) == len(KR) == 32
(jna, _), _ = level_rs(True, 'jk', JS, KR, CK610); (jnb, _), _ = level_rs(False, 'jk', JS, KR, CK610)
jup = edge_ff('jk', CK610, JS, KR, 'r'); jdn = edge_ff('jk', CK610, JS, KR, 'f')
(rna, _), _ = level_rs(True, 'rs', JS, KR, CK610); (rnb, _), _ = level_rs(False, 'rs', JS, KR, CK610)
rup = edge_ff('rs', CK610, JS, KR, 'r'); rdn = edge_ff('rs', CK610, JS, KR, 'f')
mA, sA = ms_sim('rs', 'A', JS, KR, CK610); mB, sB = ms_sim('rs', 'B', JS, KR, CK610)
e_a = '0' * 2 + '1' * 8 + '0' * 17 + '1' * 5
check('lb6.p610', jna == e_a and jnb == '1' * 8 + '0' * 17 + 'r' + '1' * 6 and jup == e_a and jdn == '0' * 6 + '1' * 8 + '0' * 18
      and rna == e_a and rnb == '1' * 8 + '0' * 17 + '1' * 7 and rup == e_a and rdn == jdn and sA == rdn and sB == rup, (jna, jnb, jup, jdn, rna, rnb, rup, rdn, sA, sB))
R['p610'] = dict(jk=[jna, jnb, jup, jdn], rs=[rna, rnb, sA, rdn, sB, rup])
p610 = marks(JS, KR, inv(CK610))
ej('lb6-10', 'Un mismo cronograma para J‑K y para R‑S de todos los sincronismos', 'Libro · Cap. 6 · P6.10', 'biestable,jk,rs,cronograma', 'lb6.p610',
   'Completa el cronograma dado. Las dos entradas se aplican a un J‑K (J, K) y a un R‑S (S=J, R=K). Para cada uno hay que dibujar la salida de las versiones por nivel alto ($Q_{NA}$), por nivel bajo ($Q_{NB}$), por flanco de subida ($Q_\\uparrow$) y por flanco de bajada ($Q_\\downarrow$); en el R‑S, además, las de maestro/esclavo con maestro a nivel alto ($Q_{MS(NA)}$) y bajo ($Q_{MS(NB)}$).\n\n' + cron([['Ck', CK610], ['J ó S', JS], ['K ó R', KR]], 'Entradas', 34, w=10),
   '**Es el mismo método ocho veces.** Para cada dispositivo se aplica la regla que corresponde: por nivel, lo que valgan las entradas mientras esté abierto; por flanco, lo que valgan justo antes del flanco; maestro/esclavo, el nivel activo del maestro y luego la copia del esclavo.',
   [('J‑K', 'Solo coinciden $J=K=1$ una vez, con el reloj a nivel bajo: el J‑K de nivel bajo entra en carrera una ranura (de ahí la banda oscura) y, como J se queda en 1 después, se resuelve poniéndose a 1. Los demás dispositivos no ven nunca $JK=11$.'),
    ('R‑S', 'La misma situación $S=R=1$ con el R‑S de nivel bajo es una combinación prohibida (las dos salidas valen 1) y también se sale por un solo lado: Q queda a 1 sin ambigüedad, igual que en el J‑K. El resto de dispositivos coincide con sus equivalentes de J‑K.'),
    ('Equivalencias', 'La salida del R‑S maestro/esclavo con maestro a nivel alto coincide con la del R‑S por flanco de bajada ($Q_\\downarrow$), y con maestro a nivel bajo con la de flanco de subida ($Q_\\uparrow$). Las versiones por nivel alto de J‑K y R‑S coinciden aquí con $Q_\\uparrow$ de J‑K porque en los niveles altos no se dan ni $JK=11$ ni $SR=11$.')],
   cron([['Ck', CK610], ['J ó S', JS], ['K ó R', KR], ['JK Q_NA', jna], ['JK Q_NB', jnb], ['JK Q↑', jup], ['JK Q↓', jdn], ['RS Q_NA', rna], ['RS Q_NB', rnb, p610], ['RS Q_MS(NA)', sA], ['RS Q↓', rdn], ['RS Q_MS(NB)', sB], ['RS Q↑', rup]], 'Todos los sincronismos', 28, w=10)
   + '\n\nGris oscuro: carreras. Trazo grueso: entrada prohibida. Los R‑S maestro/esclavo y por flanco dan la misma salida cuando las entradas no cambian durante el nivel activo del maestro.')

# ================================================================ 6.11 R-S y J-K con carreras e indeterminaciones
CK611 = runs([(0, 2), (1, 4), (0, 4), (1, 4), (0, 4), (1, 4), (0, 4), (1, 4)])
JS11 = runs([(0, 12), (1, 8), (0, 4), (1, 3), (0, 3)]); KR11 = runs([(0, 2), (1, 6), (0, 4), (1, 4), (0, 6), (1, 7), (0, 1)])
assert len(CK611) == len(JS11) == len(KR11) == 30
(rA, _), _ = level_rs(True, 'rs', JS11, KR11, CK611); (rB, _), _ = level_rs(False, 'rs', JS11, KR11, CK611)
(kA, _), _ = level_rs(True, 'jk', JS11, KR11, CK611); (kB, _), _ = level_rs(False, 'jk', JS11, KR11, CK611)
rU = edge_ff('rs', CK611, JS11, KR11, 'r'); rD = edge_ff('rs', CK611, JS11, KR11, 'f'); kU = edge_ff('jk', CK611, JS11, KR11, 'r')
check('lb6.p611', rA == '0' * 12 + '11' + 'xxxx' + '1' * 8 + '1' + '000' and rB == '0' * 14 + '1' * 8 + '00' + '11' + 'xxxx'
      and rU == '0' * 18 + '1' * 8 + 'xxxx' and rD == '0' * 14 + 'x' * 16
      and kA == '0' * 12 + 'rr' + 'xxxx' + '1' * 8 + 'r' + '000' and kB == '0' * 14 + 'rr' + '1' * 6 + '00' + 'rr' + 'xxxx' and kU == '0' * 18 + '1' * 8 + '0' * 4, (rA, rB, rU, rD, kA, kB, kU))
R['p611'] = dict(rs=[rA, rB, rU, rD], jk=[kA, kB, kU])
book('lb6.p611.qna', False, 'en el dibujo del libro la salida del J‑K de nivel alto queda a 1 tras la última carrera; con J=0, K=1 debe bajar a 0')
pr = lambda g: marks(JS11, KR11, g)
ej('lb6-11', 'R‑S y J‑K con prohibidas, carreras e indeterminaciones', 'Libro · Cap. 6 · P6.11', 'biestable,jk,rs,cronograma', 'lb6.p611',
   'Completa el cronograma para biestables R‑S (S=J, R=K) y J‑K. Señala con trazo grueso lo prohibido, con gris oscuro las carreras y con gris claro lo desconocido. Hay que dibujar las salidas de nivel alto ($Q_{NA}$), nivel bajo ($Q_{NB}$), flanco de subida ($Q_\\uparrow$) y, para el R‑S, flanco de bajada ($Q_\\downarrow$).\n\n' + cron([['Ck', CK611], ['J ó S', JS11], ['K ó R', KR11]], 'Entradas', 34, w=10),
   '**Es el cronograma más completo del capítulo:** en él aparecen las prohibidas del R‑S, las carreras del J‑K por nivel y las indeterminaciones de los dos. Se resuelve igual que los anteriores, fila a fila y con cuidado, porque un fallo se arrastra a lo largo de todo el cronograma.',
   [('R‑S por nivel alto', 'En el segundo pulso S y R suben a la vez con el reloj alto: prohibida (las dos salidas a 1). Al cerrarse el reloj con $SR=11$ la salida queda **desconocida**. El tercer pulso trae $S=1$, $R=0$ y Q=1. En el cuarto vuelve a darse $SR=11$ (prohibida) y a continuación $S=0$, $R=1$: Q pasa a 0.'),
    ('R‑S por nivel bajo y por flanco', 'En nivel bajo hay dos prohibidas: la primera se resuelve por un solo lado ($R$ baja y Q sigue en 1); luego, con $S=0$, $R=1$, Q pasa a 0, y viene otra prohibida que, al subir el reloj (la puerta se cierra con $SR=11$), deja la salida desconocida. Por flanco de subida el R‑S queda desconocido solo en el último flanco (llega con $SR=11$); por flanco de bajada, el primer flanco pone Q a 0, el segundo llega con $SR=11$ y la salida ya no se aclara.'),
    ('J‑K', 'Por nivel alto: carrera (J y K suben a la vez), desconocida (el reloj baja), set, carrera breve y reset. Por nivel bajo: carrera, set, reset, carrera y desconocida. Por flanco de subida el J‑K no tiene ningún problema: el flanco que llega con $JK=11$ solo invierte la salida.'),
    ('Qué enseña', 'Con el mismo patrón de entradas, el J‑K por flanco es un dispositivo limpio y todos los demás tienen alguna situación indefinida. El sincronismo por flanco ha degradado al R‑S, pero ha sentado bien al J‑K.')],
   cron([['Ck', CK611], ['J ó S', JS11], ['K ó R', KR11], ['RS Q_NA', rA, pr(CK611)], ['RS Q_NB', rB, pr(inv(CK611))], ['RS Q↑', rU], ['RS Q↓', rD], ['JK Q_NA', kA], ['JK Q_NB', kB], ['JK Q↑', kU]], 'R‑S y J‑K', 28, w=11)
   + '\n\nTrazo grueso: prohibido. Gris oscuro: carreras. Gris claro: valor desconocido a priori.'
   + ojo('En el dibujo del libro, la salida del J‑K de nivel alto ($Q_{NA}$) queda a 1 después de la última carrera, pero ahí $J$ ya vale 0 y $K$ vale 1 con el reloj aún en nivel alto: la salida debe bajar a 0, como en el R‑S. Es un fallo de dibujo.'))

# ================================================================ 6.12 tres circuitos con puertas
def settle_q(f, q0):
    q = q0
    for _ in range(10):
        n = f(q)
        if n == q: return q
        q = n
    return None
def table_q(f):                    # f(q) con las entradas ya fijadas; devuelve 'Qt-1' si depende del valor previo
    a, b = settle_q(f, 0), settle_q(f, 1)
    return 'Q<sub>t-1</sub>' if (a, b) == (0, 1) else a
c1 = lambda A, B: (lambda q: A | ((1 - B) & q)); c2 = lambda A, B: (lambda q: (A & B) | ((1 - A) & q))
c3 = lambda A, B, C: (lambda q: (A & B) | ((1 - A) & q) | ((1 - C) & q))
t1 = [(A, B, table_q(c1(A, B))) for A in (0, 1) for B in (0, 1)]
t2 = [(A, B, table_q(c2(A, B))) for A in (0, 1) for B in (0, 1)]
t3 = [(A, B, C, table_q(c3(A, B, C))) for A in (0, 1) for B in (0, 1) for C in (0, 1)]
bk1 = ['Q<sub>t-1</sub>', 0, 1, 1]; bk2 = ['Q<sub>t-1</sub>', 'Q<sub>t-1</sub>', 0, 1]; bk3 = ['Q<sub>t-1</sub>'] * 5 + [0, 1, 1]
check('lb6.p612', [r[2] for r in t1] == bk1 and [r[2] for r in t2] == bk2 and [r[3] for r in t3] == bk3, (t1, t2, t3))
def op(v, hold_if, rows_ok): return v
op1 = ['mantiene', 'puesta a 0', 'puesta a 1', 'prohibida']; op2 = ['mantiene', 'mantiene', 'puesta a 0', 'puesta a 1']
op3 = ['mantiene'] * 5 + ['puesta a 0', 'puesta a 1', 'prohibida']
Qt = lambda v: '$Q_{t-1}$' if isinstance(v, str) else v
book('lb6.p612.o_jk', False, 'el libro dice «R-S o J-K síncrono por nivel» para el circuito 3, pero tiene fila prohibida')
ej('lb6-12', 'Tres circuitos con puertas: ¿qué biestable es?', 'Libro · Cap. 6 · P6.12', 'biestable,analisis', 'lb6.p612',
   'Completa las tablas de verdad de tres circuitos con puertas y realimentación de la salida. Indica a qué biestable corresponde cada uno y qué señales son $A$, $B$ y $C$.\n\n'
   '- **Circuito 1:** $Q=A+\\overline B\\cdot Q$ (una AND de $\\overline B$ con la propia salida, y una OR con $A$).\n'
   '- **Circuito 2:** $Q=A\\cdot B+\\overline A\\cdot Q$ (una AND de $A$ y $B$, otra de $\\overline A$ con la propia salida, y una OR).\n'
   '- **Circuito 3:** $Q=A\\cdot B+\\overline A\\cdot Q+\\overline C\\cdot Q$ (tres AND y una OR de tres entradas).',
   '**Un circuito con realimentación se analiza poniendo una entrada, siguiendo su efecto y anotando la salida;** si hace falta, se supone un valor inicial para $Q_{t-1}$. Si el resultado depende de él, la operación es de mantenimiento.',
   [('Circuito 1', tab(['A', 'B', 'Q(t)', 'Operación'], [[a, b, Qt(q), o] for (a, b, q), o in zip(t1, op1)]) + '\n\n**R‑S asíncrono**: $A=S$, $B=R$. Con $A=B=1$, la OR da 1: $Q=1$ (prohibida).'),
    ('Circuito 2', tab(['A', 'B', 'Q(t)', 'Operación'], [[a, b, Qt(q), o] for (a, b, q), o in zip(t2, op2)]) + '\n\n**D síncrono por nivel (latch D)**: $A=Ck$ (habilita) y $B=D$. Con $A=0$ mantiene y con $A=1$ copia B.'),
    ('Circuito 3', tab(['A', 'B', 'C', 'Q(t)', 'Operación'], [[a, b, c, Qt(q), o] for (a, b, c, q), o in zip(t3, op3)]) + '\n\n**R‑S síncrono por nivel**: $A=Ck$, $B=S$, $C=R$. La fila $111$ es la prohibida (queda $Q=1$).'),
    ('Comprobación', 'Las tres tablas se han calculado resolviendo la ecuación de cada circuito para $Q_{t-1}=0$ y para $Q_{t-1}=1$: si salen valores distintos la fila es «mantiene».')],
   'Circuito 1: R‑S asíncrono. Circuito 2: latch D. Circuito 3: R‑S síncrono por nivel.'
   + ojo('El libro dice que el circuito 3 es «un biestable R‑S o J‑K síncrono por nivel». Pero su tabla tiene una fila prohibida ($111$, que da $Q=1$), y un J‑K no tiene ninguna combinación prohibida (con $J=K=1$ invertiría la salida). Es un R‑S; la mención al J‑K sobra.'))

# ================================================================ 6.13 dos circuitos con un T y un D
def tff(A, B, q): T = (A & (1 - q)) | (B & q); return q ^ T, T
def dff(A, B, q): D = (A & (1 - q)) | ((1 - B) & q); return D, D
rows13 = [(A, B, q) for A in (0, 1) for B in (0, 1) for q in (0, 1)]
tt = [(A, B, q, *tff(A, B, q)[::-1]) for A, B, q in rows13]      # (A,B,q,T,Q)
dd = [(A, B, q, *dff(A, B, q)[::-1]) for A, B, q in rows13]
jkq = lambda J, K, q: (J & (1 - q)) | ((1 - K) & q)
check('lb6.p613', all(tff(A, B, q)[0] == jkq(A, B, q) and dff(A, B, q)[0] == jkq(A, B, q) for A, B, q in rows13))
bkT = [0, 1, 0, 0, 1, 1, 1, 0]; bkTcol = [0, 0, 0, 1, 1, 0, 1, 1]; bkD = [0, 1, 0, 0, 1, 1, 1, 0]; bkDcol = [0, 0, 0, 0, 1, 1, 1, 0]
check('lb6.p613.libro_T', [r[4] for r in tt] == bkT and [r[3] for r in tt] == bkTcol)
check('lb6.p613.libro_D_q', [r[4] for r in dd] == bkD)
book('lb6.p613.d', [r[3] for r in dd] == bkDcol, 'circuito 2, fila 0 0 1: el libro anota D=0 con Q(t)=1; debe ser D=1')
ej('lb6-13', 'Un T y un D con realimentación: ¿qué biestable resulta?', 'Libro · Cap. 6 · P6.13', 'biestable,analisis,jk', 'lb6.p613',
   'Completa las tablas de verdad de dos circuitos formados por un flip‑flop por flanco de subida, dos AND, una OR y la realimentación de sus salidas. Indica qué biestable resulta y qué señales son $A$ y $B$.\n\n'
   '- **Circuito 1:** un T con $T=A\\cdot\\overline Q+B\\cdot Q$.\n'
   '- **Circuito 2:** un D con $D=A\\cdot\\overline Q+\\overline B\\cdot Q$.',
   '**Basta con excitar el circuito con una entrada y anotar la salida.** Para cada fila ($A$, $B$, $Q_{t-1}$) se calcula la entrada del flip‑flop y, con ella y con la tabla del flip‑flop, la salida tras el flanco.',
   [('Circuito 1', tab(['A', 'B', '$Q_{t-1}$', 'T', 'Q(t)'], [list(r) for r in tt]) + '\n\nT vale 1 cuando $A=1$ y $Q=0$ (hay que subir), o cuando $B=1$ y $Q=1$ (hay que bajar). Con $T=1$ invierte y con $T=0$ mantiene.'),
    ('Circuito 2', tab(['A', 'B', '$Q_{t-1}$', 'D', 'Q(t)'], [list(r) for r in dd]) + '\n\nD vale 1 si hay que subir ($A=1$, $Q=0$) o si hay que mantener a 1 ($B=0$, $Q=1$).'),
    ('Qué biestable es', 'Los dos son un **J‑K por flanco de subida**, con $A=J$ y $B=K$: $Q_t=J\\overline{Q_{t-1}}+\\overline K\\,Q_{t-1}$ en los dos. Un T o un D con dos puertas y realimentación forma un J‑K. Estos circuitos son clásicos en los libros de teoría.'),
    ('Fuera del flanco', 'Con el reloj en nivel alto o bajo (sin flanco de subida) la salida **mantiene** su valor: en las dos tablas del libro la última fila es «todo X, $Q_t=Q_{t-1}$».')],
   'Circuitos 1 y 2: J‑K por flanco de subida, con $A=J$ y $B=K$.'
   + ojo('En la tabla del circuito 2, la fila con $A=0$, $B=0$, $Q_{t-1}=1$ lleva $D=0$ pero $Q(t)=1$, lo que es incoherente: con $B=0$ y $Q=1$ la puerta da $\\overline B\\cdot Q=1$, luego $D=1$.'))

# ================================================================ 6.14 D por flanco con 6 NAND
def d_step(st, inp):
    Q1, Sb, Rb, Q4, Q, Qb = st; Ck, D = inp
    return (nand(Sb, Q4), nand(Ck, Q1), nand(Ck, Sb, Q4), nand(Rb, D), nand(Sb, Qb), nand(Rb, Q))
def d_settle(starts, inp):
    cl = closure(d_step, starts, inp); st = stables(d_step, cl, inp); assert st, inp
    return st
def d_row(states, Ck, D):
    assert len({s for s in states}) == 1, ('indeterminado', states)
    Q1, Sb, Rb, Q4, Q, Qb = next(iter(states)); return (Q1, Q4, Sb, Rb, Q)
rows14 = []; book14 = [(1, 0, 1, 1, 0, 1, 1), (1, 0, 1, 1, 0, 1, 1)]
scen = [(1, 0, 1), (1, 1, 1), (0, 0, 0), (0, 1, 0), (1, 0, 0)]
res14 = []
for D, Qp, Dafter in scen:
    st0 = {(1 - 1, 1, 1, 0, 0, 0)}                        # estado arbitrario; se estabiliza con Ck=0
    st = {(D, 1, 1, 1 - D, Qp, 1 - Qp)}                   # Q1, S̄, R̄, Q4 con Ck=0 y D dados; Q = valor previo
    st = d_settle(st, (0, D)); res14.append(('0', D, Qp, d_row(st, 0, D)))
    st = d_settle(st, (1, D)); res14.append(('↑', D, '', d_row(st, 1, D)))
    st = d_settle(st, (1, Dafter)); res14.append(('1', Dafter, '', d_row(st, 1, Dafter)))
bk14 = [(1, 0, 1, 1, 0), (1, 0, 0, 1, 1), (1, 0, 0, 1, 1), (1, 0, 1, 1, 1), (1, 0, 0, 1, 1), (1, 0, 0, 1, 1),
        (0, 1, 1, 1, 0), (0, 1, 1, 0, 0), (0, 1, 1, 0, 0), (0, 1, 1, 1, 1), (0, 1, 1, 0, 0), (0, 1, 1, 0, 0),
        (1, 0, 1, 1, 0), (1, 0, 0, 1, 1), (1, 1, 0, 1, 1)]
check('lb6.p614', [r[3] for r in res14] == bk14, [r[3] for r in res14])
# el modelo de 6 NAND se comporta como un D por flanco de subida (cambios de una señal cada vez)
random.seed(6)
ck, D, ok = 0, 0, True; st = d_settle({(D, 1, 1, 1 - D, 0, 1)}, (0, D)); qref = 0
for _ in range(3000):
    if random.random() < .5: ck ^= 1; rise = ck == 1
    else: D ^= 1; rise = False
    if rise: qref = D
    st = d_settle(st, (ck, D)); r = d_row(st, ck, D)
    ok &= (r[4] == qref)
check('lb6.p614.es_D_por_flanco', ok)
R['p614'] = [r[3] for r in res14]
tabla14 = tab(['Ck', 'D', '$Q_{t-1}$', 'Q1', 'Q4', '$\\overline S$', '$\\overline R$', 'Q(t)'], [[a, b, c, *d[:4], d[4]] for a, b, c, d in res14])
ej('lb6-14', 'Tabla de verdad de un D por flanco hecho con seis NAND', 'Libro · Cap. 6 · P6.14', 'biestable,d,flanco,analisis', 'lb6.p614',
   'Completa la tabla de verdad de un circuito con seis puertas NAND (1 a 6) que forma un biestable. Se anotan los valores internos $Q_1$ (salida de la 1), $Q_4$ (salida de la 4), $\\overline S$ (salida de la 2) y $\\overline R$ (salida de la 3), y las salidas $Q$ y $\\overline Q$ (puertas 5 y 6).\n\n'
   '- Puertas 1 y 2 forman un primer latch R‑S de NAND: $Q_1=\\overline{\\overline S\\cdot Q_4}$, $\\overline S=\\overline{Ck\\cdot Q_1}$.\n'
   '- Puerta 3: $\\overline R=\\overline{Ck\\cdot\\overline S\\cdot Q_4}$. Puerta 4: $Q_4=\\overline{\\overline R\\cdot D}$.\n'
   '- Puertas 5 y 6 forman el latch de salida: $Q=\\overline{\\overline S\\cdot\\overline Q}$, $\\overline Q=\\overline{\\overline R\\cdot Q}$.',
   '**El circuito es complicado de analizar: solo vale la paciencia y escribir sobre un dibujo.** Hay que empezar por la primera fila y seguir los cambios de entrada junto con sus efectos en la salida. Se puede ver como **tres latches R‑S asíncronos**: (1,2), (3,4) y (5,6).',
   [('Con Ck = 0', 'Las puertas 2 y 3 valen 1 ($\\overline S=\\overline R=1$): el latch de salida mantiene. Q4 = $\\overline D$ y $Q_1=D$ por la puerta 1: el circuito **sigue a D por dentro** pero sin tocar la salida.'),
    ('En el flanco de subida', 'Con $Ck=1$, si $D=1$ ($Q_4=0$, $Q_1=1$): $\\overline S=0$ y $\\overline R=1$: se pone Q a 1. Si $D=0$ ($Q_4=1$, $Q_1=0$): $\\overline S=1$ y $\\overline R=0$: Q a 0. En los dos casos, una de las dos puertas 2 o 3 se activa.'),
    ('Con Ck = 1 después del flanco', 'Si se capturó un 1, $\\overline S=0$ mantiene $Q_1=1$ y **bloquea** a la puerta 3 ($\\overline R$ no puede bajar aunque $Q_4$ cambie). Si se capturó un 0, $\\overline R=0$ fija $Q_4=1$ sea cual sea D. En los dos casos los cambios de D ya no llegan al latch de salida. Por eso el último comportamiento de la tabla es el interesante: D pasa a 0 pero la salida sigue en 1.'),
    ('Tabla', tabla14)],
   'El circuito es un **biestable D síncrono por flanco de subida**: solo captura el valor de D en el flanco; los cambios posteriores de D no llegan a la salida. Hay cinco comportamientos (uno por flanco): los cuatro primeros son los normales; el quinto es el que muestra que el circuito ignora a D después del flanco. Comprobado con 3000 cambios aleatorios de reloj y de D contra un D por flanco ideal.')

# ================================================================ 6.15 detector de flancos
CK615 = ''.join('1' if k >= 2 and (k - 2) % 4 in (0, 1) else '0' for k in range(40))
ENT = runs([(0, 3), (1, 9), (0, 8), (1, 4), (0, 16)]); assert len(CK615) == len(ENT) == 40
Q1 = edge_ff('d', CK615, ENT, '', 'r'); Q2 = edge_ff('d', CK615, Q1, '', 'r')
SAL = ''.join('1' if (a == '0' and b == '1') else '0' for a, b in zip(Q1, Q2))
ups = [k for k in range(1, 40) if SAL[k] == '1' and SAL[k-1] == '0']
dns = [k for k in range(1, 40) if SAL[k] == '0' and SAL[k-1] == '1']
check('lb6.p615', Q1 == '0' * 6 + '1' * 8 + '0' * 8 + '1' * 4 + '0' * 14 and SAL == '0' * 14 + '1111' + '0' * 8 + '1111' + '0' * 10, (Q1, Q2, SAL))
ups = [k for k in range(1, 40) if SAL[k] == '1' and SAL[k-1] == '0']; dns = [k for k in range(1, 40) if SAL[k] == '0' and SAL[k-1] == '1']
check('lb6.p615.un_periodo', len(ups) == 2 and all(d - u == 4 for u, d in zip(ups, dns)))
R['p615'] = dict(Q1=Q1, Q2=Q2, Sal=SAL)
ej('lb6-15', 'Un circuito con dos D: detector de flancos descendentes', 'Libro · Cap. 6 · P6.15', 'biestable,d,aplicacion,cronograma', 'lb6.p615',
   'Completa el cronograma del circuito siguiente y di cuál es su cometido. Son dos biestables D por flanco de subida con el mismo reloj: el primero recibe $Ent$ en D; el segundo recibe $Q_1$ en D; y una puerta AND da la salida $Sal=\\overline{Q_1}\\cdot Q_2$.\n\n' + cron([['Ck', CK615], ['Ent', ENT]], 'Entradas', 34, w=8),
   '**Dos biestables en cadena retrasan la entrada dos relojes:** $Q_1$ es $Ent$ retrasada un flanco y $Q_2$ es $Q_1$ retrasada otro. La salida mira la diferencia entre ellos.',
   [('$Q_1$ y $Q_2$', 'En cada flanco de subida $Q_1$ copia a $Ent$ y $Q_2$ copia el valor **anterior** de $Q_1$. Cada uno repite la entrada con un flanco de reloj de retraso respecto al anterior.'),
    ('La salida', '$Sal=\\overline{Q_1}\\cdot Q_2$ vale 1 solo cuando $Q_1$ ya ha bajado (la entrada fue 0 en el último flanco) pero $Q_2$ aún recuerda un 1: es decir, **justo el periodo de reloj siguiente a que la entrada baje**. Dura exactamente un periodo $T$.'),
    ('Cometido', 'El circuito **detecta los flancos descendentes** de la entrada y los convierte en un pulso de duración $T$ (un periodo de reloj). Un pulso largo de duración $t$ de la entrada se transforma en uno corto de duración $T$. El pulso de salida se da cuando la entrada baja a 0, no cuando sube.'),
    ('Variante', 'Para detectar flancos **ascendentes** (pulso al principio) basta con usar $Sal=Q_1\\cdot\\overline{Q_2}$ (se toma $Q_1$ y $\\overline{Q_2}$ en la puerta).')],
   cron([['Ck', CK615], ['Ent', ENT], ['Q1', Q1], ['Q2', Q2], ['Sal', SAL]], 'Detector de flanco descendente', 34, w=8)
   + '\n\nSal vale 1 durante exactamente un periodo de reloj tras cada flanco descendente de Ent.')

# ---------------------------------------------------------------- SALIDA
def finish():
    open(os.path.join(ROOT, 'src', 'libro6.dsl'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    bad = [c for c in CHK if not c['ok']]
    json.dump({'R': R, 'CHK': CHK}, open(os.path.join(ROOT, 'out', 'results12.json'), 'w'), ensure_ascii=False)
    print(len(CHK), 'checks;', len(bad), 'fallos;', len(DIFF), 'diferencias con el libro')
finish()
