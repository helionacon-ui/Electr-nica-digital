# -*- coding: utf-8 -*-
# Problemas 8.10 a 8.20 (se ejecuta dentro de gen_libro8.py)
def cmpt(res, bk, M, nb):
    ig = same_funcs(res, bk, M, nb)
    return ('Mi propia minimización coincide con ellas como función.' if ig
            else 'Mi minimización da expresiones distintas, equivalentes en todas las transiciones que ocurren (sólo difieren en indiferentes).')
def hist(M, seq, st=None):
    rows = []; s = st or M.start
    for k, i in enumerate(seq, 1):
        r = M.run([i], s)[0]; s = r[1]
        rows.append([k, ''.join(map(str, i)), r[1], ''.join(map(str, r[2]))])
    return rows
def bits(s): return tuple(int(c) for c in s)
def sobs(M, seq):
    """Lista de salidas (como cadenas) tras cada paso."""
    return [''.join(map(str, r[2])) for r in M.run(seq)]

# ============================================================ 8.10 sumador serie (Moore)
M810 = moore(['E1', 'E0'], {
    'C0S0': [('00', 'C0S0'), ('01', 'C0S1'), ('10', 'C0S1'), ('11', 'C1S0')],
    'C0S1': [('00', 'C0S0'), ('01', 'C0S1'), ('10', 'C0S1'), ('11', 'C1S0')],
    'C1S0': [('00', 'C0S1'), ('01', 'C1S0'), ('10', 'C1S0'), ('11', 'C1S1')],
    'C1S1': [('00', 'C0S1'), ('01', 'C1S0'), ('10', 'C1S0'), ('11', 'C1S1')]},
    {'C0S0': (0,), 'C0S1': (1,), 'C1S0': (0,), 'C1S1': (1,)})
ok = True; ok2 = True
for _ in range(300):
    a = RNG.randrange(256); b = RNG.randrange(256)
    seq = [((a >> k) & 1, (b >> k) & 1) for k in range(8)] + [(0, 0)]
    o = [r[2][0] for r in M810.run(seq)]
    if sum(x << k for k, x in enumerate(o)) != a + b: ok = False
    if o != [r[2][0] for r in M89.run(seq)]: ok2 = False
check('lb8.p810.suma', ok); check('lb8.p810.igual_mealy', ok2)
check('lb8.p810.estados_minimos', len(quotient(M810).states) == 4)
enc810 = {'C0S0': 0, 'C0S1': 1, 'C1S0': 2, 'C1S1': 3}
K0ok = '/E1*/E0*/q1 + /E1*E0*q1 + E1*/E0*q1 + E1*E0*/q1'
K0bad = '/E1*/E0*q1 + /E1*E0*q1 + E1*/E0*q1 + E1*E0*/q1'
bk810 = {'J1': 'E1*E0', 'K1': '/E1*/E0', 'J0': 'E1^E0^q1', 'K0': K0ok}
res810, mine810, brow810, *_ = diseno('lb8.p810', M810, enc810, 2, 'JK', bk810, ['q0'])
fbad = check_realization(M810, enc810, 2, dict(bk810, K0=K0bad), 'JK', ['q0'])
check('lb8.p810.k0_impreso_falla', sorted((f[1], f[2]) for f in fbad) == [('C0S1', '00'), ('C1S1', '00')], str(fbad))
book('lb8.p810', False, 'K0 impreso con /E1 /E0 q1 en lugar de /E1 /E0 /q1')
ej('lb8-10', 'Sumador serie como autómata de Moore', 'Libro · Cap. 8 · P8.10', 'moore,aritmetica-serie,jk', 'lb8.p810',
   'Rehaz el sumador serie del problema anterior como autómata de **Moore**: la salida debe depender sólo del estado. Los operandos llegan por $E_1$ y $E_0$, bit menos significativo primero. Impleméntalo con biestables J‑K y analiza si se pueden reducir estados y qué diferencia hay con la versión de Mealy.',
   '**En un Moore la salida es parte del estado**, así que el estado tiene que recordar, además del acarreo, el último bit de suma que se calculó. Las combinaciones (acarreo, suma) son cuatro: $C_0S_0$, $C_0S_1$, $C_1S_0$ y $C_1S_1$.',
   [('Transiciones', 'Desde un estado con acarreo $c$ y entradas $E_1E_0$ se calcula la suma $s=E_1\\oplus E_0\\oplus c$ y el acarreo nuevo $c\'=E_1E_0+E_1c+E_0c$; el estado siguiente es $C_{c\'}S_s$. La transición **no depende del bit de suma almacenado**: $C_0S_0$ y $C_0S_1$ tienen las mismas filas, y lo mismo $C_1S_0$ y $C_1S_1$.'),
    ('¿Se pueden fusionar?', 'A pesar de esa simetría **no son equivalentes**: tienen distinta salida (el bit $S$). Un Moore necesita pues cuatro estados y dos biestables, frente a los dos estados y un biestable del Mealy. El algoritmo de particiones confirma que cuatro es el mínimo.'),
    ('Codificación y ecuaciones', 'Con el código $q_1q_0=(\\text{acarreo},\\text{suma})$ la salida es $S=q_0$. El biestable $q_1$ hace de acarreo exactamente como en el Mealy ($J_1=E_1E_0$, $K_1=\\overline{E_1}\\,\\overline{E_0}$) y $q_0$ guarda la suma: $J_0=E_1\\oplus E_0\\oplus q_1$ y $K_0$ es su negación.'),
    ('Retardo', 'En un circuito real la suma aparece **un ciclo más tarde** que en el Mealy (se lee en el estado, tras el flanco). Por eso, después de los $n$ bits de los operandos, hace falta un ciclo extra con entradas 00 para sacar el último bit.')],
   fsmfig(M810, 'Sumador serie de Moore. Cada estado: $C$ (acarreo) y $S$ (suma)') + tabs(M810) + '\n\n' + encs(M810, enc810, 2) + '\n\n' + tab(['Función', 'Ecuación (libro, corregida)'], brow810)
   + '\n\n' + cmpt(resj := res810, {k: bk810[k] for k in ('J1', 'K1', 'J0', 'K0')}, M810, 2)
   + '\n\nSimulados 300 pares de números de 8 bits: la salida da $a+b$ y es, ciclo a ciclo, idéntica a la del Mealy.'
   + ojo('En la ecuación de $K_0$ el primer sumando aparece impreso como $\\overline{E_1}\\,\\overline{E_0}\\,q_1$, pero debe ser $\\overline{E_1}\\,\\overline{E_0}\\,\\overline{q_1}$. $K_0=\\overline{E_1\\oplus E_0\\oplus q_1}$ vale 1 cuando entre $E_1$, $E_0$ y $q_1$ hay un número **par** de unos: para 000 sí, para 001 no. Con el término impreso fallan exactamente dos transiciones, ambas con entrada 00: en $C_0S_1$ el biestable $q_0$ no se pone a 0 (debería, pues la suma es 0) y en $C_1S_1$ sí se pone a 0 (debería quedarse en 1, pues la suma es 1). Se ha comprobado contra la tabla.'))

