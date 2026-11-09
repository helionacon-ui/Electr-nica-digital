# -*- coding: utf-8 -*-
# ============================================================ 8.1 tres unos seguidos (Mealy)
def runout(M, seq, st=None):
    return [r[2][0] for r in M.run(seq, st)]
def ref_last(pred):
    return lambda bits: int(pred(bits))
M81 = mealy(['E0'], {'Q0': [('0', 'Q0', (0,)), ('1', 'Q1', (0,))], 'Q1': [('0', 'Q0', (0,)), ('1', 'Q2', (0,))], 'Q2': [('0', 'Q0', (0,)), ('1', 'Q2', (1,))]})
def sim_ref(M, ref, n=200, L=60, nb=1):
    for _ in range(n):
        s = stream(L, nb); b = [x[0] for x in s]
        got = runout(M, s)
        exp = [ref(b[:t + 1]) for t in range(L)]
        if got != exp: return False
    return True
check('lb8.p81.referencia', sim_ref(M81, lambda b: int(b[-3:] == [1, 1, 1])))
enc81 = {'Q0': 0, 'Q1': 1, 'Q2': 2}
bk81 = {'J1': 'E0*q0', 'K1': '/E0', 'J0': 'E0*/q1', 'K0': '1'}
res81, mine81, brow81, k81, s81, no81 = diseno('lb8.p81', M81, enc81, 2, 'JK', bk81, ['E0*q1'])
check('lb8.p81.estados_minimos', len(quotient(M81).states) == 3)
ig81 = same_funcs(res81, bk81, M81, 2)
ej('lb8-1', 'Detector de tres unos seguidos (Mealy)', 'Libro · Cap. 8 · P8.1', 'mealy,detector,jk', 'lb8.p81',
   'Diseña un autómata de **Mealy** que vigile una línea serie $E_0$ y ponga su salida a 1 cuando lleguen **tres o más unos consecutivos**: la salida vale 1 en cada uno que completa o prolonga una racha de al menos tres. Impleméntalo con biestables J‑K.',
   '**Un autómata recuerda sólo lo imprescindible del pasado.** Aquí basta saber cuántos unos seguidos acaban de llegar: ninguno, uno, o dos o más. Eso son **tres estados**. Como la salida depende de la entrada actual (el tercer 1 se detecta *al llegar*), es natural un Mealy.',
   [('Estados', '$Q_0$: la racha de unos es de longitud 0. $Q_1$: acaba de llegar un 1. $Q_2$: llevamos dos o más unos seguidos.'),
    ('Transiciones', 'Un 0 rompe la racha desde cualquier estado y devuelve a $Q_0$. Un 1 avanza: $Q_0\\to Q_1\\to Q_2$ y $Q_2$ se queda en $Q_2$. La salida vale 1 sólo en la transición $Q_2\\xrightarrow{1}Q_2$ (es el tercer 1 o posterior). Se permiten solapamientos: 1111 da dos detecciones.'),
    ('Codificación', 'Con tres estados hacen falta dos biestables: $Q_0=00$, $Q_1=01$, $Q_2=10$. El código $11$ no se usa y es indiferente.'),
    ('Tabla de excitación y minimización', 'Para cada fila $(E_0,q_1q_0)$ se anota qué pide cada biestable J‑K según el cambio $q\\to Q$. Minimizando con los códigos libres como indiferentes sale el resultado de abajo.'),
    ('Circuito', 'Dos biestables J‑K con el mismo reloj. $J_1$ es una AND de $E_0$ y $q_0$; $K_1$ es $\\overline{E_0}$ (un inversor); $J_0$ es una AND de $E_0$ y $\\overline{q_1}$; $K_0$ está a nivel alto fijo; la salida es una AND de $E_0$ y $q_1$.')],
   fsmfig(M81, 'Detector de 111 (Mealy). Etiquetas: $E_0$/S')
   + tabs(M81) + '\n\n' + encs(M81, enc81, 2) + '\n\n' + tab(['Función', 'Ecuación'], brow81)
   + '\n\nLas ecuaciones impresas en el libro se han comprobado en **las seis transiciones definidas** y reproducen la tabla. ' + ('Mi propia minimización coincide con ellas término a término.' if ig81 else 'Mi minimización da otras ecuaciones, equivalentes en todas las transiciones que ocurren.') + '\n\n' + pcount([bk81['J1'], bk81['J0'], 'E0*q1', '/E0'])
   + '\n\nSimulación: 200 flujos aleatorios de 60 bits comparados con el modelo «los tres últimos bits son 111»; coinciden en todos.')