# ============================================================ 8.11 contador mod 4 reversible (Moore, 8 estados)
r811 = {}
for k in range(4): r811['A%d' % k] = [('0', 'D3'), ('1', 'A%d' % ((k + 1) % 4))]
for k in (3, 2, 1, 0): r811['D%d' % k] = [('0', 'D%d' % ((k - 1) % 4)), ('1', 'A0')]
M811 = moore(['E0'], r811, {s: ((int(s[1]) >> 1) & 1, int(s[1]) & 1) for s in r811})
def ref811(bs):
    cnt = 0; d = 'u'; o = []
    for e in bs:
        if e: cnt = (cnt + 1) % 4 if d == 'u' else 0; d = 'u'
        else: cnt = (cnt - 1) % 4 if d == 'd' else 3; d = 'd'
        o.append(cnt)
    return o
ok = True
for _ in range(300):
    s_ = stream(40); b = [x[0] for x in s_]
    got = [2 * r[2][0] + r[2][1] for r in M811.run(s_)]
    if got != ref811(b): ok = False
check('lb8.p811.referencia', ok)
check('lb8.p811.ocho_estados', len(M811.classes()) == 8)
enc811 = {'A0': 0, 'A1': 1, 'A2': 2, 'A3': 3, 'D3': 4, 'D2': 5, 'D1': 6, 'D0': 7}
bk811 = {'J2': '/E0', 'K2': 'E0', 'J1': 'E0*/q2*q0 + /E0*q2*q0', 'K1': '/E0*/q2 + q0 + E0*q2', 'J0': 'E0*/q2 + /E0*q2', 'K0': '1'}
res811, mine811, brow811, *_ = diseno('lb8.p811', M811, enc811, 3, 'JK', bk811, ['q2^q1', 'q2^q0'])
ej('lb8-11', 'Contador módulo 4 reversible (Moore, 8 estados)', 'Libro · Cap. 8 · P8.11', 'moore,contador,jk', 'lb8.p811',
   'Diseña un contador de Moore **módulo 4 reversible**: con $E_0=1$ cuenta hacia arriba (0, 1, 2, 3, 0, …) y con $E_0=0$ hacia abajo (3, 2, 1, 0, 3, …). La salida son dos bits con el valor de la cuenta. Al cambiar el sentido, la nueva secuencia **empieza por su primer valor** (por ejemplo, al pasar de subir a bajar se sale con el 3).',
   '**El valor de la cuenta no basta para decidir el siguiente**: si la salida es 2, lo que viene depende de si se estaba subiendo (2→3) o bajando (2→1). Hay que recordar el sentido, y por eso se necesitan **dos copias de cada valor**: ocho estados.',
   [('Estados', '$A_0\\dots A_3$: cuenta ascendente (salida 0…3). $D_3\\dots D_0$: cuenta descendente (salida 3…0). El estado inicial es $A_0$.'),
    ('Transiciones', 'Dentro de una secuencia se avanza con el mismo valor de $E_0$ (en $A_k$, $E_0=1$ da $A_{k+1}$; en $D_k$, $E_0=0$ da $D_{k-1}$, con vuelta módulo 4). Al cambiar de sentido: desde cualquier $A_k$ con $E_0=0$ se salta a $D_3$, y desde cualquier $D_k$ con $E_0=1$ se salta a $A_0$.'),
    ('¿Bastarían cuatro estados?', 'No. El algoritmo de particiones deja los ocho estados separados: por ejemplo $A_2$ y $D_2$ tienen la misma salida pero llevan a salidas distintas (3 ó 3 frente a 1 ó 0).'),
    ('Codificación', 'Se codifica con $q_2$ = sentido (0 ascendente, 1 descendente) y $q_1q_0$ = el valor en las ascendentes; en las descendentes se numeran $D_3=100$, $D_2=101$, $D_1=110$, $D_0=111$. Con esa elección las salidas son sencillas: $S_1=q_2\\oplus q_1$, $S_0=q_2\\oplus q_0$ (una XOR convierte los códigos descendentes en el valor de la cuenta).')],
   fsmfig(M811, 'Contador reversible mod 4 (Moore). Estado: salida') + tabs(M811) + '\n\n' + encs(M811, enc811, 3)
   + '\n\n' + tab(['Función', 'Ecuación'], brow811)
   + '\n\nLas ecuaciones del libro se han comprobado en las 16 transiciones (los ocho códigos están usados, no hay indiferentes). Simulados 300 flujos aleatorios de 40 entradas contra un modelo que lleva la cuenta y el sentido.')

# ============================================================ 8.12 contador módulo 8 con habilitación
M812 = moore(['E0'], {'Q%d' % n: [('0', 'Q%d' % n), ('1', 'Q%d' % ((n + 1) % 8))] for n in range(8)},
             {'Q%d' % n: ((n >> 2) & 1, (n >> 1) & 1, n & 1) for n in range(8)})
ok = True
for _ in range(200):
    s_ = stream(50); b = [x[0] for x in s_]
    got = [4 * r[2][0] + 2 * r[2][1] + r[2][2] for r in M812.run(s_)]
    if got != [sum(b[:t + 1]) % 8 for t in range(50)]: ok = False
check('lb8.p812.referencia', ok)
enc812 = {'Q%d' % n: n for n in range(8)}
bk812 = {'J2': 'E0*q1*q0', 'K2': 'E0*q1*q0', 'J1': 'E0*q0', 'K1': 'E0*q0', 'J0': 'E0', 'K0': 'E0'}
res812, mine812, brow812, *_ = diseno('lb8.p812', M812, enc812, 3, 'JK', bk812, ['q2', 'q1', 'q0'])
ig812 = same_funcs(res812, bk812, M812, 3)
check('lb8.p812.mismas_ecuaciones', ig812 is True)
ej('lb8-12', 'Contador módulo 8 con habilitación (Moore)', 'Libro · Cap. 8 · P8.12', 'moore,contador,jk', 'lb8.p812',
   'Diseña un contador de Moore **módulo 8** con una entrada de habilitación $E_0$: con $E_0=1$ cuenta un valor en cada flanco de reloj y con $E_0=0$ se mantiene. La salida son tres bits con el valor de la cuenta.',
   '**Ocho estados, uno por valor, y la salida es el propio código del estado**, así que no hace falta lógica de salida. Todo el trabajo está en las funciones de excitación, y con J‑K sale una estructura muy regular.',
   [('Autómata', '$Q_n\\xrightarrow{E_0=0}Q_n$ y $Q_n\\xrightarrow{E_0=1}Q_{(n+1)\\bmod 8}$. Es un anillo de ocho estados con un lazo en cada uno.'),
    ('Codificación', 'Se asigna a $Q_n$ el binario de $n$ en $q_2q_1q_0$; así $S_2S_1S_0=q_2q_1q_0$.'),
    ('Excitación', 'Un bit cambia de valor cuando el contador está habilitado **y todos los bits inferiores valen 1** (acarreo del incremento). Para ese bit se necesita conmutar: $J=K=1$; en caso contrario, mantener: $J=K=0$. De ahí $J_0=K_0=E_0$, $J_1=K_1=E_0q_0$ y $J_2=K_2=E_0q_1q_0$: es un contador con biestables que **conmutan** (tipo T).')],
   fsmfig(M812, 'Contador módulo 8 con habilitación. Etiqueta: $E_0$') + tabs(M812) + '\n\n' + tab(['Función', 'Ecuación'], brow812)
   + '\n\nMi minimización coincide con las del libro como función. Simulados 200 flujos de 50 entradas: la salida es siempre «número de unos recibidos módulo 8». Coste: dos AND de dos y tres entradas ($E_0q_0$ y $E_0q_1q_0$; la AND de tres puede hacerse en cascada con la anterior).')

# ============================================================ 8.13 registro de desplazamiento
M813 = moore(['E0'], {'Q%d' % n: [('0', 'Q%d' % ((2 * n) % 8)), ('1', 'Q%d' % ((2 * n + 1) % 8))] for n in range(8)},
             {'Q%d' % n: ((n >> 2) & 1, (n >> 1) & 1, n & 1) for n in range(8)})
ok = True
for _ in range(200):
    s_ = stream(30); b = [x[0] for x in s_]
    exp = []
    for t in range(30):
        w = ([0, 0, 0] + b[:t + 1])[-3:]
        exp.append(tuple(w))
    if [tuple(r[2]) for r in M813.run(s_)] != exp: ok = False
check('lb8.p813.referencia', ok)
enc813 = {'Q%d' % n: n for n in range(8)}
bkJ813 = {'J2': 'q1', 'K2': '/q1', 'J1': 'q0', 'K1': '/q0', 'J0': 'E0', 'K0': '/E0'}
bkD813 = {'D2': 'q1', 'D1': 'q0', 'D0': 'E0'}
resj813, minj813, brj813, *_ = diseno('lb8.p813', M813, enc813, 3, 'JK', bkJ813, ['q2', 'q1', 'q0'])
resd813, mind813, brd813, *_ = diseno('lb8.p813d', M813, enc813, 3, 'D', bkD813, ['q2', 'q1', 'q0'])
check('lb8.p813.mismas_J', same_funcs(resj813, bkJ813, M813, 3) is True)
check('lb8.p813.mismas_D', same_funcs(resd813, bkD813, M813, 3) is True)
ej('lb8-13', 'Registro de desplazamiento de 3 bits visto como autómata (Moore)', 'Libro · Cap. 8 · P8.13', 'moore,registro,jk,d', 'lb8.p813',
   'Un registro de desplazamiento de tres bits, con entrada serie $E_0$ y desplazamiento hacia la izquierda, es también un autómata. Diséñalo como autómata de Moore (salida = contenido del registro) con biestables J‑K y con biestables D.',
   '**Ejercicio de cambio de punto de vista:** el estado es el contenido del registro, así que hay ocho estados $Q_n$ ($n$ = valor binario). Al desplazar a la izquierda el valor se duplica y entra $E_0$ por la derecha. Ya se sabe cómo debe quedar el circuito; la gracia es que el método general lo reconstruye.',
   [('Transiciones', '$Q_n\\xrightarrow{0}Q_{2n\\bmod 8}$ y $Q_n\\xrightarrow{1}Q_{(2n+1)\\bmod 8}$. El bit más significativo se pierde (sale del registro) y el nuevo bit entra por el menos significativo.'),
    ('Con biestables D', '$D=Q^+$: el bit $q_2$ pasa a valer el que tenía $q_1$, $q_1$ el de $q_0$ y $q_0$ el de la entrada: $D_2=q_1$, $D_1=q_0$, $D_0=E_0$. Son cables directos, sin puertas.'),
    ('Con biestables J‑K', 'El método da $J_2=q_1$, $K_2=\\overline{q_1}$, $J_1=q_0$, $K_1=\\overline{q_0}$, $J_0=E_0$, $K_0=\\overline{E_0}$: cada J‑K se comporta como un D (con un inversor entre J y K). Es la forma de convertir un J‑K en D.')],
   tabs(M813) + '\n\n**J‑K**\n\n' + tab(['Función', 'Ecuación'], brj813) + '\n\n**D**\n\n' + tab(['Función', 'Ecuación'], brd813)
   + '\n\nLas ecuaciones del libro coinciden con las mías como funciones y reproducen las 16 transiciones. Simulados 200 flujos: la salida es siempre «los tres últimos bits recibidos» (con ceros al principio). El diagrama completo tiene 16 flechas y se omite aquí por ser poco legible.')

# ============================================================ 8.14 bit de paridad (Mealy, 7 -> 5 estados)
M814a = mealy(['E0'], {'Q0': [('0', 'Q1', (0,)), ('1', 'Q2', (0,))],
                       'Q1': [('0', 'Q3', (0,)), ('1', 'Q4', (0,))], 'Q2': [('0', 'Q5', (0,)), ('1', 'Q6', (0,))],
                       'Q3': [('0', 'Q0', (0,)), ('1', 'Q0', (1,))], 'Q4': [('0', 'Q0', (1,)), ('1', 'Q0', (0,))],
                       'Q5': [('0', 'Q0', (1,)), ('1', 'Q0', (0,))], 'Q6': [('0', 'Q0', (0,)), ('1', 'Q0', (1,))]})
M814 = mealy(['E0'], {'Q0': [('0', 'Q2', (0,)), ('1', 'Q1', (0,))], 'Q1': [('0', 'Q4', (0,)), ('1', 'Q3', (0,))],
                      'Q2': [('0', 'Q3', (0,)), ('1', 'Q4', (0,))], 'Q3': [('0', 'Q0', (0,)), ('1', 'Q0', (1,))],
                      'Q4': [('0', 'Q0', (1,)), ('1', 'Q0', (0,))]})