# ============================================================ 8.2 tres ceros seguidos (Mealy, J-K y D)
M82 = mealy(['E0'], {'Q0': [('1', 'Q0', (0,)), ('0', 'Q1', (0,))], 'Q1': [('1', 'Q0', (0,)), ('0', 'Q2', (0,))], 'Q2': [('1', 'Q0', (0,)), ('0', 'Q2', (1,))]})
check('lb8.p82.referencia', sim_ref(M82, lambda b: int(b[-3:] == [0, 0, 0])))
enc82 = {'Q0': 0, 'Q1': 1, 'Q2': 2}
bkJ82 = {'J1': '/E0*q0', 'K1': 'E0', 'J0': '/E0*/q1', 'K0': '1'}
bkD82 = {'D1': '/E0*q0 + /E0*q1', 'D0': '/E0*/q1*/q0'}
resj82, minej82, brj82, kj, sj, _ = diseno('lb8.p82', M82, enc82, 2, 'JK', bkJ82, ['/E0*q1'])
resd82, mined82, brd82, kd, sd, _ = diseno('lb8.p82d', M82, enc82, 2, 'D', bkD82, ['/E0*q1'])
ej('lb8-2', 'Detector de tres ceros seguidos (Mealy, con J‑K y con D)', 'Libro · Cap. 8 · P8.2', 'mealy,detector,jk,d', 'lb8.p82',
   'Igual que el problema anterior pero detectando **tres o más ceros seguidos**. Impleméntalo con biestables J‑K y después con biestables D.',
   '**Es el mismo autómata con los papeles de 0 y 1 intercambiados.** Sólo cambian las ecuaciones: donde antes aparecía $E_0$ ahora aparece $\\overline{E_0}$. Lo interesante es comparar las dos tecnologías de biestable.',
   [('Autómata', 'Tres estados que cuentan los ceros seguidos (0, 1, 2 o más). Un 1 devuelve a $Q_0$. La salida es 1 en $Q_2\\xrightarrow{0}Q_2$.'),
    ('Con biestables D', 'Como $D=Q^+$, basta mirar en qué filas el código siguiente tiene cada bit a 1: $D_0$ sólo vale 1 al pasar de $Q_0$ a $Q_1$ con un 0, y $D_1$ vale 1 al ir a $Q_2$.'),
    ('Con biestables J‑K', 'Las ecuaciones tienen más términos de partida (hay dos funciones por biestable) pero se simplifican mucho gracias a los indiferentes: $K_0=1$ siempre.')],
   fsmfig(M82, 'Detector de 000 (Mealy). Etiquetas: $E_0$/S')
   + tabs(M82) + '\n\n**Con biestables J‑K**\n\n' + tab(['Función', 'Ecuación'], brj82)
   + '\n\n**Con biestables D**\n\n' + tab(['Función', 'Ecuación'], brd82)
   + '\n\nAmbos juegos de ecuaciones, los del libro y los míos, se han comprobado contra la tabla. Con D se necesitan dos funciones y con J‑K cuatro, pero las del J‑K son mucho más cortas: es el compromiso habitual (el J‑K simplifica la lógica a cambio de más hilos).')

# ============================================================ 8.3 secuencia 1011 (Mealy)
def trans(M, st, b): return M.nxt(st, (b,))
M83 = mealy(['E0'], {'Q0': [('0', 'Q0', (0,)), ('1', 'Q1', (0,))], 'Q1': [('0', 'Q2', (0,)), ('1', 'Q1', (0,))],
                     'Q2': [('0', 'Q0', (0,)), ('1', 'Q3', (0,))], 'Q3': [('0', 'Q2', (0,)), ('1', 'Q1', (1,))]})
check('lb8.p83.referencia', sim_ref(M83, lambda b: int(b[-4:] == [1, 0, 1, 1])))
enc83 = {'Q0': 0, 'Q1': 1, 'Q2': 2, 'Q3': 3}
bk83 = {'J1': '/E0*q0', 'K1': '/E0*/q0 + E0*q0', 'J0': 'E0', 'K0': '/E0'}
res83, mine83, brow83, *_ = diseno('lb8.p83', M83, enc83, 2, 'JK', bk83, ['E0*q1*q0'])
check('lb8.p83.estados_minimos', len(quotient(M83).states) == 4)
ej('lb8-3', 'Detector de la secuencia 1011 con solapamiento', 'Libro · Cap. 8 · P8.3', 'mealy,detector,jk,secuencia', 'lb8.p83',
   'Diseña un autómata de Mealy que detecte la secuencia **1011** en una línea serie, permitiendo que dos apariciones se solapen (el último 1 de una puede ser el primero de la siguiente).',
   '**Cada estado representa «lo que llevo escrito del patrón»**: nada ($Q_0$), «1» ($Q_1$), «10» ($Q_2$) y «101» ($Q_3$). Lo difícil son las transiciones que *no* avanzan: hay que volver al **sufijo más largo que siga siendo prefijo del patrón**.',
   [('Transiciones que avanzan', '$Q_0\\xrightarrow{1}Q_1$, $Q_1\\xrightarrow{0}Q_2$, $Q_2\\xrightarrow{1}Q_3$ y $Q_3\\xrightarrow{1}$ (se completa 1011: salida 1).'),
    ('Transiciones que retroceden', 'En $Q_1$ («1») un nuevo 1 deja «1»: se queda en $Q_1$. En $Q_2$ («10») un 0 da «100»: sin prefijo útil, a $Q_0$. En $Q_3$ («101») un 0 da «1010» y su sufijo «10» es prefijo del patrón: a $Q_2$. Tras detectar (1011) el último 1 queda como primer 1 de otra posible aparición: a $Q_1$ (solapamiento).'),
    ('Codificación y ecuaciones', 'Cuatro estados, dos biestables, código natural. Al estar los cuatro códigos usados no hay indiferentes por códigos libres.')],
   fsmfig(M83, 'Detector de 1011. Etiquetas: $E_0$/S')
   + tabs(M83) + '\n\n' + tab(['Función', 'Ecuación'], brow83)
   + '\n\nComprobadas las ocho transiciones y simulados 200 flujos aleatorios de 60 bits contra «los cuatro últimos bits son 1011».')