par = lambda b: int(len(b) % 3 == 0 and sum(b[-3:]) % 2 == 1)
check('lb8.p814.ref7', sim_ref(M814a, par, 200, 60)); check('lb8.p814.ref5', sim_ref(M814, par, 200, 60))
check('lb8.p814.clases', sorted(map(sorted, M814a.classes())) == [['Q0'], ['Q1'], ['Q2'], ['Q3', 'Q6'], ['Q4', 'Q5']])
M814m, nm814m = moore_of_mealy(M814)
check('lb8.p814.moore_ref', sim_ref_moore(M814m, par)); n814m = len(quotient(M814m).states)
check('lb8.p814.moore_min', n814m == len(M814m.states), str((len(M814m.states), n814m)))
enc814 = {'Q%d' % k: k for k in range(5)}
bk814 = {'J2': '/E0*/q1*q0 + E0*q1*/q0', 'K2': '1', 'J1': '/E0*/q2*/q0 + E0*q0', 'K1': 'q0 + E0', 'J0': 'E0*/q2*/q1 + /E0*q1', 'K0': '/E0 + q1'}
res814, mine814, brow814, *_ = diseno('lb8.p814', M814, enc814, 3, 'JK', bk814, ['E0*q1*q0 + /E0*q2'])
ej('lb8-14', 'Bit de paridad par de un mensaje de 3 bits (Mealy, 7→5 estados)', 'Libro · Cap. 8 · P8.14', 'mealy,paridad,reduccion,jk', 'lb8.p814',
   'Un mensaje de **tres bits** llega en serie por $E_0$, sin pausas, y se repite sin parar. Diseña un autómata de Mealy que ponga su salida a 0 en los dos primeros bits de cada mensaje y, en el tercero, entregue el **bit de paridad par** (1 si el número de unos del mensaje es impar). Después de cada tercer bit, el autómata vuelve al principio.',
   '**El primer diseño es un árbol de decisión de tres niveles**: tras el primer bit (2 casos), tras el segundo (4 casos) y tras el tercero se vuelve a $Q_0$. Salen siete estados. Pero para calcular la paridad **no importa qué bits llegaron, sólo cuántos unos**, y eso permite reducir.',
   [('Diseño en árbol (7 estados)', '$Q_1$/$Q_2$: el primer bit fue 0/1. $Q_3,\\dots,Q_6$: los dos primeros bits fueron 00, 01, 10 y 11. En el tercer bit la salida es el OR exclusivo de los tres. Desde $Q_3\\dots Q_6$ se vuelve a $Q_0$.'),
    ('Reducción', 'El algoritmo de particiones fusiona $Q_3$ con $Q_6$ (ambos con paridad par hasta ahora: salida 0 con un 0 y 1 con un 1) y $Q_4$ con $Q_5$ (paridad impar). Quedan **cinco estados**: $Q_0$, dos para «primer bit visto» y dos para «paridad par/impar».'),
    ('Estados del diseño reducido', '$Q_0$ inicio. $Q_1$ primer bit 1 y $Q_2$ primer bit 0 (el nombre es de la tabla de abajo). $Q_3$: paridad par tras dos bits. $Q_4$: paridad impar tras dos bits. En el tercer bit: $Q_3$ emite lo que llega y $Q_4$ lo invierte.'),
    ('Mealy y Moore', 'En el Mealy la paridad sale **durante** el tercer ciclo (depende de la entrada actual); en el Moore equivalente sale tras el tercer flanco. Pasar a Moore exige duplicar $Q_0$ según lleguemos con salida 0 ó 1: **%d estados** y ninguna fusión posible.' % len(M814m.states))],
   '**Árbol de 7 estados**\n\n' + tabs(M814a)
   + '\n\n**Reducido a 5 estados** (los estados se renombran)\n\n' + fsmfig(M814, 'Paridad de 3 bits, 5 estados. $E_0$/S') + tabs(M814) + '\n\n' + encs(M814, enc814, 3)
   + '\n\n' + tab(['Función', 'Ecuación'], brow814)
   + '\n\nLas ecuaciones del libro se han comprobado en las 10 transiciones (los códigos 101, 110 y 111 son indiferentes). Las dos versiones, la de 7 y la de 5 estados, se han simulado con 200 flujos aleatorios de 60 bits contra el modelo «cada tres bits, el OR exclusivo de los tres». ' + cmpt(res814, bk814, M814, 3))

# ============================================================ 8.15 codificador 4:2 con prioridad serie (Mealy)
def vals(M, seq): return [2 * r[2][0] + r[2][1] for r in M.run(seq)]
def enc42(d3, d2, d1): return 3 if d3 else 2 if d2 else 1 if d1 else 0
M815 = mealy(['E0'], {'Q0': [('X', 'Q1', (0, 0))], 'Q1': [('0', 'Q2', (0, 0)), ('1', 'Q3', (0, 0))],
                      'Q2': [('0', 'Q4', (0, 0)), ('1', 'Q5', (0, 0))], 'Q3': [('0', 'Q6', (0, 0)), ('1', 'Q5', (0, 0))],
                      'Q4': [('0', 'Q0', (0, 0)), ('1', 'Q0', (1, 1))], 'Q5': [('0', 'Q0', (1, 0)), ('1', 'Q0', (1, 1))],
                      'Q6': [('0', 'Q0', (0, 1)), ('1', 'Q0', (1, 1))]})
M815b = mealy(['E0'], {'Q0': [('1', 'Q1', (0, 0)), ('0', 'Q2', (0, 0))], 'Q1': [('X', 'Q3', (0, 0))], 'Q2': [('1', 'Q4', (0, 0)), ('0', 'Q5', (0, 0))],
                       'Q3': [('X', 'Q6', (0, 0))], 'Q4': [('X', 'Q7', (0, 0))], 'Q5': [('1', 'Q8', (0, 0)), ('0', 'Q9', (0, 0))],
                       'Q6': [('X', 'Q0', (1, 1))], 'Q7': [('X', 'Q0', (1, 0))], 'Q8': [('X', 'Q0', (0, 1))], 'Q9': [('X', 'Q0', (0, 0))]})
check('lb8.p815.completo', M815.complete() and M815b.complete())
ok = ok2 = True
for _ in range(300):
    s_ = stream(48); b = [x[0] for x in s_]
    exp = [0] * 48; expb = [0] * 48
    for k in range(0, 48, 4):
        d0, d1, d2, d3 = b[k:k + 4]; exp[k + 3] = enc42(d3, d2, d1)
        e3, e2, e1, e0 = b[k:k + 4]; expb[k + 3] = enc42(e3, e2, e1)
    if vals(M815, s_) != exp: ok = False
    if vals(M815b, s_) != expb: ok2 = False
check('lb8.p815.lsb', ok); check('lb8.p815.msb', ok2)
check('lb8.p815.estados', len(M815.classes()) == 7 and len(M815b.classes()) == 10)
enc815 = {'Q%d' % k: k for k in range(7)}
bk815 = {'J2': 'q1', 'K2': '1', 'J1': '/q2*q0', 'K1': '/q0 + E0', 'J0': '/q2*/q1 + E0*/q2', 'K0': '/E0 + q2'}
res815, mine815, brow815, *_ = diseno('lb8.p815', M815, enc815, 3, 'JK', bk815, ['q2*q0 + E0*q2', 'q2*q1 + E0*q2'])
ej('lb8-15', 'Codificador de prioridad 4:2 serie (Mealy)', 'Libro · Cap. 8 · P8.15', 'mealy,codificador,jk', 'lb8.p815',
   'Las cuatro entradas $d_0,d_1,d_2,d_3$ de un codificador de prioridad 4:2 llegan **en serie** por $E_0$, en ese orden (primero $d_0$), repitiéndose en grupos de cuatro bits. Diseña un autómata de Mealy que, al llegar el cuarto bit, entregue por dos salidas $S_1S_0$ el código de la entrada activa de mayor índice ($d_0$ no importa: si sólo está activa $d_0$ o ninguna, sale 00). En los otros ciclos las salidas valen 00. Estudia después si tiene ventaja recibir los bits en orden inverso.',
   '**La prioridad manda sobre el orden de llegada:** la entrada de mayor índice llega la última, así que cuando se recibe $d_3$ ya se conoce todo lo anterior. Cada estado debe resumir «cuál es la entrada activa más alta de las vistas hasta ahora». Con un contador de posición implícito (que sólo avanza) los estados forman un árbol que se reúne en $Q_0$.',
   [('Primer bit', '$d_0$ no influye en el resultado: de $Q_0$ se pasa a $Q_1$ con cualquier entrada (la «X» de la flecha).'),
    ('Segundo y tercer bit', '$Q_1\\to Q_2$ si $d_1=0$ y $Q_1\\to Q_3$ si $d_1=1$. Después, $d_2=1$ lleva a $Q_5$ («la mayor vista es $d_2$», que domina a $d_1$) en cualquiera de los dos casos; con $d_2=0$ se llega a $Q_4$ (ninguna activa: 00) o a $Q_6$ (sólo $d_1$: 01).'),
    ('Cuarto bit', 'Desde $Q_4$, $Q_5$ y $Q_6$ se vuelve a $Q_0$ y se emite el código: con $d_3=1$ siempre 11; con $d_3=0$, 00, 10 ó 01 según el estado.'),
    ('Orden inverso (el más significativo primero)', 'Se puede, pero **no es más sencillo**: hay que decidir ya con $d_3$ y seguir contando los bits restantes sin cambiar de opinión, con cadenas de estados «X» hasta el final del grupo. Salen **10 estados** (el más significativo primero, la prioridad no deja ahorrar ninguno); el algoritmo de particiones confirma que son todos distintos.')],
   '**Orden $d_0$ primero** (7 estados)\n\n' + fsmfig(M815, 'Codificador 4:2 serie ($d_0$ primero). $E_0$/$S_1S_0$') + tabs(M815) + '\n\n' + encs(M815, enc815, 3)
   + '\n\n' + tab(['Función', 'Ecuación'], brow815)
   + '\n\nLas ecuaciones del libro reproducen las 14 transiciones (código 111 indiferente). Simulados 300 flujos de 48 bits contra el modelo de prioridad: coinciden las dos versiones.\n\n**Orden inverso** (10 estados)\n\n' + tabs(M815b)
   + '\n\n' + cmpt(res815, bk815, M815, 3))

# ============================================================ 8.16 comparador serie (Moore)
def cmp3(a, b): return (1, 0, 0) if a > b else (0, 1, 0) if a == b else (0, 0, 1)
M816 = moore(['E1', 'E0'], {'IGUAL': [('00', 'IGUAL'), ('01', 'MENOR'), ('10', 'MAYOR'), ('11', 'IGUAL')],
                            'MAYOR': [('00', 'MAYOR'), ('01', 'MENOR'), ('10', 'MAYOR'), ('11', 'MAYOR')],
                            'MENOR': [('00', 'MENOR'), ('01', 'MENOR'), ('10', 'MAYOR'), ('11', 'MENOR')]},
             {'IGUAL': (0, 1, 0), 'MAYOR': (1, 0, 0), 'MENOR': (0, 0, 1)})
M816b = moore(['E1', 'E0'], {'IGUAL': [('00', 'IGUAL'), ('01', 'MENOR'), ('10', 'MAYOR'), ('11', 'IGUAL')],
                             'MAYOR': [('XX', 'MAYOR')], 'MENOR': [('XX', 'MENOR')]}, M816.outs)
ok = ok2 = True
for _ in range(300):
    a = RNG.randrange(256); b = RNG.randrange(256)
    seq = [((a >> k) & 1, (b >> k) & 1) for k in range(8)]
    o = [tuple(r[2]) for r in M816.run(seq)]
    if o != [cmp3(a & ((1 << (k + 1)) - 1), b & ((1 << (k + 1)) - 1)) for k in range(8)]: ok = False
    seqb = [((a >> (7 - k)) & 1, (b >> (7 - k)) & 1) for k in range(8)]
    o2 = [tuple(r[2]) for r in M816b.run(seqb)]
    if o2 != [cmp3(a >> (7 - k), b >> (7 - k)) for k in range(8)]: ok2 = False
check('lb8.p816.lsb', ok); check('lb8.p816.msb', ok2)
check('lb8.p816.estados', len(M816.classes()) == 3 and len(M816b.classes()) == 3)
enc816 = {'IGUAL': 0, 'MAYOR': 1, 'MENOR': 2}
bk816 = {'J1': '/E1*E0', 'K1': 'E1*/E0', 'J0': 'E1*/E0', 'K0': '/E1*E0'}
res816, mine816, brow816, *_ = diseno('lb8.p816', M816, enc816, 2, 'JK', bk816, ['q0', '/q1*/q0', 'q1'])
bk816b = {'J1': '/E1*E0*/q0', 'K1': '0', 'J0': 'E1*/E0*/q1', 'K0': '0'}
res816b, mine816b, brow816b, *_ = diseno('lb8.p816b', M816b, enc816, 2, 'JK', bk816b, ['q0', '/q1*/q0', 'q1'])
ex = [(0, 0), (1, 1), (1, 0), (1, 0), (0, 0), (0, 1)]
rex = hist(M816, ex)
check('lb8.p816.ejemplo', [r[2] for r in rex] == ['IGUAL', 'IGUAL', 'MAYOR', 'MAYOR', 'MAYOR', 'MENOR'])
book('lb8.p816', False, 'el ejemplo del libro anota B=100010 como 18; vale 34')
ej('lb8-16', 'Comparador serie de dos números (Moore)', 'Libro · Cap. 8 · P8.16', 'moore,comparador,aritmetica-serie,jk', 'lb8.p816',
   'Dos números llegan en serie por $E_1$ ($A$) y $E_0$ ($B$), **empezando por el bit menos significativo**. Diseña un autómata de Moore que indique en tres salidas $S_2S_1S_0$ si, con los bits recibidos hasta el momento, $A>B$, $A=B$ o $A<B$. Impleméntalo con J‑K. Después piensa qué cambia si los bits llegan empezando por el más significativo.',
   '**Con el menos significativo primero manda siempre el último bit que difiere:** cada bit nuevo es más significativo que todos los anteriores, así que si $E_1\\ne E_0$ decide él; si son iguales, se mantiene el veredicto anterior. Tres estados: IGUAL, MAYOR y MENOR.',
   [('Transiciones (LSB primero)', 'En cualquier estado, $E_1E_0=10$ lleva a MAYOR y $01$ a MENOR (el bit nuevo prevalece). Con $00$ ó $11$ se queda donde estaba. Desde IGUAL, $00$ y $11$ mantienen IGUAL.'),
    ('Codificación y ecuaciones', 'IGUAL $=00$, MAYOR $=01$, MENOR $=10$ (el 11 es indiferente). Las salidas son simples: $S_2=q_0$ (mayor), $S_1=\\overline{q_1}\\,\\overline{q_0}$ (igual), $S_0=q_1$ (menor).'),
    ('Orden inverso (MSB primero)', 'Ahora el **primer bit que difiere** decide para siempre: MAYOR y MENOR se vuelven estados absorbentes (se quedan con cualquier entrada) y sólo IGUAL puede abandonarse. Las ecuaciones se simplifican: $K_1=K_0=0$, $J_1=\\overline{E_1}E_0\\overline{q_0}$, $J_0=E_1\\overline{E_0}\\,\\overline{q_1}$. Esa versión necesita un reinicio para empezar otra comparación.')],
   fsmfig(M816, 'Comparador serie, LSB primero (Moore). Estado: $S_2S_1S_0$') + tabs(M816) + '\n\n' + encs(M816, enc816, 2) + '\n\n' + tab(['Función', 'Ecuación'], brow816)
   + '\n\n**Versión MSB primero**\n\n' + fsmfig(M816b, 'Comparador serie, MSB primero') + tab(['Función', 'Ecuación'], brow816b)
   + '\n\nSimulados 300 pares de 8 bits en los dos órdenes, comprobando la salida **en cada ciclo** (en LSB primero, comparando los bits bajos recibidos; en MSB primero, los bits altos). Ejemplo con $A=001110_2=14$ y $B=100010_2=34$, LSB primero:\n\n'
   + tab(['Ciclo', '$E_1E_0$', 'Estado', 'Salida'], [[r[0], r[1], r[2], r[3]] for r in rex])
   + '\n\nTras 5 bits ($A=01110=14$, $B=00010=2$) el resultado es MAYOR; el sexto bit, $A_5=0$ y $B_5=1$, lo cambia a MENOR, porque $B$ pasa a valer 34.'
   + ojo('En el ejemplo numérico del libro el segundo número, 100010, aparece con valor decimal 18. Es 34 ($32+2$). La conclusión ($A<B$) no cambia.'))