# ============================================================ 8.4 tres iguales seguidos (Mealy, 5 estados)
M84 = mealy(['E0'], {'Q0': [('0', 'Q1', (0,)), ('1', 'Q3', (0,))], 'Q1': [('0', 'Q2', (0,)), ('1', 'Q3', (0,))],
                     'Q2': [('0', 'Q2', (1,)), ('1', 'Q3', (0,))], 'Q3': [('0', 'Q1', (0,)), ('1', 'Q4', (0,))],
                     'Q4': [('0', 'Q1', (0,)), ('1', 'Q4', (1,))]})
check('lb8.p84.referencia', sim_ref(M84, lambda b: int(len(b) >= 3 and b[-1] == b[-2] == b[-3])))
check('lb8.p84.estados_minimos', len(quotient(M84).states) == 5)
enc84 = {'Q0': 0, 'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
bk84 = {'J2': 'E0*q1*q0', 'K2': '/E0', 'J1': 'q0 + E0*/q2', 'K1': 'q0', 'J0': 'E0*/q2 + /E0*/q1', 'K0': '/E0*/q1 + E0*q1'}
res84, mine84, brow84, *_ = diseno('lb8.p84', M84, enc84, 3, 'JK', bk84, ['/E0*q1*/q0 + E0*q2'])
ej('lb8-4', 'Tres bits iguales seguidos, ceros o unos (Mealy, 5 estados)', 'Libro · Cap. 8 · P8.4', 'mealy,detector,jk', 'lb8.p84',
   'Diseña un autómata de Mealy que active su salida cuando en la línea $E_0$ lleguen **tres o más bits iguales seguidos**, sean tres ceros o tres unos.',
   '**Ahora el estado debe recordar dos cosas:** cuál fue el último bit y cuántas veces seguidas se repite. Hay que distinguir «un 0 suelto», «dos ceros», «tres o más ceros» y lo mismo para los unos; pero el primer bit de la secuencia, que aún no tiene antecesor, es el estado inicial $Q_0$. Total: **cinco estados**.',
   [('Estados', '$Q_0$ inicial. $Q_1$: un 0 (racha de ceros de longitud 1). $Q_2$: dos o más ceros. $Q_3$: un 1. $Q_4$: dos o más unos.'),
    ('Transiciones', 'Un bit igual al de la racha la alarga (y si ya era de longitud 2 o más, la salida es 1); un bit distinto empieza una racha nueva de longitud 1 (de $Q_1$, $Q_2$ o $Q_4$ se pasa a $Q_3$ con un 1; de $Q_3$ o $Q_4$ a $Q_1$ con un 0).'),
    ('Tres biestables', 'Cinco estados necesitan $\\lceil\\log_2 5\\rceil=3$ biestables. Los códigos 101, 110 y 111 son indiferentes: eso permite simplificar mucho las ecuaciones.')],
   fsmfig(M84, 'Tres bits iguales seguidos (Mealy)')
   + tabs(M84) + '\n\n' + tab(['Función', 'Ecuación'], brow84)
   + '\n\nSe han comprobado las ecuaciones del libro en las 10 transiciones definidas (las combinaciones con códigos 101‑111 son indiferentes) y se ha simulado contra el modelo «los tres últimos bits son iguales». Reducción de estados: el algoritmo de particiones no fusiona ninguno, así que cinco es el mínimo.')

# ============================================================ 8.5 1111 y 11011 (Mealy y Moore)
def kmp_mealy(pats):
    prefs = {''}
    for p in pats:
        for k in range(1, len(p)): prefs.add(p[:k])
    order = sorted(prefs, key=lambda x: (len(x), x)); nm = {p: 'Q%d' % i for i, p in enumerate(order)}
    rules = {}
    for p in order:
        r = []
        for b in '01':
            s = p + b; o = int(any(s.endswith(q) for q in pats))
            n = max((s[k:] for k in range(len(s) + 1) if s[k:] in prefs), key=len)
            r.append((b, nm[n], (o,)))
        rules[nm[p]] = r
    return FSM(['E0'], list(rules), rules, None, True), nm
M85, nm85 = kmp_mealy(['1111', '11011'])
check('lb8.p85.mealy_ref', sim_ref(M85, lambda b: int(b[-4:] == [1, 1, 1, 1] or b[-5:] == [1, 1, 0, 1, 1])))
M85m, nmm85 = moore_of_mealy(M85)
def sim_ref_moore(M, ref, n=200, L=60):
    for _ in range(n):
        s = stream(L); b = [x[0] for x in s]
        got = [r[2][0] for r in M.run(s)]
        if got != [ref(b[:t + 1]) for t in range(L)]: return False
    return True
check('lb8.p85.moore_ref', sim_ref_moore(M85m, lambda b: int(b[-4:] == [1, 1, 1, 1] or b[-5:] == [1, 1, 0, 1, 1])))
check('lb8.p85.tamanos', (len(M85.states), len(M85m.states), len(quotient(M85m).states)) == (6, 8, 8), str((len(M85.states), len(M85m.states))))
ej('lb8-5', 'Detectar 1111 y 11011 con solapamiento (Moore y Mealy)', 'Libro · Cap. 8 · P8.5', 'mealy,moore,detector,secuencia', 'lb8.p85',
   'Diseña, como autómata de **Mealy** y como autómata de **Moore**, un detector de **dos** secuencias a la vez: 1111 y 11011. Se permite que las apariciones se solapen y que se pase de una secuencia a otra sin volver al principio.',
   '**El estado recuerda el sufijo más largo de lo recibido que todavía puede convertirse en alguna de las dos secuencias.** Los prefijos propios de los patrones son $\\varepsilon$, 1, 11, 111, 110 y 1101: **seis estados**. El Moore necesita dos más porque «detecté ahora» debe vivir en el estado y no en la transición.',
   [('Mealy', 'Se construye por «longest suffix»: desde el prefijo $p$ y la entrada $b$ se forma $pb$; si acaba en algún patrón completo la salida vale 1; el estado siguiente es el sufijo más largo de $pb$ que sea prefijo propio de algún patrón. Por ejemplo, de «111» con un 1 se completa 1111 y queda «111» (solapamiento).'),
    ('Moore', 'Cada estado Mealy se **duplica** si se puede llegar a él tanto con salida 0 como con salida 1. Aquí le pasa a «111» (tras 1111) y a «11» (tras 11011): 6 + 2 = **8 estados**, sin fusiones posibles.'),
    ('Comprobación', 'Ambas máquinas se simulan contra «los cuatro últimos bits son 1111 o los cinco últimos 11011» con 200 flujos aleatorios de 60 bits.')],
   '**Mealy (6 estados)** — estado = sufijo útil\n\n' + tab(['Estado', 'Sufijo'], [[nm85[p], '$\\varepsilon$' if p == '' else p] for p in sorted(nm85, key=lambda x: (len(x), x))])
   + '\n\n' + tabs(M85) + '\n\n**Moore (8 estados)**\n\n' + tabs(M85m)
   + ojo('En el dibujo del libro del Mealy hay una flecha desde $Q_5$ con entrada 1 cuyo destino es ambiguo en la figura (acaba en un nudo de trazos). Por eso aquí se construye el autómata a partir de los sufijos y se verifica por simulación, en lugar de copiar esa flecha. El número de estados (6 y 8) sí coincide con el del libro.'))

# ============================================================ 8.6 última secuencia detectada (Moore)
def build86(fix):
    # estados (salida, contexto de los dos últimos bits)
    sts = [(o, h) for o in (0, 1) for h in ('', '0', '1', '00', '01', '10', '11')]
    names = {}; rules = {}; outs = {}
    def nxt(o, h, b):
        t = h + b
        o2 = 1 if t[-3:] == '010' else 0 if t[-3:] == '110' else o
        return (o2, t[-2:])
    seen = []; todo = [(0, '')]
    while todo:
        s = todo.pop(0)
        if s in seen: continue
        seen.append(s)
        for b in '01':
            n = nxt(s[0], s[1], b)
            if n not in seen: todo.append(n)
    nm = {s: 'Q%d' % k for k, s in enumerate(seen)}
    rules = {nm[s]: [(b, nm[nxt(s[0], s[1], b)]) for b in '01'] for s in seen}
    outs = {nm[s]: (s[0],) for s in seen}
    return FSM(['E0'], [nm[s] for s in seen], rules, outs, False), nm
M86full, nm86 = build86(True)
M86 = quotient(M86full)
def ref86(b):
    o = 0
    for t in range(len(b)):
        w = b[max(0, t - 2):t + 1]
        if w == [0, 1, 0]: o = 1
        elif w == [1, 1, 0]: o = 0
    return o
check('lb8.p86.referencia', sim_ref_moore(M86, ref86))
# autómata tal como se lee en el libro (Q5 con un 0 a Q0)
M86b = moore(['E0'], {'Q0': [('1', 'Q0'), ('0', 'Q1')], 'Q1': [('0', 'Q1'), ('1', 'Q2')], 'Q2': [('1', 'Q0'), ('0', 'Q3')],
                      'Q3': [('0', 'Q3'), ('1', 'Q4')], 'Q4': [('0', 'Q3'), ('1', 'Q5')], 'Q5': [('1', 'Q5'), ('0', 'Q0')]},
             {'Q0': (0,), 'Q1': (0,), 'Q2': (0,), 'Q3': (1,), 'Q4': (1,), 'Q5': (1,)})
M86c = moore(['E0'], dict(M86b.rules, Q5=[('1', 'Q5'), ('0', 'Q1')]), M86b.outs)
seqx = [(0,), (1,), (0,), (1,), (1,), (0,), (1,), (0,)]
okb = [r[2][0] for r in M86b.run(seqx)]; okc = [r[2][0] for r in M86c.run(seqx)]
refx = [ref86([s[0] for s in seqx][:t + 1]) for t in range(len(seqx))]
check('lb8.p86.contraejemplo', okb != refx and okc == refx, '%s %s %s' % (okb, okc, refx))
check('lb8.p86.corregido', sim_ref_moore(M86c, ref86))
book('lb8.p86', False, 'el autómata del libro pierde un 0 aprovechable tras 110 (Q5-0->Q0 en lugar de Q1)')
ej('lb8-6', 'Recordar cuál fue la última secuencia detectada: 010 o 110', 'Libro · Cap. 8 · P8.6', 'moore,mealy,detector,secuencia', 'lb8.p86',
   'Una línea serie $E_0$ puede contener las secuencias 010 y 110. Diseña un autómata cuya salida valga **1 si la última secuencia detectada fue 010** y **0 si fue 110** (al empezar vale 0). Hazlo de Moore y de Mealy.',
   '**La salida es una memoria de un bit** (cuál fue la última detección), y además hay que seguir buscando los patrones en la línea. El estado debe contener ambas cosas: el valor de la salida y la parte útil de los dos últimos bits.',
   [('Modelo de referencia', 'Se parte de un modelo que lleva la salida $o$ y los dos últimos bits: si los tres últimos son 010, $o=1$; si son 110, $o=0$; en otro caso $o$ no cambia.'),
    ('Reducción', 'El modelo tiene 14 estados posibles (2 valores de $o$ por 7 contextos). El algoritmo de equivalencia de estados lo reduce a **%d estados**, que son los de la tabla.' % len(M86.states)),
    ('Cuidado con el solapamiento', 'Después de detectar 110, el 0 final **ya es el primer símbolo** de un posible 010 (110 10 → detecta 010). Un autómata que, tras 110, vuelva al estado de «nada recibido» pierde esa detección.')],
   fsmfig(M86, 'Última secuencia: 010→1, 110→0 (Moore)') + tabs(M86)
   + '\n\nSimulados 200 flujos aleatorios contra el modelo de referencia: coinciden. La versión de Mealy se obtiene con la misma tabla pasando la salida a las transiciones.'
   + ojo('Según se lee en el diagrama del libro, desde el estado que ya había visto 110 con salida 1 (en la figura $Q_5$) el cero final lleva a $Q_0$ («nada»). Con entrada 0 1 0 1 1 0 1 0 el autómata así leído **no** detecta el último 010 (da 0, y debería dar 1), mientras que si ese cero lleva a $Q_1$ («un 0») sí lo detecta. Ambas versiones se han simulado.'))

# ============================================================ 8.7 1010 o 110 con solapamiento (Mealy)
M87 = mealy(['E0'], {'Q0': [('0', 'Q0', (0,)), ('1', 'Q1', (0,))], 'Q1': [('0', 'Q2', (0,)), ('1', 'Q4', (0,))],
                     'Q2': [('0', 'Q0', (0,)), ('1', 'Q3', (0,))], 'Q3': [('0', 'Q2', (1,)), ('1', 'Q4', (0,))],
                     'Q4': [('0', 'Q2', (1,)), ('1', 'Q4', (0,))]})
check('lb8.p87.referencia5', sim_ref(M87, lambda b: int(b[-4:] == [1, 0, 1, 0] or b[-3:] == [1, 1, 0])))
cl87 = M87.classes(); M87r = quotient(M87)
check('lb8.p87.q3_q4', sorted(map(sorted, cl87)) == [['Q0'], ['Q1'], ['Q2'], ['Q3', 'Q4']])
M87r = FSM(['E0'], ['Q0', 'Q1', 'Q2', 'Q3'], {'Q0': [('0', 'Q0', (0,)), ('1', 'Q1', (0,))], 'Q1': [('0', 'Q2', (0,)), ('1', 'Q3', (0,))],
                                              'Q2': [('0', 'Q0', (0,)), ('1', 'Q3', (0,))], 'Q3': [('0', 'Q2', (1,)), ('1', 'Q3', (0,))]}, None, True)
check('lb8.p87.referencia4', sim_ref(M87r, lambda b: int(b[-4:] == [1, 0, 1, 0] or b[-3:] == [1, 1, 0])))
enc87 = {'Q0': 0, 'Q1': 1, 'Q2': 2, 'Q3': 3}
bk87 = {'J1': 'q0', 'K1': '/E0*/q0', 'J0': 'E0', 'K0': '/E0'}
res87, mine87, brow87, *_ = diseno('lb8.p87', M87r, enc87, 2, 'JK', bk87, ['/E0*q1*q0'])
tr = [(1, 0, 1, 0)]
t1 = M87r.run([(b,) for b in (1, 0, 1, 0)]); check('lb8.p87.mano1', t1[-1][1] == 'Q2' and t1[-1][2] == (1,) )
t2 = M87r.run([(b,) for b in (1, 1, 0)]); check('lb8.p87.mano2', t2[-1][2] == (1,))
seq87 = [int(c) for c in '110101000110']
t3 = M87r.run([(b,) for b in seq87]); st87 = ['Q0'] + [x[1] for x in t3]
check('lb8.p87.mano3', st87 == ['Q0', 'Q1', 'Q3', 'Q2', 'Q3', 'Q2', 'Q3', 'Q2', 'Q0', 'Q0', 'Q1', 'Q3', 'Q2'] and sum(x[2][0] for x in t3) == 4, str(st87))
ej('lb8-7', 'Detectar 1010 o 110 y reducir estados (Mealy)', 'Libro · Cap. 8 · P8.7', 'mealy,detector,reduccion', 'lb8.p87',
   'Diseña un autómata de Mealy que detecte las secuencias **1010** y **110** con solapamiento. Después comprueba si se pueden **fusionar estados** y analiza a mano el comportamiento con las entradas 1010, 110 y 110101000110.',
   '**El primer diseño es el de los sufijos útiles**, y sale con cinco estados. La pregunta clave es si dos estados son **equivalentes**: mismas salidas y, para cada entrada, siguientes equivalentes. Si lo son, se fusionan sin cambiar el comportamiento externo.',
   [('Cinco estados', '$Q_0$ ($\\varepsilon$), $Q_1$ (1), $Q_2$ (10), $Q_3$ (101) y $Q_4$ (11). En $Q_3$ y en $Q_4$ un 0 da salida 1 y lleva a $Q_2$ (1010 o 110); y con un 1 los dos van a $Q_4$.'),
    ('Fusión', '$Q_3$ y $Q_4$ **son equivalentes**: ante un 0 ambos emiten 1 y pasan a $Q_2$; ante un 1 ambos emiten 0 y pasan a $Q_4$ (equivalente a sí mismo). El algoritmo de particiones lo confirma. Queda un autómata de **cuatro estados**, con dos biestables.'),
    ('Análisis a mano', 'Con 1010 el autómata recorre $Q_0\\to Q_1\\to Q_2\\to Q_3\\to Q_2$ y emite 1 en el último paso. Con 110 recorre $Q_0\\to Q_1\\to Q_3\\to Q_2$ y emite 1 también al final. La secuencia larga 110101000110 produce **cuatro** detecciones (en los símbolos 3, 5, 7 y 12).')],
   fsmfig(M87r, 'Detector de 1010 o 110 (4 estados)') + tabs(M87r) + '\n\n' + tab(['Función', 'Ecuación'], brow87)
   + '\n\nRecorrido del libro, comprobado con la máquina de 4 estados:\n\n' + tab(['Entrada', 'Estados visitados', 'Detecciones'], [['1010', ' → '.join(['Q0'] + [x[1] for x in t1]), '1'], ['110', ' → '.join(['Q0'] + [x[1] for x in t2]), '1'], ['110101000110', ' → '.join(st87), '4']]))

# ============================================================ 8.8 código Manchester: detección de error
M88a = moore(['E0'], {'Q0': [('0', 'Q1'), ('1', 'Q2')], 'Q1': [('1', 'R0'), ('0', 'ERROR')], 'Q2': [('0', 'R1'), ('1', 'ERROR')],
                      'R0': [('0', 'Q1'), ('1', 'Q2')], 'R1': [('0', 'Q1'), ('1', 'Q2')], 'ERROR': [('0', 'ERROR'), ('1', 'ERROR')]},
              {'Q0': (0,), 'Q1': (0,), 'Q2': (0,), 'R0': (0,), 'R1': (0,), 'ERROR': (1,)})
M88b = quotient(M88a)
check('lb8.p88.equivalencia', sorted(map(sorted, M88a.classes())) == [['ERROR'], ['Q0', 'R0', 'R1'], ['Q1'], ['Q2']])
def ref88(bits):
    for k in range(0, len(bits) - 1, 2):
        if bits[k] == bits[k + 1]: return 1
    return 0
ok = True
for _ in range(300):
    s_ = stream(30); b = [x[0] for x in s_]
    if [r[2][0] for r in M88b.run(s_)] != [ref88(b[:t + 1]) for t in range(30)]: ok = False
check('lb8.p88.referencia', ok)
msg = []
for _ in range(100):
    m = [RNG.randint(0, 1) for _ in range(8)]; bits_ = [x for v in m for x in ((0, 1) if v == 0 else (1, 0))]
    msg.append(all(r[2][0] == 0 for r in M88b.run([(x,) for x in bits_])))
check('lb8.p88.mensajes_correctos', all(msg))
M88c = mealy(['P', 'E0'], {}, None) if False else None
M88p = moore(['P', 'E0'], {'INICI': [('0X', 'INICI'), ('10', 'S0'), ('11', 'S1')], 'S0': [('X1', 'INICI'), ('X0', 'ERROR')],
                           'S1': [('X0', 'INICI'), ('X1', 'ERROR')], 'ERROR': [('0X', 'ERROR'), ('1X', 'INICI')]},
             {'INICI': (0,), 'S0': (0,), 'S1': (0,), 'ERROR': (1,)})
check('lb8.p88p.completo', M88p.complete())
enc88 = {'INICI': 0, 'S0': 1, 'S1': 2, 'ERROR': 3}
bk88 = {'J1': 'P*E0*/q0 + /E0*q0', 'K1': '/E0*/q0 + P*q0', 'J0': 'E0*q1 + P*/E0*/q1', 'K0': 'E0*/q1 + P*q1'}
res88, mine88, brow88, *_ = diseno('lb8.p88p', M88p, enc88, 2, 'JK', bk88, ['q1*q0'])
okp = True
for _ in range(300):
    m = [RNG.randint(0, 1) for _ in range(6)]
    seq = []
    for v in m:
        a, b = (0, 1) if v == 0 else (1, 0)
        seq += [(1, a), (RNG.randint(0, 1), b)]
    if any(r[2][0] for r in M88p.run(seq)): okp = False
    bad = seq[:4] + [(1, 0), (RNG.randint(0, 1), 0)]
    r_ = M88p.run(bad)
    if r_[-1][2][0] != 1: okp = False
    r2 = M88p.run(bad + [(0, 1), (0, 0), (1, 0)])
    if not (r2[-3][2][0] == 1 and r2[-2][2][0] == 1 and r2[-1][1] == 'INICI' and r2[-1][2][0] == 0): okp = False
check('lb8.p88p.propiedades', okp)
ej('lb8-8', 'Detección de errores en código Manchester', 'Libro · Cap. 8 · P8.8', 'moore,manchester,reset,jk', 'lb8.p88',
   'Un mensaje llega por una línea serie $E_0$ codificado en **Manchester**: cada bit se envía como dos símbolos, el 0 como 01 y el 1 como 10. Diseña un autómata que active una salida ERROR si en algún par llegan dos símbolos iguales (00 u 11). Sólo se sale del error con el RESET asíncrono. Después rehaz el diseño sustituyendo el RESET por un pulsador **P** de inicio/reinicio, que además marca el primer símbolo de cada par.',
   '**Es un detector de secuencias prohibidas (00 y 11) alineado por parejas.** El autómata sólo necesita saber en qué mitad del par está y cuál fue el primer símbolo. Una vez en ERROR no hay vuelta atrás: la entrada deja de importar (la «X» de la flecha).',
   [('Versión con RESET', 'Seis estados si se quiere saber qué bit llegó (Q0, Q1, Q2, R0, R1, ERROR): $R_0$ y $R_1$ significan «acabo de recibir un 0 / un 1». Como la única salida es ERROR, $R_0$, $R_1$ y $Q_0$ son **equivalentes** (mismas transiciones y misma salida): quedan **cuatro estados**.'),
    ('Versión con pulsador P', 'Entradas ordenadas $P\\,E_0$. Con $P=0$ en INICI el autómata espera. Con $P=1$ la entrada $E_0$ es el primer símbolo: va a $S_0$ si es 0 y a $S_1$ si es 1. En $S_0$ se espera un 1 (vuelve a INICI) y un 0 es error; en $S_1$ al revés. Para recibir el segundo símbolo no hace falta mantener $P$. De ERROR sólo se sale con $P=1$.'),
    ('Códigos libres y condiciones libres', 'Con cuatro estados y dos biestables no hay códigos libres. En cambio, con $P$ y $E_0$ las transiciones tienen muchos «no importa» sobre la entrada (X), que se escriben como una sola flecha para varias combinaciones.')],
   '**Versión con RESET**\n\n' + fsmfig(M88b, 'Manchester con RESET (4 estados)') + tabs(M88b)
   + '\n\nQ0, R0 y R1 se han fusionado en Q0. Simulados 300 flujos aleatorios contra «hay algún par igual en las posiciones pares» y cien mensajes Manchester correctos (ninguno da error).'
   + '\n\n**Versión con pulsador $P$** (entradas $P\\,E_0$)\n\n' + fsmfig(M88p, 'Manchester con pulsador P') + tabs(M88p) + '\n\n' + encs(M88p, enc88, 2)
   + '\n\n' + tab(['Función', 'Ecuación'], brow88)
   + '\n\nLas ecuaciones del libro se han comprobado en las 16 transiciones; además se han verificado propiedades por simulación: un mensaje correcto no da error, un par repetido sí, el error permanece con $P=0$ y se limpia con $P=1$.')

# ============================================================ 8.9 sumador serie (Mealy)
M89 = mealy(['E1', 'E0'], {'C0': [('00', 'C0', (0,)), ('01', 'C0', (1,)), ('10', 'C0', (1,)), ('11', 'C1', (0,))],
                           'C1': [('00', 'C0', (1,)), ('01', 'C1', (0,)), ('10', 'C1', (0,)), ('11', 'C1', (1,))]})
enc89 = {'C0': 0, 'C1': 1}
ok = True
for _ in range(300):
    a = RNG.randrange(256); b = RNG.randrange(256)
    seq = [((a >> k) & 1, (b >> k) & 1) for k in range(8)] + [(0, 0)]
    o = [r[2][0] for r in M89.run(seq)]
    if sum(x << k for k, x in enumerate(o)) != a + b: ok = False
check('lb8.p89.suma', ok)
bkj89 = {'J0': 'E1*E0', 'K0': '/E1*/E0'}; bkd89 = {'D0': 'E0*q0 + E1*q0 + E1*E0'}
resj89, minj89, brj89, *_ = diseno('lb8.p89', M89, enc89, 1, 'JK', bkj89, ['E1^E0^q0'])
resd89, mind89, brd89, *_ = diseno('lb8.p89d', M89, enc89, 1, 'D', bkd89, ['E1^E0^q0'])
check('lb8.p89.s_xor', all(((e1 ^ e0 ^ c) == M89.out('C%d' % c, (e1, e0))[0]) for c in (0, 1) for e1 in (0, 1) for e0 in (0, 1)))
a_, b_ = 13, 11
seq = [((a_ >> k) & 1, (b_ >> k) & 1) for k in range(5)] + [(0, 0)]
st = 'C0'; rows = []
for k, i in enumerate(seq):
    n, o = M89.step(st, i); rows.append([k, i[0], i[1], st[1], o[0], n[1]]); st = n
check('lb8.p89.ejemplo', sum(r[4] << r[0] for r in rows) == 24)
ej('lb8-9', 'Sumador serie con biestable de acarreo (Mealy)', 'Libro · Cap. 8 · P8.9', 'mealy,aritmetica-serie,jk,d', 'lb8.p89',
   'Dos números llegan **en serie**, bit a bit y empezando por el menos significativo, por las líneas $E_1$ y $E_0$. Diseña el autómata que entrega en serie la suma, un bit por ciclo de reloj. Impleméntalo con un biestable J‑K y con uno D.',
   '**Sumar en serie es repetir un sumador completo con una memoria de un bit:** el acarreo. Basta un estado por cada valor del acarreo (0 ó 1): **dos estados y un solo biestable**. La salida es la suma de los tres bits $E_1,E_0$ y acarreo, y depende de la entrada actual, por lo que se trata de un Mealy.',
   [('Estados', '$C_0$: el acarreo pendiente es 0. $C_1$: el acarreo pendiente es 1.'),
    ('Transiciones y salida', 'La suma de tres bits $E_1+E_0+q$ da salida $S=E_1\\oplus E_0\\oplus q$ y nuevo acarreo $=E_1E_0+E_1q+E_0q$ (mayoría). Con $q=0$ sólo hay acarreo si ambos bits son 1. Con $q=1$ lo hay salvo que ambos sean 0.'),
    ('Con J‑K', 'El acarreo se pone a 1 cuando $E_1E_0=11$ ($J_0=E_1E_0$) y se pone a 0 cuando $E_1E_0=00$ ($K_0=\\overline{E_1}\\,\\overline{E_0}$); en los demás casos se mantiene.'),
    ('Con D', '$D_0$ es la función mayoría de $E_1$, $E_0$ y $q_0$, la misma de la etapa de acarreo de un sumador completo.')],
   fsmfig(M89, 'Sumador serie. Etiquetas: $E_1E_0$/S') + tabs(M89)
   + '\n\n**J‑K:** $J_0=E_1E_0$, $K_0=\\overline{E_1}\\,\\overline{E_0}$. **D:** $D_0=E_0q_0+E_1q_0+E_1E_0$. **Salida:** $S=E_1\\oplus E_0\\oplus q_0$ (3 puertas XOR en cadena de dos).'
   + '\n\nEjemplo $13+11$ (01101 y 01011, bit menos significativo primero): ' + '\n\n' + tab(['Ciclo', '$E_1$', '$E_0$', 'Acarreo previo', 'Salida $S$', 'Acarreo nuevo'], rows)
   + '\n\nLa salida leída de abajo arriba es 11000 = 24, y el ciclo extra con entradas a 0 saca el acarreo final. Comprobado con 300 pares aleatorios de 8 bits.')