# ============================================================ 8.17 puerta automática (Moore, entradas PAC)
M817 = moore(['P', 'A', 'C'], {
    'QUIETO': [('000', 'CERRAR'), ('001', 'QUIETO'), ('010', 'CERRAR'), ('100', 'ABRIR'), ('101', 'ABRIR'), ('110', 'ABRIR')],
    'ABRIR': [('000', 'ABRIR'), ('001', 'ABRIR'), ('010', 'CERRAR'), ('100', 'ABRIR'), ('101', 'ABRIR'), ('110', 'CERRAR')],
    'CERRAR': [('000', 'CERRAR'), ('001', 'QUIETO'), ('010', 'CERRAR'), ('100', 'ABRIR'), ('101', 'QUIETO'), ('110', 'CERRAR')]},
    {'QUIETO': (0, 0), 'ABRIR': (1, 0), 'CERRAR': (0, 1)}, valid=lambda i: not (i[1] and i[2]))
check('lb8.p817.completo', M817.complete())
H1 = [bits(x) for x in ('001', '101', '100', '000', '010', '000', '001')]
h1 = hist(M817, H1)
check('lb8.p817.historia1', [r[2] for r in h1] == ['QUIETO', 'ABRIR', 'ABRIR', 'ABRIR', 'CERRAR', 'CERRAR', 'QUIETO'] and [r[3] for r in h1] == ['00', '10', '10', '10', '01', '01', '00'])
H2 = [bits(x) for x in ('001', '101', '100', '000', '010', '000', '100', '000', '010', '000', '001')]
h2 = hist(M817, H2)
check('lb8.p817.historia2', [r[2] for r in h2] == ['QUIETO', 'ABRIR', 'ABRIR', 'ABRIR', 'CERRAR', 'CERRAR', 'ABRIR', 'ABRIR', 'CERRAR', 'CERRAR', 'QUIETO'])
ok = True
for _ in range(300):    # un ciclo completo siempre termina quieto y no se mueve sin orden
    s_ = [bits('001')]
    if any(r[3] != '00' for r in hist(M817, s_)): ok = False
    r_ = hist(M817, [bits('001'), bits('100')] + [bits('000')] * RNG.randint(0, 5) + [bits('010')] + [bits('000')] * RNG.randint(0, 5) + [bits('001')])
    if r_[-1][2] != 'QUIETO': ok = False
check('lb8.p817.ciclo', ok)
enc817 = {'QUIETO': 0, 'ABRIR': 2, 'CERRAR': 1}
res817, mine817, brow817, k817, s817, no817 = diseno('lb8.p817', M817, enc817, 2, 'JK')
ej('lb8-17', 'Puerta automática con pulsador y topes (autómata «industrial»)', 'Libro · Cap. 8 · P8.17', 'moore,industrial,jk', 'lb8.p817',
   'Una puerta se abre al activar un pulsador $P$. Se abre hasta que el sensor $A$ detecta el tope de apertura; entonces empieza a cerrarse hasta que el sensor $C$ detecta el tope de cierre, y se para. Dos salidas $S_1S_0$ controlan el motor: 00 para, 01 cierra, 10 abre. Las entradas se ordenan $PAC$. Diseña el autómata.',
   '**Los estados de un automatismo coinciden con los estados del aparato**: QUIETO, ABRIR y CERRAR (infinitivos o gerundios: una buena pista). La salida es el propio estado, así que es un Moore. Además, las entradas son **asíncronas** (las genera una persona o un sensor): antes de llegar al autómata se pasan por biestables D con el mismo reloj, que las sincronizan. El reloj despierta al autómata en cada flanco, y si va rápido es casi como si fuera continuo.',
   [('Método de las historias', 'En estos problemas se empieza **contando historias** (secuencias típicas de funcionamiento) y se escribe una tabla paso a paso. Después se completan las transiciones que faltan. Dos consejos del libro: en una historia, dos entradas consecutivas deben diferir en un solo bit (de 010 a 000 a 001, no de 101 a 000), y la transición de llegada a un estado debe **repetirse como lazo** en el estado de destino (si 010 lleva a CERRAR, 010 también mantiene CERRAR).'),
    ('Entradas imposibles', 'Con tres entradas hay 8 combinaciones por estado, pero $A$ y $C$ no pueden valer 1 a la vez (la puerta no está abierta y cerrada a la vez): se descartan 011 y 111. Quedan **seis** transiciones por estado.'),
    ('Completar los estados', 'QUIETO: con 001 se queda; con $P$ (100, 101, 110) se pone a abrir; con 000 ó 010 (en reposo pero sin el sensor de cerrado) pasa a cerrar, para dejar la puerta bien cerrada. ABRIR: con 001 sigue abriendo (extraño pero razonable); con 010 empieza a cerrar (tope de apertura); con 110 (pulsan y ya está abierta) también cierra. CERRAR: con 001 y con 101 llega al tope y queda quieto; con 100 (pulsan mientras cierra) vuelve a abrir; en el resto sigue cerrando.')],
   fsmfig(M817, 'Puerta automática. Entradas $PAC$; el estado muestra la salida') + tabs(M817) + '\n\n**Historia 1** (apertura y cierre completos)\n\n' + tab(['Paso', 'Entrada PAC', 'Estado', 'Salida $S_1S_0$'], h1)
   + '\n\n**Historia 2** (se pulsa $P$ mientras se cierra: vuelve a abrir)\n\n' + tab(['Paso', 'Entrada PAC', 'Estado', 'Salida $S_1S_0$'], h2)
   + '\n\n' + encs(M817, enc817, 2) + '\n\n' + tab(['Función', 'Ecuación (mía, mínima)'], mine817)
   + '\n\nLas dos historias del libro se han reproducido exactamente con la tabla completada, y 300 ciclos aleatorios (abrir, esperar, cerrar, esperar) terminan siempre en QUIETO. El libro no desarrolla las ecuaciones de este ejemplo, que aquí se derivan por el método general, con el código 11 y las entradas imposibles como indiferentes; los resultados se han comprobado contra la tabla.')

# ============================================================ 8.18 limpiaparabrisas (M, P)
M818 = moore(['M', 'P'], {'PARO': [('00', 'PARO'), ('01', 'PARO'), ('10', 'MARCHA'), ('11', 'PARO')],
                          'MARCHA': [('00', 'MARCHA'), ('01', 'PARO'), ('10', 'MARCHA'), ('11', 'PARO')]},
             {'PARO': (0,), 'MARCHA': (1,)})
ok = True
for _ in range(200):
    s_ = stream(40, 2); st_ = 0; exp = []
    for m, p in s_:
        st_ = 0 if p else (1 if m else st_); exp.append(st_)
    if [r[2][0] for r in M818.run(s_)] != exp: ok = False
check('lb8.p818.referencia', ok)
enc818 = {'PARO': 0, 'MARCHA': 1}
bk818 = {'J0': 'M*/P', 'K0': 'P'}
res818, mine818, brow818, *_ = diseno('lb8.p818', M818, enc818, 1, 'JK', bk818, ['q0'])
book('lb8.p818', True)
ej('lb8-18', 'Limpiaparabrisas con pulsadores de marcha y paro', 'Libro · Cap. 8 · P8.18', 'moore,industrial,jk', 'lb8.p818',
   'Un limpiaparabrisas tiene un pulsador de marcha $M$ y otro de paro $P$. Al pulsar $M$ se pone en marcha y sigue funcionando al soltarlo; al pulsar $P$ se para. Si se pulsan los dos a la vez, **prevalece el paro**. Diseña el autómata con un biestable J‑K.',
   '**Dos estados, PARO y MARCHA, y la salida es el estado:** el motor está encendido sólo en MARCHA. La prioridad del paro se refleja en la fila 11 (los dos pulsadores): lleva a PARO desde cualquier estado.',
   [('Tabla de transición', 'Entradas ordenadas $MP$. En PARO: sólo 10 lleva a MARCHA. En MARCHA: sólo 01 y 11 llevan a PARO. En todo lo demás se mantiene el estado.'),
    ('Ecuaciones', 'Con PARO $=0$ y MARCHA $=1$: $J_0$ debe valer 1 sólo desde PARO con $M=1,P=0$, y $K_0$ vale 1 siempre que $P=1$ (el paro manda). Resultado: $J_0=M\\overline{P}$, $K_0=P$, $S_0=q_0$.')],
   fsmfig(M818, 'Limpiaparabrisas (entradas $MP$)') + tabs(M818) + '\n\n' + tab(['Función', 'Ecuación'], brow818)
   + '\n\nComprobadas las ecuaciones del libro en las ocho transiciones, y simulados 200 flujos aleatorios de 40 pares $MP$ contra «el estado es PARO si $P$, si no MARCHA si $M$, si no el anterior».'
   + ojo('El enunciado del libro pide un autómata de Mealy, pero la solución que se desarrolla tiene la salida en el estado y se rotula «resultados del autómata de Moore». Aquí se presenta como Moore, que es lo que de verdad se diseña (la salida es $q_0$ y no depende de las entradas).'))

# ============================================================ 8.19 limpiaparabrisas con detector de reposo (MPR)
M819 = moore(['M', 'P', 'R'], {
    'PARO': [('001', 'PARO'), ('011', 'PARO'), ('100', 'MARCHA'), ('101', 'MARCHA'), ('000', 'MAPA'), ('010', 'MAPA')],
    'MARCHA': [('000', 'MARCHA'), ('001', 'MARCHA'), ('010', 'MAPA'), ('011', 'PARO'), ('100', 'MARCHA'), ('101', 'MARCHA')],
    'MAPA': [('000', 'MAPA'), ('001', 'PARO'), ('010', 'MAPA'), ('011', 'PARO'), ('100', 'MARCHA'), ('101', 'MARCHA')]},
    {'PARO': (0,), 'MARCHA': (1,), 'MAPA': (1,)}, valid=lambda i: not (i[0] and i[1]))
check('lb8.p819.completo', M819.complete())
check('lb8.p819.tres_estados', len(M819.classes()) == 3)
hL = hist(M819, [bits(x) for x in ('001', '101', '100', '000', '001', '000', '010', '000', '001')])
check('lb8.p819.historia_izq', [r[2] for r in hL] == ['PARO', 'MARCHA', 'MARCHA', 'MARCHA', 'MARCHA', 'MARCHA', 'MAPA', 'MAPA', 'PARO'])
hR = hist(M819, [bits(x) for x in ('100', '000', '010', '011')])
check('lb8.p819.historia_der', [r[2] for r in hR] == ['MARCHA', 'MARCHA', 'MAPA', 'PARO'])
ok = True
for _ in range(300):    # sin P, una vez en marcha nunca se para; con P y luego R siempre se acaba en PARO
    s_ = [bits('100')] + [(RNG.randint(0, 1), 0, RNG.randint(0, 1)) for _ in range(20)]
    if any(r[1] != 'MARCHA' for r in M819.run(s_)): ok = False
    s2 = [bits('100'), bits('010')] + [(0, 1, 0)] * RNG.randint(0, 4) + [bits('001')]
    if M819.run(s2)[-1][1] != 'PARO': ok = False
check('lb8.p819.propiedades', ok)
enc819 = {'PARO': 0, 'MARCHA': 1, 'MAPA': 3}
res819, mine819, brow819, *_ = diseno('lb8.p819', M819, enc819, 2, 'JK')
book('lb8.p819', False, 'historia con entradas 010 y 100/110 impresas con el orden de bits cambiado; fila 5 con 010 en vez de 001')
ej('lb8-19', 'Limpiaparabrisas con detector de posición de reposo (3 estados)', 'Libro · Cap. 8 · P8.19', 'moore,industrial,jk', 'lb8.p819',
   'Se mejora el limpiaparabrisas anterior con un detector de reposo $R$ (vale 1 cuando la escobilla está en su posición inicial). Entradas ordenadas $MPR$. Al pulsar $P$ la escobilla **no se detiene donde esté**, sino que termina el recorrido y se para al llegar al reposo. Diseña el autómata con salida de Moore.',
   '**Ahora aparece un estado transitorio:** MAPA («marcha para paro»), en el que la escobilla sigue moviéndose pero ya se ha ordenado parar. MARCHA y PARO son estacionarios; MAPA dura hasta que $R=1$. El motor está activo en MARCHA y en MAPA.',
   [('Por qué no bastan dos estados', 'Con la entrada 001 (reposo, nada pulsado) la escobilla debe **seguir** si estaba en MARCHA (pasa por el reposo en cada ciclo) pero debe **parar** si estaba en MAPA (acaba de llegar al reposo). La misma entrada pide acciones distintas: hace falta memoria, o sea un tercer estado. El algoritmo de particiones lo confirma: MARCHA y MAPA tienen la misma salida pero no son equivalentes.'),
    ('Transiciones', 'MARCHA: $P$ con $R=0$ (010) pasa a MAPA; $P$ con $R=1$ (011) a PARO; el resto sigue en MARCHA. MAPA: llegar al reposo sin $M$ (001, 011) lleva a PARO; si se vuelve a pulsar $M$ (100, 101) vuelve a MARCHA; si no, sigue. PARO: $M$ lleva a MARCHA; si la escobilla no está en reposo (000, 010) pasa a MAPA para volver a él; si lo está, se queda. Las combinaciones 110 y 111 ($M$ y $P$ a la vez) se consideran imposibles.'),
    ('Codificación', 'PARO $=00$, MARCHA $=01$, MAPA $=11$ (el 10 es indiferente). Con esa elección la salida es $S=q_0$.')],
   fsmfig(M819, 'Limpiaparabrisas con reposo. Entradas $MPR$') + tabs(M819) + '\n\n' + encs(M819, enc819, 2) + '\n\n' + tab(['Función', 'Ecuación (mía, mínima)'], mine819)
   + '\n\n**Historia izquierda** (marcha, pasa por el reposo sin parar, se pulsa $P$ y se detiene al llegar al reposo)\n\n' + tab(['Paso', 'Entrada MPR', 'Estado', 'Salida'], hL)
   + '\n\n**Historia derecha** (marcha y paro pulsando $P$ hasta el reposo)\n\n' + tab(['Paso', 'Entrada MPR', 'Estado', 'Salida'], hR)
   + '\n\nSimulados 300 casos aleatorios: sin pulsar $P$ la escobilla no se detiene nunca, y tras pulsar $P$ siempre acaba parada al llegar al reposo. El libro no incluye ecuaciones de este ejemplo; las de arriba son las mínimas que salen del método y se han comprobado contra la tabla.'
   + ojo('En la historia de la izquierda, el paso 5 («tope») aparece con la entrada 010; debe ser 001: la escobilla **pasa por el reposo sin parar**, y con 010 iría a MAPA, lo que choca con el paso 7. En la de la derecha, «seguir pulsando $P$» y «reposo con $P$ pulsado» aparecen como 100 y 110; con el orden $MPR$ que usa el libro son 010 y 011. Por último, el estado del paso 9 se rotula QUIETO y es PARO.'))

# ============================================================ 8.20 motor con activación al soltar (Moore, 4 estados)
M820 = moore(['M', 'P'], {'P': [('00', 'P'), ('01', 'P'), ('10', 'PM')], 'PM': [('00', 'M'), ('10', 'PM')],
                          'M': [('00', 'M'), ('01', 'MP'), ('10', 'M')], 'MP': [('00', 'P'), ('01', 'MP')]},
             {'P': (0,), 'PM': (0,), 'M': (1,), 'MP': (1,)}, valid=lambda i: i != (1, 1))
check('lb8.p820.cuatro_estados', len(M820.classes()) == 4)
h820 = hist(M820, [bits(x) for x in ('00', '10', '00', '01', '00')])
check('lb8.p820.historia', [(r[2], r[3]) for r in h820] == [('P', '0'), ('PM', '0'), ('M', '1'), ('MP', '1'), ('P', '0')])
enc820 = {'P': 0, 'PM': 1, 'M': 2, 'MP': 3}
bk820 = {'J1': '/M*q0', 'K1': '/P*q0', 'J0': 'P*q1 + M*/q1', 'K0': '/M*/P'}
res820, mine820, brow820, *_ = diseno('lb8.p820', M820, enc820, 2, 'JK', bk820, ['q1'])
M820b = moore(['P'], {'P': [('0', 'P'), ('1', 'PM')], 'PM': [('1', 'PM'), ('0', 'M')], 'M': [('0', 'M'), ('1', 'MP')], 'MP': [('1', 'MP'), ('0', 'P')]},
              {'P': (0,), 'PM': (0,), 'M': (1,), 'MP': (1,)})
h820b = hist(M820b, [(0,), (1,), (0,), (1,), (0,)])
check('lb8.p820b.historia', [(r[2], r[3]) for r in h820b] == [('P', '0'), ('PM', '0'), ('M', '1'), ('MP', '1'), ('P', '0')])
enc820b = {'P': 0, 'PM': 1, 'M': 2, 'MP': 3}
bk820b = {'J1': '/P*q0', 'K1': '/P*q0', 'J0': 'P', 'K0': '/P'}
res820b, mine820b, brow820b, *_ = diseno('lb8.p820b', M820b, enc820b, 2, 'JK', bk820b, ['q1'])
okk = True
for _ in range(200):
    s_ = []
    for j in range(RNG.randint(1, 8)):
        s_ += [(1,)] * RNG.randint(1, 4) + [(0,)] * RNG.randint(1, 4)
    o = [r[2][0] for r in M820b.run(s_)]
    cnt = 0; prev = 0
    for t, x in enumerate(s_):
        if prev == 1 and x[0] == 0: cnt += 1
        prev = x[0]
        if o[t] != cnt % 2: okk = False
check('lb8.p820b.alternancia', okk)
book('lb8.p820b', False, 'historia: paso 4 anota MP con salida 0 (es 1) y el paso 5 anota soltar con 1 (es 0)')
ej('lb8-20', 'Motor que se activa al soltar el pulsador (Moore, 4 estados)', 'Libro · Cap. 8 · P8.20', 'moore,industrial,jk', 'lb8.p820',
   'Un motor se controla con un pulsador de marcha $M$ y otro de paro $P$, pero la orden **sólo se ejecuta al soltar** el pulsador (en el paso de 1 a 0). Diseña el autómata. Después hazlo con un **único pulsador** que alterne marcha y paro, también al soltar.',
   '**Hay que distinguir «pulsado» de «ya soltado».** Con la orden al soltar, cada pulsación produce dos situaciones distintas: mientras se mantiene el pulsador (el motor aún no ha cambiado) y después de soltarlo (ya cambió). Cuatro estados: P (parado), PM (parado, $M$ pulsado y pendiente de soltar), M (en marcha) y MP (en marcha, $P$ pulsado y pendiente).',
   [('Transiciones', 'P: con $M$ pulsado (10) pasa a PM; con $P$ (01) no hace nada. PM: mientras $M$ siga pulsado se queda; al soltarlo (00) pasa a M. M: con $P$ (01) pasa a MP; MP: al soltar $P$ (00) vuelve a P. Dos combinaciones, 11 y las que supondrían soltar uno y pulsar el otro en el mismo ciclo, no pueden ocurrir (indiferentes).'),
    ('Salida', 'El motor está activo en M y en MP, y parado en P y PM. Con el código P $=00$, PM $=01$, M $=10$, MP $=11$ la salida es sencillamente $S_0=q_1$.'),
    ('Un solo pulsador', 'Con el mismo cuarteto de estados, pero con una entrada: PM y MP **se alternan** cada vez que se pulsa. La tabla codificada es la de un contador que cambia con el flanco de bajada, y las ecuaciones tienen $J_1=K_1$ (el bit alto conmuta).'),
    ('¿Y con dos estados?', 'Con sólo «parado/marcha», la entrada 1 debería llevar de un estado al otro; pero entonces, mientras el pulsador siga a 1, el estado **conmutaría en cada flanco de reloj** (oscilaría). Hace falta recordar que «esta pulsación ya se ha contado», y eso son los otros dos estados.')],
   '**Dos pulsadores** (entradas $MP$; «—» = combinación imposible)\n\n' + fsmfig(M820, 'Motor con dos pulsadores. Estado: salida') + tabs(M820) + '\n\n' + encs(M820, enc820, 2) + '\n\n' + tab(['Función', 'Ecuación'], brow820)
   + '\n\nHistoria completa (reposo, pulso de $M$, soltar, pulso de $P$, soltar):\n\n' + tab(['Paso', 'Entrada $MP$', 'Estado', 'Salida'], h820)
   + '\n\n**Un solo pulsador** (entrada $P$)\n\n' + fsmfig(M820b, 'Motor con un pulsador (alterna al soltar)') + tabs(M820b) + '\n\n' + encs(M820b, enc820b, 2) + '\n\n' + tab(['Función', 'Ecuación'], brow820b)
   + '\n\nHistoria:\n\n' + tab(['Paso', 'Entrada $P$', 'Estado', 'Salida'], h820b)
   + '\n\nLas ecuaciones del libro se han comprobado en todas las transiciones definidas de las dos versiones.'
   + ojo('En la tabla de historias del problema con un solo pulsador, el paso 4 anota el estado MP con salida 0 y el paso 5 anota la entrada «soltar» como 1. El estado MP tiene salida 1 (el motor sigue en marcha mientras se mantiene el pulsador) y «soltar» es la entrada 0. La tabla de arriba es la correcta y reproduce el funcionamiento.'))
