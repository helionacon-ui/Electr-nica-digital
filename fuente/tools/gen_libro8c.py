# -*- coding: utf-8 -*-
# Problemas 8.21 a 8.35 (se ejecuta dentro de gen_libro8.py)
def rr(a, b): return RNG.randint(a, b)
def runs_stream(lo=2, hi=4, n=8, first=0):
    s = []; v = first
    for _ in range(n):
        s += [(v,)] * rr(lo, hi); v ^= 1
    return s
def fl(M, seq, st=None): return [r[1] for r in M.run(seq, st)]
def outs_s(M, seq, st=None): return [''.join(map(str, r[2])) for r in M.run(seq, st)]

# ============================================================ 8.21 depósito con dos bombas (Moore, 6 estados)
M821 = moore(['I', 'S'], {
    'UB1': [('00', 'B12a'), ('10', 'B1'), ('11', 'UB1')], 'B1': [('00', 'B12a'), ('10', 'B1'), ('11', 'UB2')],
    'B12a': [('00', 'B12a'), ('10', 'B2'), ('11', 'UB1')], 'UB2': [('00', 'B12b'), ('10', 'B2'), ('11', 'UB2')],
    'B2': [('00', 'B12b'), ('10', 'B2'), ('11', 'UB1')], 'B12b': [('00', 'B12b'), ('10', 'B1'), ('11', 'UB2')]},
    {'UB1': (0, 0), 'B1': (0, 1), 'B12a': (1, 1), 'UB2': (0, 0), 'B2': (1, 0), 'B12b': (1, 1)}, valid=lambda i: i != (0, 1))
check('lb8.p821.completo', M821.complete())
check('lb8.p821.seis_estados', len(M821.classes()) == 6)
hl = fl(M821, [bits(x) for x in ('10', '11', '11', '10', '00', '10', '11')])
check('lb8.p821.historia_izq', hl == ['B1', 'UB2', 'UB2', 'B2', 'B12b', 'B1', 'UB2'], str(hl))
hr = fl(M821, [bits(x) for x in ('00', '10', '00', '10', '11')], 'B1')
check('lb8.p821.historia_der', hr == ['B12a', 'B2', 'B12b', 'B1', 'UB2'], str(hr))
ok = True
for _ in range(200):
    L = 9; st = 'UB1'; last = None; prev_in = None
    for _ in range(80):
        i = (int(L >= 3), int(L >= 7))
        n = M821.nxt(st, i); o = M821.outs[n]
        if o == (1, 1) and i != (0, 0): ok = False
        if o == (0, 0) and i != (1, 1): ok = False
        if st in ('UB1', 'UB2') and n in ('B1', 'B2') and n == last: ok = False
        if n in ('B1', 'B2'): last = n
        st = n; L = max(0, min(10, L + RNG.choice([-1, 0, 1])))
check('lb8.p821.alternancia', ok)
enc821 = {'UB1': 0, 'B1': 1, 'B2': 2, 'B12a': 3, 'UB2': 4, 'B12b': 7}
res821, mine821, brow821, *_ = diseno('lb8.p821', M821, enc821, 3, 'JK')
ej('lb8-21', 'Depósito con dos bombas que se turnan', 'Libro · Cap. 8 · P8.21', 'moore,industrial,jk', 'lb8.p821',
   'Un depósito se llena con dos bombas, $B_1$ y $B_2$, y tiene dos sensores de nivel: $I$ (inferior) y $S$ (superior), con las entradas ordenadas $IS$ (la combinación 01 es imposible: nivel alto sin nivel bajo). Con el nivel por encima de $S$ las bombas están paradas. Al bajar de $S$ se pone en marcha **una** bomba; si el nivel sigue bajando hasta quedar por debajo de $I$, se conectan **las dos**. Las bombas deben **turnarse** para desgastarse por igual. Diseña el autómata.',
   '**Para turnarse hay que recordar cuál fue la última en trabajar.** Eso duplica los estados «paradas» y «las dos en marcha»: hay que saber qué bomba toca después. Salen seis estados de Moore.',
   [('Estados', 'UB1 y UB2: bombas paradas con el depósito lleno; la siguiente bomba que se use será $B_1$ o $B_2$. B1 y B2: sólo trabaja esa bomba. B12a y B12b: trabajan las dos; hay dos copias porque al subir el nivel se debe continuar con la bomba **distinta** de la última usada.'),
    ('Funcionamiento', 'De UB1 con $IS=10$ (nivel intermedio) se pasa a B1; desde B1, al llenarse (11), se pasa a UB2, de modo que la próxima vez toque $B_2$. Si con B1 el nivel baja de $I$ (00), se pasa a B12a; al volver a 10 sigue sólo $B_2$ (la que descansó) y al llenarse se vuelve a UB1.'),
    ('Salidas', 'Las dos salidas $B_2B_1$ son 00 en UB1/UB2, 01 en B1, 10 en B2 y 11 en B12a/B12b.'),
    ('¿Bastan cuatro estados?', 'No. Con sólo «paradas», «$B_1$», «$B_2$» y «las dos» no se sabe cuál fue la última bomba en trabajar, y no se podría asegurar el turno. El algoritmo de particiones separa los seis estados.')],
   fsmfig(M821, 'Depósito con dos bombas (entradas $IS$). Estado: $B_2B_1$') + tabs(M821) + '\n\n' + encs(M821, enc821, 3) + '\n\n' + tab(['Función', 'Ecuación (mía, mínima)'], mine821)
   + '\n\nSe reproducen las dos historias del libro: (izquierda) UB1, B1, UB2, UB2, B2, B12b, B1, UB2; (derecha) B1, B12a, B2, B12b, B1, UB2. Además, se ha simulado el depósito con un nivel que sube y baja de uno en uno, durante 200 trayectorias de 80 pasos, y se verifica que (i) las dos bombas sólo trabajan juntas con el nivel por debajo de $I$, (ii) están paradas sólo con el nivel lleno y (iii) la bomba que se usa al bajar de $S$ es siempre distinta de la última que trabajó sola. El libro desarrolla este ejemplo con el diagrama; las ecuaciones de aquí son las del método.')

# ============================================================ 8.22 puertas de cristal (Moore, entradas PCA)
M822 = moore(['P', 'C', 'A'], {
    'CDA': [('000', 'CDO'), ('001', 'CDO'), ('010', 'CDA'), ('100', 'ABDO'), ('101', 'ABTA'), ('110', 'ABDO')],
    'ABDO': [('000', 'ABDO'), ('010', 'ABDO'), ('100', 'ABDO'), ('110', 'ABDO'), ('101', 'ABTA'), ('001', 'CDO')],
    'ABTA': [('101', 'ABTA'), ('001', 'CDO'), ('000', 'CDO'), ('010', 'CDO'), ('100', 'ABDO'), ('110', 'ABDO')],
    'CDO': [('000', 'CDO'), ('001', 'CDO'), ('010', 'CDA'), ('101', 'ABTA'), ('100', 'ABDO'), ('110', 'ABDO')]},
    {'CDA': (0, 0), 'ABDO': (0, 1), 'ABTA': (0, 0), 'CDO': (1, 0)}, valid=lambda i: not (i[1] and i[2]))
check('lb8.p822.completo', M822.complete())
hi = fl(M822, [bits(x) for x in ('010', '110', '100', '000', '001', '000', '010')])
hc = fl(M822, [bits(x) for x in ('100', '100', '101', '001', '000', '010')])
hd = fl(M822, [bits(x) for x in ('100', '101', '001', '100', '101', '001', '010')])
check('lb8.p822.historias', hi == ['CDA', 'ABDO', 'ABDO', 'ABDO', 'CDO', 'CDO', 'CDA'] and hc == ['ABDO', 'ABDO', 'ABTA', 'CDO', 'CDO', 'CDA']
      and hd == ['ABDO', 'ABTA', 'CDO', 'ABDO', 'ABTA', 'CDO', 'CDA'], str((hi, hc, hd)))
ok = True
for _ in range(300):
    s_ = [(RNG.randint(0, 1), RNG.randint(0, 1), 0) for _ in range(10)]
    if any(r[1] != 'ABDO' for r in M822.run(s_, 'ABDO')): ok = False          # abriendo: completa la apertura
    s2 = [(1, RNG.randint(0, 1), 0), ]
    if M822.run(s2, 'CDO')[-1][1] not in ('ABDO',): ok = False                 # cerrando y aparece alguien: reabre
    if M822.run([(1, 0, 1)] * RNG.randint(1, 6), 'ABTA')[-1][1] != 'ABTA': ok = False   # con gente permanece abierta
check('lb8.p822.propiedades', ok)
enc822 = {'CDA': 0, 'ABDO': 1, 'CDO': 2, 'ABTA': 3}
res822, mine822, brow822, *_ = diseno('lb8.p822', M822, enc822, 2, 'JK')
ej('lb8-22', 'Puertas de cristal de un edificio (Moore, entradas PCA)', 'Libro · Cap. 8 · P8.22', 'moore,industrial,jk', 'lb8.p822',
   'Una puerta de cristal tiene un detector de persona $P$ y dos topes: abierta $A$ y cerrada $C$ (entradas ordenadas $PCA$). Debe cumplir: si llega una persona, se abre; si ha empezado a abrirse, **completa la apertura**; mientras haya gente, **permanece abierta**; si se está cerrando y aparece una persona, **vuelve a abrirse**. Sale una orden de dos bits (cerrando, abriendo).',
   '**Cuatro estados de la puerta:** CDA (cerrada, parada), ABDO (abriéndose), ABTA (abierta, parada) y CDO (cerrándose). Las salidas valen 00, 01, 00 y 10: CDA y ABTA son estacionarios y no se mueve el motor. $C=A=1$ es imposible (011 y 111 se descartan).',
   [('Lo que dice el enunciado', 'CDA con persona (100, 110) → ABDO. ABDO se mantiene con cualquier combinación sin $A$ (completa la apertura) y pasa a ABTA con $A=1$ y gente (101) o a CDO con $A=1$ sin gente (001). ABTA con gente y abierta (101) se queda; sin gente (001) pasa a CDO. CDO termina en CDA al llegar a $C$ (010); con persona vuelve a ABDO (100, 110) o a ABTA (101).'),
    ('Lo que hay que completar', 'El dibujo no cubre todas las combinaciones. Las completo así: en CDA, sin $C$ (000) o con $A$ (001), la puerta no está donde debe: pasa a CDO (cerrar) como en el problema 8.17; en ABTA, si $A$ cae a 0 con gente (100, 110) se reabre (ABDO) y sin gente (000, 010) se cierra (CDO); CDO con 110 reabre (ABDO).')],
   fsmfig(M822, 'Puertas de cristal (entradas $PCA$). Estado: salida (cerrando, abriendo)') + tabs(M822) + '\n\n' + encs(M822, enc822, 2) + '\n\n' + tab(['Función', 'Ecuación (mía, mínima)'], mine822)
   + '\n\n**Historias**\n\n' + tab(['Historia', 'Entradas $PCA$ (desde el estado inicial)', 'Estados'],
       [['Ciclo completo', '010, 110, 100, 000, 001, 000, 010', ' → '.join(hi)], ['Con gente al final', '100, 100, 101, 001, 000, 010', ' → '.join(hc)], ['Alguien aparece al cerrar', '100, 101, 001, 100, 101, 001, 010', ' → '.join(hd)]])
   + '\n\nEl libro presenta este ejemplo sólo con el diagrama de estados y sus comentarios (sin ecuaciones); la tabla completa y las ecuaciones son las del método, y se han comprobado frente a las historias y a tres propiedades simuladas (abriendo no se detiene, cerrando con persona reabre, abierta con gente permanece abierta).')

# ============================================================ 8.23 desvío de trenes
M823a = moore(['E1', 'E0'], {'NADA': [('00', 'NADA'), ('10', 'ENTRA')], 'ENTRA': [('10', 'ENTRA'), ('00', 'VIAA'), ('11', 'VIAB')],
                            'VIAA': [('00', 'VIAA'), ('01', 'SALEA')], 'SALEA': [('01', 'SALEA'), ('00', 'NADA')],
                            'VIAB': [('01', 'VIAB'), ('11', 'VIAB'), ('00', 'NADA')]},
              {'NADA': (1, 0), 'ENTRA': (1, 0), 'VIAA': (1, 0), 'SALEA': (1, 0), 'VIAB': (0, 1)})
M823b = moore(['E1', 'E0'], {'VIAA': [('00', 'VIAA'), ('01', 'VIAA'), ('10', 'VIAA'), ('11', 'VIAB')], 'VIAB': [('00', 'VIAA'), ('01', 'VIAB'), ('11', 'VIAB')]},
              {'VIAA': (1, 0), 'VIAB': (0, 1)})
def passage(kind):
    if kind == 's': return ['10'] * rr(1, 3) + ['00'] * rr(1, 3) + ['01'] * rr(1, 3) + ['00'] * rr(1, 3)
    return ['10'] * rr(1, 3) + ['11'] * rr(1, 3) + ['01'] * rr(1, 3) + ['00'] * rr(1, 3)
ok = True
for _ in range(300):
    seq = ['00'] * rr(1, 3)
    for _ in range(rr(1, 5)): seq += passage(RNG.choice('sl'))
    sq = [bits(x) for x in seq]
    if outs_s(M823a, sq) != outs_s(M823b, sq): ok = False
check('lb8.p823.equivalentes_en_trenes', ok)
hl = [bits(x) for x in ('00', '10', '11', '01', '00')]; hs = [bits(x) for x in ('00', '10', '00', '01', '00')]
check('lb8.p823.historias', fl(M823a, hl) == ['NADA', 'ENTRA', 'VIAB', 'VIAB', 'NADA'] and fl(M823a, hs) == ['NADA', 'ENTRA', 'VIAA', 'SALEA', 'NADA']
      and outs_s(M823b, hl) == ['10', '10', '01', '01', '10'] and outs_s(M823b, hs) == ['10'] * 5)
enc823 = {'VIAA': 0, 'VIAB': 1}
bk823 = {'J0': 'E1*E0', 'K0': '/E0'}
res823, mine823, brow823, *_ = diseno('lb8.p823', M823b, enc823, 1, 'JK', bk823, ['/q0', 'q0'])
fb = check_realization(M823b, enc823, 1, bk823, 'JK', ['q0', '/q0'])
check('lb8.p823.salidas_impresas_fallan', len(fb) >= 1 and all(f[0] == 'out' for f in fb), str(fb))
book('lb8.p823', False, 'salidas A=q0, B=/q0 impresas al revés respecto a VIAA=0 con salida 10')
ej('lb8-23', 'Desvío de trenes: un tren corto o uno largo', 'Libro · Cap. 8 · P8.23', 'moore,industrial,jk,reduccion', 'lb8.p823',
   'En una vía hay un desvío con dos ramales: $A$ (corto) y $B$ (largo). Dos sensores, $E_1$ a la entrada y $E_0$ a la salida del tramo de aguja (entradas ordenadas $E_1E_0$), dicen por dónde va el tren: si **sólo $E_1$** está activo y luego se libera, el tren es corto y pasa por $A$; si **$E_1$ y $E_0$ están activos a la vez**, el tren es largo y debe ir por $B$. La salida $AB$ posiciona la aguja: 10 es el ramal $A$ y 01 el $B$. Por defecto, la aguja está en $A$.',
   '**Dos soluciones: la «natural» y la mínima.** La primera sigue el recorrido de un tren y tiene cinco estados; pero en realidad lo único que importa es **dónde está la aguja**, y eso sólo necesita saber si hay un tren largo cruzando. Esa idea da dos estados y un único biestable.',
   [('Primera solución: cinco estados', 'NADA (sin trenes), ENTRA (el tren acaba de entrar), VIAA (tren corto, sale por $A$), SALEA (saliendo) y VIAB (tren largo). Las dos historias del libro se recorren como sigue: corto, NADA→ENTRA→VIAA→SALEA→NADA; largo, NADA→ENTRA→VIAB→VIAB→NADA. Los saltos no previstos («—») no pueden ocurrir físicamente y son indiferentes.'),
    ('Segunda solución: dos estados', 'VIAA (salida 10) y VIAB (01). Sólo se pasa a VIAB cuando se ven **los dos sensores a la vez** (11); se vuelve a VIAA cuando ya no hay tren (00). Con un biestable $q_0$ ($0$ = VIAA, $1$ = VIAB): $J_0=E_1E_0$ y $K_0=\\overline{E_0}$, y las salidas $A=\\overline{q_0}$, $B=q_0$.'),
    ('Equivalencia', 'Para todos los pasos de trenes posibles (cortos y largos, con pausas) la aguja se coloca **exactamente igual** en las dos soluciones: se han comparado 300 secuencias aleatorias de hasta cinco trenes.'),
    ('Una pega del diseño', 'Tras pasar un tren largo, en cuanto los dos sensores quedan libres la aguja vuelve a $A$, aunque el tren aún pudiera estar saliendo del ramal. El libro sugiere dejar la salida en $B$ un poco más; es un ajuste de diseño, no un fallo.')],
   '**Cinco estados** (« — »: no puede ocurrir)\n\n' + fsmfig(M823a, 'Desvío: cinco estados. Estado: salida $AB$') + tabs(M823a)
   + '\n\n**Dos estados**\n\n' + fsmfig(M823b, 'Desvío: dos estados') + tabs(M823b) + '\n\n' + tab(['Función', 'Ecuación'], brow823)
   + '\n\nEn ambas el comportamiento del libro (historias de arriba) se reproduce.'
   + ojo('Las ecuaciones de salida impresas en el libro son $A=q_0$ y $B=\\overline{q_0}$. Eso contradice la propia codificación (VIAA $=0$ debe dar $AB=10$, es decir $A=\\overline{q_0}$ y $B=q_0$). Las ecuaciones de excitación $J_0$ y $K_0$ son correctas; las salidas están intercambiadas. Con las salidas impresas, el sistema colocaría la aguja en $B$ cuando no hay tren.'))

# ============================================================ 8.24 secador de manos
M824 = moore(['P', 'D'], {'PARO': [('00', 'PARO'), ('01', 'PARO'), ('10', 'PARO'), ('11', 'MARCHA')],
                          'MARCHA': [('00', 'PARO'), ('01', 'MARCHA'), ('10', 'PARO'), ('11', 'MARCHA')]}, {'PARO': (0,), 'MARCHA': (1,)})
ok = True
for _ in range(200):
    s_ = stream(40, 2); st_ = 0; ex = []
    for p, d in s_:
        st_ = int(d and (p or st_)); ex.append(st_)
    if [r[2][0] for r in M824.run(s_)] != ex: ok = False
check('lb8.p824.referencia', ok)
hI = fl(M824, [bits(x) for x in ('00', '10', '11', '01', '00')]); hD = fl(M824, [bits(x) for x in ('11', '10', '00')])
check('lb8.p824.historias', hI == ['PARO', 'PARO', 'MARCHA', 'MARCHA', 'PARO'] and hD == ['MARCHA', 'PARO', 'PARO'])
enc824 = {'PARO': 0, 'MARCHA': 1}
bk824 = {'J0': 'P*D', 'K0': '/D'}
res824, mine824, brow824, *_ = diseno('lb8.p824', M824, enc824, 1, 'JK', bk824, ['q0'])
ej('lb8-24', 'Secador de manos con pulsador y detector de presencia', 'Libro · Cap. 8 · P8.24', 'moore,industrial,jk', 'lb8.p824',
   'Un secador de manos arranca cuando se pulsa un pulsador $P$ **y** el detector de presencia $D$ ve unas manos, y sigue funcionando mientras $D$ siga detectando. Entradas ordenadas $PD$. Diseña el autómata con un biestable J‑K.',
   '**Dos estados, PARO y MARCHA**, y el motor es el estado. La condición para arrancar es un AND ($P\\cdot D$) y la de seguir es sólo $D$: el pulsador deja de importar una vez en marcha.',
   [('Tabla', 'En PARO sólo $PD=11$ lleva a MARCHA. En MARCHA se continúa con $D=1$ (01 y 11) y se para con $D=0$ (00 y 10), aunque se esté pulsando.'),
    ('Ecuaciones', '$J_0=P\\cdot D$ (arranque), $K_0=\\overline D$ (se apaga al dejar de detectar), $S_0=q_0$.')],
   fsmfig(M824, 'Secador (entradas $PD$)') + tabs(M824) + '\n\n' + tab(['Función', 'Ecuación'], brow824)
   + '\n\nLas dos historias del libro (arranque y parada normales; salir sin soltar el pulsador) se reproducen. Simulados 200 flujos de 40 pares $PD$ contra «el estado siguiente es $D\\cdot(P+\\text{estado})$».')

# ============================================================ 8.25 contador mod 4 con pulsador
r825 = {}
for n in range(4): r825['C%d' % n] = [('0', 'C%d' % n), ('1', 'C%dT' % ((n + 1) % 4))]
for n in range(4): r825['C%dT' % n] = [('0', 'C%d' % n), ('1', 'C%dT' % n)]
M825 = moore(['E0'], r825, {s: ((int(s[1]) >> 1) & 1, int(s[1]) & 1) for s in r825})
ok = True
for _ in range(300):
    s_ = stream(40); prev = 0; cnt = 0; ex = []
    for (e,) in s_:
        if e and not prev: cnt += 1
        prev = e; ex.append(cnt % 4)
    if [2 * r[2][0] + r[2][1] for r in M825.run(s_)] != ex: ok = False
check('lb8.p825.referencia', ok)
check('lb8.p825.ocho_estados', len(M825.classes()) == 8)
enc825 = {'C%d' % n: n for n in range(4)}; enc825.update({'C%dT' % n: 4 + n for n in range(4)})
bk825 = {'J2': 'E0', 'K2': '/E0', 'J1': 'E0*/q2*q0', 'K1': 'E0*/q2*q0', 'J0': 'E0*/q2', 'K0': 'E0*/q2'}
res825, mine825, brow825, *_ = diseno('lb8.p825', M825, enc825, 3, 'JK', bk825, ['q1', 'q0'])
check('lb8.p825.mismas', same_funcs(res825, bk825, M825, 3) is True)
book('lb8.p825', False, 'diagrama con C2T rotulado 01 (es 10)')
ej('lb8-25', 'Contador módulo 4 que cuenta al pulsar (8 estados)', 'Libro · Cap. 8 · P8.25', 'moore,contador,industrial,jk', 'lb8.p825',
   'Un contador módulo 4 debe avanzar **un solo paso cada vez que se pulsa** un pulsador $E_0$ (en el flanco de subida de la pulsación), por mucho que dure la pulsación. La salida son dos bits con la cuenta. Diseña el autómata de Moore.',
   '**Un pulsador humano dura muchos ciclos de reloj**, así que hay que distinguir «he contado ya esta pulsación» de «aún no». Por cada valor de la cuenta hay un estado estacionario $C_n$ (pulsador suelto) y otro transitorio $C_nT$ (pulsador mantenido tras haber contado). Son ocho estados.',
   [('Transiciones', '$C_n\\xrightarrow{0}C_n$; $C_n\\xrightarrow{1}C_{n+1}T$ (cuenta al pulsar y pasa a esperar). $C_nT\\xrightarrow{1}C_nT$ (mantiene) y $C_nT\\xrightarrow{0}C_n$ (se suelta).'),
    ('Salida', 'Tanto $C_n$ como $C_nT$ dan el valor $n$.'),
    ('Codificación y ecuaciones', 'Los estacionarios son 000 a 011 y los transitorios 100 a 111 ($q_2$ = «ya contado»). $J_2=E_0$, $K_2=\\overline{E_0}$ (es una copia retrasada del pulsador). Los otros dos biestables **conmutan** sólo en el instante de la pulsación, es decir cuando $E_0=1$ y $q_2=0$: $J_0=K_0=E_0\\overline{q_2}$ y $J_1=K_1=E_0\\overline{q_2}q_0$ (el bit alto cambia si el bajo es 1).')],
   fsmfig(M825, 'Contador con pulsador. Etiqueta: $E_0$; estado: cuenta') + tabs(M825) + '\n\n' + encs(M825, enc825, 3) + '\n\n' + tab(['Función', 'Ecuación'], brow825)
   + '\n\nMi minimización coincide con la del libro como función. Simulados 300 flujos aleatorios de 40 entradas contra «número de flancos de subida, módulo 4».'
   + ojo('En el diagrama del libro el estado $C_2T$ aparece rotulado con la salida 01; debe ser 10, como indican la tabla de estados y el funcionamiento (cuenta 2). Se ha comprobado que con 01 el contador daría 1 en vez de 2 en ese estado.'))

# ============================================================ 8.26 caja fuerte (Moore, 8 estados)
M826 = moore(['P1', 'P0'], {
    'Q0': [('00', 'Q0'), ('10', 'Q1'), ('01', 'ALARM')], 'Q1': [('10', 'Q1'), ('00', 'S1')],
    'S1': [('00', 'S1'), ('10', 'Q3'), ('01', 'ALARM')], 'Q3': [('10', 'Q3'), ('00', 'S11')],
    'S11': [('00', 'S11'), ('01', 'Q6'), ('10', 'ALARM')], 'Q6': [('01', 'Q6'), ('00', 'S110')],
    'S110': [('XX', 'S110')], 'ALARM': [('XX', 'ALARM')]},
    {'Q0': (0, 0), 'Q1': (0, 0), 'S1': (0, 0), 'Q3': (0, 0), 'S11': (0, 0), 'Q6': (0, 0), 'S110': (1, 0), 'ALARM': (0, 1)}, valid=lambda i: i != (1, 1))
ok = True
KEY = [1, 1, 0]
for _ in range(400):
    presses = [RNG.choice([1, 1, 0]) if RNG.random() < .7 else RNG.randint(0, 1) for _ in range(rr(1, 6))]
    if RNG.random() < .4: presses = KEY[:rr(1, 3)] if RNG.random() < .5 else KEY + [RNG.randint(0, 1)]
    s_ = []
    for b in presses: s_ += [(1, 0) if b else (0, 1)] * rr(1, 3) + [(0, 0)] * rr(1, 3)
    # esperado
    bad = False; i = 0
    for b in presses[:3]:
        if b != KEY[i]: bad = True; break
        i += 1
    exp = 'alarm' if bad else ('open' if len(presses) >= 3 else 'none')
    o = M826.run(s_)[-1][2]
    got = {(0, 1): 'alarm', (1, 0): 'open', (0, 0): 'none'}[o]
    if got != exp: ok = False
check('lb8.p826.codigo', ok)
check('lb8.p826.ocho_estados', len(M826.classes()) == 8)
hh = fl(M826, [bits(x) for x in ('10', '00', '10', '00', '01', '00')])
check('lb8.p826.historia', hh == ['Q1', 'S1', 'Q3', 'S11', 'Q6', 'S110'], str(hh))
enc826 = {'Q0': 0, 'Q1': 1, 'S1': 2, 'Q3': 3, 'S11': 4, 'Q6': 5, 'S110': 6, 'ALARM': 7}
res826, mine826, brow826, *_ = diseno('lb8.p826', M826, enc826, 3, 'JK')
ej('lb8-26', 'Caja fuerte con combinación 1‑1‑0 y alarma', 'Libro · Cap. 8 · P8.26', 'moore,industrial,jk', 'lb8.p826',
   'Una caja fuerte tiene dos pulsadores, $P_1$ y $P_0$ (entradas ordenadas $P_1P_0$, nivel alto al pulsar). Se abre al introducir la **combinación 1, 1, 0** (pulsar $P_1$, pulsar $P_1$, pulsar $P_0$; entre una pulsación y la siguiente hay que soltar). Cualquier pulsación equivocada dispara la **alarma**. Salidas $CA$: $C$ abre la caja, $A$ activa la alarma. Un RESET asíncrono la devuelve al estado inicial. Pulsar los dos a la vez es imposible.',
   '**Cada pulsación correcta es un par de estados**: «el botón está apretado» (esperando soltar) y «ya se ha aceptado» (esperando el siguiente). Eso da una cadena $Q_0\\to Q_1\\to S_1\\to Q_3\\to S_{11}\\to Q_6\\to S_{110}$, y de cada estado de espera un botón equivocado lleva a ALARM. Tanto la apertura como la alarma son **absorbentes**: sólo se sale con el RESET.',
   [('Cadena de aciertos', 'En $Q_0$ se espera un 1 (10 → $Q_1$); mientras se mantiene (10) se queda; al soltar (00) pasa a $S_1$ («un 1 aceptado»). Lo mismo para el segundo 1 ($S_1\\to Q_3\\to S_{11}$). En $S_{11}$ se espera el 0 (01 → $Q_6$), y al soltar se llega a $S_{110}$ (abierta, salida 10).'),
    ('Errores', 'En $Q_0$ y en $S_1$ una pulsación de $P_0$ (01) es un error; en $S_{11}$ lo es una de $P_1$ (10). Esos tres saltos van a ALARM (salida 01).'),
    ('Estados de la cadena', 'Los estados $Q_1$, $Q_3$ y $Q_6$ son los de «botón apretado». Con las entradas posibles, no se puede pasar de 10 a 01 de golpe (habría que soltar primero), por lo que algunas casillas quedan como indiferentes.')],
   fsmfig(M826, 'Caja fuerte (entradas $P_1P_0$). Estado: salida $CA$') + tabs(M826) + '\n\n' + encs(M826, enc826, 3) + '\n\n' + tab(['Función', 'Ecuación (mía, mínima)'], mine826)
   + '\n\nHistoria de apertura correcta: pulsar 1, soltar, pulsar 1, soltar, pulsar 0, soltar → $Q_1,S_1,Q_3,S_{11},Q_6,S_{110}$. Simulados 400 intentos aleatorios (combinación correcta, incompleta, con errores y con pulsaciones de más): el resultado siempre es «abierta» sólo con 1‑1‑0 y «alarma» con cualquier otro primer error. El libro presenta este ejemplo con el diagrama y las historias; las ecuaciones de arriba son las del método.')

# ============================================================ 8.27 juego de reflejos
M827 = moore(['E1', 'E0'], {'INICIO': [('00', 'INICIO'), ('10', 'GA'), ('01', 'GB'), ('11', 'GT')], 'GA': [('XX', 'GA')], 'GB': [('XX', 'GB')], 'GT': [('XX', 'GT')]},
             {'INICIO': (0, 0), 'GA': (1, 0), 'GB': (0, 1), 'GT': (1, 1)})
ok = True
for _ in range(300):
    s_ = [(0, 0)] * rr(0, 4) + [RNG.choice([(1, 0), (0, 1), (1, 1)])] + stream(6, 2)
    first = [x for x in s_ if x != (0, 0)][0]
    if M827.run(s_)[-1][2] != first: ok = False
check('lb8.p827.primero_gana', ok)
enc827 = {'INICIO': 0, 'GB': 1, 'GA': 2, 'GT': 3}
res827, mine827, brow827, *_ = diseno('lb8.p827', M827, enc827, 2, 'JK')
M827b = moore(['I', 'J', 'E1', 'E0'], {
    'REPOS': [('1XXX', 'INICIO'), ('0XXX', 'REPOS')],
    'INICIO': [('1XXX', 'INICIO'), ('0000', 'INICIO'), ('0100', 'JUGAN'), ('0010', 'PIERA'), ('0001', 'PIERB'), ('0011', 'PIERT'), ('0110', 'GANA'), ('0101', 'GANB'), ('0111', 'GANT')],
    'JUGAN': [('1XXX', 'INICIO'), ('0X00', 'JUGAN'), ('0X10', 'GANA'), ('0X01', 'GANB'), ('0X11', 'GANT')],
    'PIERA': [('1XXX', 'INICIO'), ('0XXX', 'PIERA')], 'PIERB': [('1XXX', 'INICIO'), ('0XXX', 'PIERB')], 'PIERT': [('1XXX', 'INICIO'), ('0XXX', 'PIERT')],
    'GANA': [('1XXX', 'INICIO'), ('0XXX', 'GANA')], 'GANB': [('1XXX', 'INICIO'), ('0XXX', 'GANB')], 'GANT': [('1XXX', 'INICIO'), ('0XXX', 'GANT')]},
    {'REPOS': (0, 0, 0), 'INICIO': (0, 0, 0), 'JUGAN': (1, 0, 0), 'PIERA': (0, 0, 1), 'PIERB': (0, 1, 0), 'PIERT': (0, 1, 1), 'GANA': (1, 1, 0), 'GANB': (1, 0, 1), 'GANT': (1, 1, 1)})
check('lb8.p827b.completo', M827b.complete())
pre = ['0000', '1000', '0000', '0100', '0000']
hA = hist(M827b, [bits(x) for x in pre + ['0010', '0000', '1000']]); hB = hist(M827b, [bits(x) for x in pre + ['0001', '1000']])
hP = hist(M827b, [bits(x) for x in pre[:3] + ['0010', '1000']]); hT = hist(M827b, [bits(x) for x in pre + ['0011', '1000']])
check('lb8.p827b.historias', [r[2] for r in hA] == ['REPOS', 'INICIO', 'INICIO', 'JUGAN', 'JUGAN', 'GANA', 'GANA', 'INICIO']
      and [r[3] for r in hA] == ['000', '000', '000', '100', '100', '110', '110', '000'] and hB[5][3] == '101' and hB[6][2] == 'INICIO'
      and hP[3][2] == 'PIERA' and hP[3][3] == '001' and hT[5][2] == 'GANT' and hT[5][3] == '111' and hT[6][2] == 'INICIO',
      str((hA, hB, hP, hT)))
ok = True
for _ in range(300):
    st = RNG.choice(M827b.states[1:])
    if M827b.run([(1, RNG.randint(0, 1), RNG.randint(0, 1), RNG.randint(0, 1))], st)[0][1] != 'INICIO': ok = False
check('lb8.p827b.reinicio', ok)
book('lb8.p827', False, 'erratas en salidas de las historias y del diagrama')
ej('lb8-27', 'Juego de reflejos entre dos jugadores (con juez)', 'Libro · Cap. 8 · P8.27', 'moore,industrial,jk', 'lb8.p827',
   'Dos jugadores, $A$ y $B$, tienen un pulsador cada uno ($E_1$ y $E_0$). Gana el que pulse primero; si pulsan a la vez, hay empate. Salidas $S_1S_0$: 10 gana $A$, 01 gana $B$, 11 empate. Diseña el autómata. Después mejóralo: un **juez** da la orden de salida con un pulsador $J$ (hay una luz $L_J$ encendida durante la partida), quien pulse **antes** de la orden pierde, y un pulsador de **inicio** $I$ prepara una nueva partida.',
   '**Versión simple: cuatro estados.** INICIO y tres estados absorbentes (GA, GB, GT) que registran el resultado. Su problema es doble: sólo se reinicia con RESET y se puede hacer trampa pulsando antes de empezar. La versión con juez lo resuelve añadiendo estados.',
   [('Versión simple', 'INICIO/00: con 00 espera; con 10 gana A, con 01 gana B, con 11 empate. Una vez decidido, el resultado se mantiene (la «X» de la flecha: cualquier entrada). Con el código INICIO $=00$, GB $=01$, GA $=10$, GT $=11$ las salidas son $S=q$ (sin lógica de salida).'),
    ('Versión con juez', 'Entradas $I\\,J\\,E_1E_0$ y salidas $L_JS_1S_0$. Estados: REPOS (espera el primer inicio), INICIO (preparado, sin luz), JUGAN (juez ha dado la orden, luz encendida), PIERA y PIERB (un jugador pulsó antes de la orden y **pierde**: gana el otro), PIERT (los dos pulsaron antes), y GANA, GANB y GANT (resultado válido).'),
    ('Reglas', 'En INICIO: sólo $J=1$ solo (0100) pasa a JUGAN; si un jugador pulsa sin que el juez haya dado la orden, pierde (PIERA con 0010, PIERB con 0001, PIERT con 0011); si la orden y la pulsación coinciden se acepta la pulsación (0110, 0101, 0111). En JUGAN el primero que pulse gana (0X10, 0X01, 0X11). Cualquier estado de resultado se mantiene hasta que $I=1$ lo devuelve a INICIO.'),
    ('Sobre REPOS', 'REPOS sólo se usa después del RESET: se sale con $I=1$ y no se vuelve a entrar, porque los reinicios llevan a INICIO. El libro comenta que podría eliminarse.')],
   '**Versión simple**\n\n' + fsmfig(M827, 'Juego simple (entradas $E_1E_0$)') + tabs(M827) + '\n\n' + encs(M827, enc827, 2) + '\n\n' + tab(['Función', 'Ecuación (mía)'], mine827)
   + '\n\n**Versión con juez** (9 estados; entradas $I\\,J\\,E_1E_0$; estado: salida $L_JS_1S_0$)\n\n' + fsmfig(M827b, 'Juego con juez') + tabs(M827b)
   + '\n\nHistoria completa del libro: ' + ' → '.join(r[2] for r in hA) + ', con salidas ' + ', '.join(r[3] for r in hA) + '. Gana B: ' + ', '.join(r[3] for r in hB) + '. Pulsa A antes de la orden: ' + hP[3][2] + ' con salida ' + hP[3][3] + '. Empate: ' + hT[5][2] + ' con salida ' + hT[5][3] + '. Se ha comprobado que desde cualquier estado $I=1$ lleva a INICIO. El libro no desarrolla ecuaciones de la versión con juez (cuatro biestables), que quedan como ejercicio.'
   + ojo('En las historias y en el diagrama de la versión con juez hay varias erratas: (1) la historia anota «Gana B» con salida 110; la salida de GANB es 101. (2) El diagrama rotula PIER A con salida 010 y PIER B con 001, al revés que la historia y el texto: si $A$ se adelanta, gana $B$, y el código es 001 para PIERA. (3) La última historia anota el reinicio con entrada 0000; debe ser 1000 (el pulsador de inicio). Aquí se usan las salidas correctas.'))

# ============================================================ 8.28 alarma de peso (Moore, 8 estados)
low = ['0XX', '100']
def r828(n5, n6): return [(p, 'INICI') for p in low] + [('101', n5), ('110', n6), ('111', 'P7')]
M828 = moore(['E2', 'E1', 'E0'], {'INICI': r828('P51', 'P61'), 'P51': r828('P52', 'P61'), 'P52': r828('P53', 'P61'), 'P53': r828('P54', 'P61'), 'P54': r828('P54', 'P61'),
                                  'P61': r828('P51', 'P62'), 'P62': r828('P51', 'P62'), 'P7': r828('P51', 'P61')},
             {'INICI': (0,), 'P51': (0,), 'P52': (0,), 'P53': (0,), 'P54': (1,), 'P61': (0,), 'P62': (1,), 'P7': (1,)})
check('lb8.p828.completo', M828.complete())
check('lb8.p828.ocho_estados', len(M828.classes()) == 8)
ok = True
for _ in range(400):
    w = [RNG.choice([5, 5, 5, 6, 6, 7, RNG.randint(0, 4)]) for _ in range(40)]
    s_ = [((x >> 2) & 1, (x >> 1) & 1, x & 1) for x in w]
    ex = []; run = 0
    for t, x in enumerate(w):
        run = run + 1 if t and w[t - 1] == x else 1
        ex.append(int((x == 7) or (x == 6 and run >= 2) or (x == 5 and run >= 4)))
    if [r[2][0] for r in M828.run(s_)] != ex: ok = False
check('lb8.p828.referencia', ok)
enc828 = {'INICI': 0, 'P51': 1, 'P52': 2, 'P53': 3, 'P54': 4, 'P61': 5, 'P62': 6, 'P7': 7}
bk828 = {'J0': 'E2*E0*/q2 + E2*E0*q1 + E2*E1*/q1 + E2*E1*/q2', 'K0': '/E0*q2*/q1 + /E1*/q2 + /E1*/E0 + /E2',
         'J1': 'E2*E0*/q2*q0 + E2*E1*q2*q0 + E2*E1*E0', 'K1': '/E0*/q2 + /E1*q0 + /E1*q2 + /E2 + /E0*q0',
         'J2': 'E2*E0*q1*q0 + E2*E1', 'K2': '/E1*/E0 + /E1*q0 + /E1*q1 + /E2'}
res828, mine828, brow828, *_ = diseno('lb8.p828', M828, enc828, 3, 'JK', bk828, ['q2*/q0 + q2*q1'])
hh = fl(M828, [bits(x) for x in ('000', '011', '001', '101', '101', '101', '101', '101', '010')])
check('lb8.p828.historia', hh == ['INICI', 'INICI', 'INICI', 'P51', 'P52', 'P53', 'P54', 'P54', 'INICI'], str(hh))
ej('lb8-28', 'Alarma de sobrecarga de un ascensor (peso en serie… de tres bits)', 'Libro · Cap. 8 · P8.28', 'moore,industrial,jk,contador', 'lb8.p828',
   'Un sensor de peso entrega el peso del ascensor en tres bits $E_2E_1E_0$ (valor de 0 a 7). Debe sonar una **alarma** si el peso es **5 durante al menos 4 pulsos de reloj consecutivos**, **6 durante al menos 2** o **7 durante al menos 1**. Cualquier otro valor (0 a 4) borra la cuenta. Diseña el autómata de Moore.',
   '**El autómata cuenta cuántos pulsos seguidos lleva el mismo peso crítico.** Para el 5 se cuenta hasta 4, para el 6 hasta 2 y el 7 se detecta ya a la primera, así que hay ocho estados: INICI (nada), P51 a P54 (lleva 1, 2, 3 y 4 o más pulsos con peso 5), P61 y P62 (1 y 2 o más con peso 6) y P7. La alarma está en P54, P62 y P7.',
   [('Transiciones', 'Con peso de 0 a 4 se vuelve siempre a INICI. Con peso 5 se avanza P51→P52→P53→P54 (que se mantiene); desde cualquier otro estado (incluidos P6x y P7) se empieza una cuenta nueva en P51. Con peso 6 se avanza P61→P62 y desde el resto se entra en P61. Con peso 7 se va a P7 desde cualquier estado.'),
    ('Qué significa «seguidos»', 'Es la cuenta de **pulsos consecutivos con exactamente el mismo peso**: si entre dos pesos 5 aparece un 6, la cuenta de 5 se pierde (y al volver el 5 se parte de 1). Es una decisión de diseño razonable, pero conviene saberla: tres pesos 5 seguidos de un 6 no dan alarma por ninguno de los dos.'),
    ('Codificación', 'Natural: INICI $=000$, P51 $=001$, …, P54 $=100$, P61 $=101$, P62 $=110$, P7 $=111$. La salida es $S_0=q_2\\overline{q_0}+q_2q_1$.')],
   tabs(M828) + '\n\n' + tab(['Función', 'Ecuación (libro)'], brow828) + '\n\nSalida: $S_0=q_2\\overline{q_0}+q_2q_1$. ' + cmpt(res828, bk828, M828, 3)
   + '\n\nLas ecuaciones del libro (suma de productos) se han comprobado en las 64 transiciones: todas reproducen la tabla. Se ha simulado con 400 secuencias de 40 pesos, muchas de ellos críticos, contra el modelo directo «longitud de la racha de pesos iguales». También se reproduce la historia del libro: tres pesos bajos, luego cinco veces el 5 (con alarma al cuarto) y vuelta a INICI con el 2.')

# ============================================================ 8.29 dispensador de leche (Moore, 11 estados)
r829 = {'INICIO': [('0', 'INICIO'), ('1', 'TRANS')], 'TRANS': [('1', 'TRANS'), ('0', 'D1')]}
for k in range(1, 5): r829['D%d' % k] = [('X', 'D%d' % (k + 1) if k < 4 else 'C1')]
for k in range(1, 5): r829['C%d' % k] = [('X', 'C%d' % (k + 1) if k < 4 else 'INICIO')]
o829 = {'INICIO': (0, 0, 0, 0), 'TRANS': (0, 0, 0, 0)}
for k in range(1, 5): o829['D%d' % k] = (1, 1, 0, 1); o829['C%d' % k] = (0, 0, 1, 1)
M829 = moore(['P'], r829, o829)
check('lb8.p829.diez_estados', len(M829.states) == 10 and len(M829.classes()) == 10)
ok = True
for _ in range(200):
    s_ = [(0,)] * rr(0, 3) + [(1,)] * rr(1, 4) + [(0,)] + [(RNG.randint(0, 1),) for _ in range(8)] + [(0,)] * 2
    o = outs_s(M829, s_)
    k0 = next(i for i, x in enumerate(s_) if x == (1,)); k1 = next(i for i in range(k0, len(s_)) if s_[i] == (0,))
    ex = ['0000'] * k1 + ['1101'] * 4 + ['0011'] * 4 + ['0000'] * (len(s_) - k1 - 8)
    if o != ex: ok = False
check('lb8.p829.secuencia', ok)
ej('lb8-29', 'Dispensador de leche con calentador (Moore, 10 estados)', 'Libro · Cap. 8 · P8.29', 'moore,industrial,secuencial', 'lb8.p829',
   'Una máquina dispensa leche cuando se pulsa un pulsador $P$, **al soltarlo**. Durante cuatro segundos sale la leche y se recarga el depósito; después, durante otros cuatro segundos, se calienta la leche. En las ocho fases la máquina está ocupada y **no atiende nuevas pulsaciones**. Cuatro salidas $D\\,R\\,C\\,L_R$: dispensador, recargador, calentador y led rojo de ocupado ($L_R$, a 1 durante las ocho fases). Hay un reloj de 1 Hz. Diseña el autómata de Moore.',
   '**Es una secuencia temporizada disparada por un pulsador:** una espera, una confirmación de que se soltó y ocho pasos de reloj fijos. Con un reloj de 1 Hz cada paso dura un segundo, así que se necesitan 4 estados para la fase de dispensar y 4 para la de calentar. Más los dos de espera: **10 estados**.',
   [('Esperar y confirmar', 'INICIO (todo a 0): con $P=1$ pasa a TRANS; TRANS espera a que se suelte ($P=0$) y entonces arranca el ciclo. Esto evita arrancar al pulsar y permite pulsaciones largas.'),
    ('Dispensar y calentar', 'D1, D2, D3 y D4 con salidas 1101 ($D=R=L_R=1$), y C1, C2, C3 y C4 con salidas 0011 ($C=L_R=1$). En cada uno se pasa al siguiente con cualquier entrada (la «X»: no se atiende el pulsador durante el ciclo). Tras C4 se vuelve a INICIO.'),
    ('Reducción', 'No se puede fusionar ningún par: los ocho estados del ciclo están a distancias distintas del final, y INICIO y TRANS difieren en cómo reaccionan a $P$. El algoritmo de particiones confirma que el autómata es mínimo.')],
   tabs(M829)
   + '\n\nEl libro presenta sólo el diagrama y los comentarios, sin ecuaciones (cuatro biestables para 10 estados). Se ha simulado el funcionamiento: tras soltar el pulsador salen exactamente cuatro ciclos 1101, luego cuatro 0011 y se vuelve a 0000, sin importar lo que valga $P$ durante esos ocho ciclos (200 casos aleatorios).')

# ============================================================ 8.30 barrera de garaje (Moore, entradas SE SS SA SC)
M830 = moore(['SE', 'SS', 'SA', 'SC'], {
    'REPOS': [('1XXX', 'ABDO'), ('0XXX', 'REPOS')], 'ABDO': [('X1XX', 'CDO'), ('XX1X', 'ABTO'), ('XXXX', 'ABDO')],
    'ABTO': [('X1XX', 'CDO'), ('XXXX', 'ABTO')], 'CDO': [('XXX1', 'REPOS'), ('XXXX', 'CDO')]},
    {'REPOS': (0, 0), 'ABDO': (0, 1), 'ABTO': (0, 0), 'CDO': (1, 0)}, valid=lambda i: not (i[0] and i[1]) and not (i[2] and i[3]))
check('lb8.p830.completo', M830.complete())
hI = fl(M830, [bits(x) for x in ('0001', '1001', '1000', '0000', '0100', '0100', '0000', '0001')])
hDd = fl(M830, [bits(x) for x in ('0001', '1001', '1000', '0000', '0000', '0000', '0000', '0010', '0110', '0100', '0000', '0001')])
check('lb8.p830.historias', hI == ['REPOS', 'ABDO', 'ABDO', 'ABDO', 'CDO', 'CDO', 'CDO', 'REPOS'] and hDd[7] == 'ABTO' and hDd[8] == 'CDO' and hDd[-1] == 'REPOS', str((hI, hDd)))
enc830 = {'REPOS': 0, 'ABDO': 1, 'CDO': 2, 'ABTO': 3}
res830, mine830, brow830, *_ = diseno('lb8.p830', M830, enc830, 2, 'JK')
book('lb8.p830', False, 'rótulos 1010/0010 del dibujo incoherentes con las historias (0010 y 0110)')
ej('lb8-30', 'Barrera de un garaje (Moore, entradas SE SS SA SC)', 'Libro · Cap. 8 · P8.30', 'moore,industrial,jk', 'lb8.p830',
   'Una barrera de garaje tiene cuatro sensores, ordenados $S_E\\,S_S\\,S_A\\,S_C$: coche en la **entrada** (antes de la barrera), coche en la **salida** (ya pasó), barrera **abierta** y barrera **cerrada**. La orden al motor son dos bits $M_1M_0$: 00 parado, 01 abre, 10 cierra. Debe abrirse cuando llega un coche, esperar abierta hasta que haya pasado y cerrarse. $S_E$ y $S_S$ no pueden valer 1 a la vez, ni $S_A$ y $S_C$.',
   '**Cuatro estados de la barrera:** REPOS (cerrada y parada), ABDO (abriéndose), ABTO (abierta, parada, esperando que el coche pase) y CDO (cerrándose). De las 16 entradas quedan 9 posibles: se descartan 11XX y XX11.',
   [('Transiciones que dibuja el libro', 'REPOS con $S_E=1$ pasa a ABDO; ABDO se mantiene (1001, 1000, 0000) hasta que se completa la apertura (1010 → ABTO) o el coche ya ha pasado (0100, 0110 → CDO); ABTO se mantiene con 1010; CDO se mantiene (0010, 0110, 0100) y llega a REPOS con 0001.'),
    ('Cómo se completan', 'ABDO: si $S_S=1$ (el coche ya pasó) cierra; si no, con $S_A=1$ queda abierta. ABTO: sale a CDO cuando el coche pasa ($S_S=1$). CDO: con $S_C=1$ llega a REPOS. REPOS: sólo $S_E$ la saca de ahí. Así quedan cubiertas las nueve combinaciones posibles de cada estado y se reproducen las dos historias del libro.')],
   fsmfig(M830, 'Barrera de garaje (entradas $S_ES_SS_AS_C$)') + tabs(M830) + '\n\n' + encs(M830, enc830, 2) + '\n\n' + tab(['Función', 'Ecuación (mía, mínima)'], mine830)
   + '\n\nHistoria 1: ' + ', '.join(hI) + '. Historia 2 (coche que se adelanta con la barrera a medias, abierta del todo, pasa y cierra): ' + ', '.join(hDd) + '.'
   + '\n\nEl libro no da ecuaciones de este problema (sólo diagrama y comentarios). Las de arriba se derivan con el método general y se han comprobado.'
   + ojo('Las flechas del diagrama no son coherentes con las historias del propio libro: el dibujo rotula con 1010 la salida de ABDO a ABTO y con 0010 la de ABTO a CDO, pero en las historias se llega a ABTO con 0010 (paso 10) y se pasa a CDO con 0110 (paso 11). Aquí se usa la tabla que cumple las historias (la que sale arriba).'))

# ============================================================ 8.31 calificaciones en serie (Moore, 10 → 9 estados)
M831 = moore(['E'], {
    'INICIO': [('0', 'SUSP1'), ('1', 'EMPIE')], 'SUSP1': [('X', 'SUSP2')], 'SUSP2': [('X', 'SUSP3')], 'SUSP3': [('0', 'SUSP1'), ('1', 'EMPIE')],
    'EMPIE': [('0', 'APRO1'), ('1', 'SIGUE')], 'APRO1': [('X', 'APRO2')], 'APRO2': [('0', 'SUSP1'), ('1', 'EMPIE')],
    'SIGUE': [('0', 'NOTAB'), ('1', 'SOBRE')], 'NOTAB': [('0', 'SUSP1'), ('1', 'EMPIE')], 'SOBRE': [('0', 'SUSP1'), ('1', 'EMPIE')]},
    {'INICIO': (0, 0, 0), 'SUSP1': (0, 0, 0), 'SUSP2': (0, 0, 0), 'SUSP3': (0, 0, 0), 'EMPIE': (0, 0, 0), 'APRO1': (0, 0, 0), 'APRO2': (1, 0, 0), 'SIGUE': (0, 0, 0), 'NOTAB': (0, 1, 0), 'SOBRE': (0, 0, 1)})
cl831 = sorted(map(sorted, M831.classes()))
check('lb8.p831.fusion', len(cl831) == 9 and ['INICIO', 'SUSP3'] in cl831, str(cl831))
M831r = quotient(M831)
ok = True
for _ in range(300):
    ex_ = []; s_ = []
    for _ in range(rr(1, 6)):
        b = [RNG.randint(0, 1) for _ in range(3)]; s_ += [(x,) for x in b]
        ex_ += ['000', '000', '100' if b[:2] == [1, 0] else '010' if b[:2] == [1, 1] and b[2] == 0 else '001' if b == [1, 1, 1] else '000']
    if outs_s(M831, s_) != ex_ or outs_s(M831r, s_) != ex_: ok = False
check('lb8.p831.referencia', ok)
ej('lb8-31', 'Calificaciones recibidas en serie (Moore, 10 → 9 estados)', 'Libro · Cap. 8 · P8.31', 'moore,reduccion,serie', 'lb8.p831',
   'Un sistema de corrección entrega la nota de cada examen en **tres bits seguidos** por una línea serie $E$: el primero dice si se supera la parte básica (BAS), el segundo si se llega a notable (NOT) y el tercero si se llega a sobresaliente (SOB). Interpretación: $0XX$ suspenso, $10X$ aprobado, $110$ notable y $111$ sobresaliente. Hay tres luces $L_AL_NL_S$ (aprobado, notable, sobresaliente) que se encienden **al llegar el tercer bit**. Diseña el autómata de Moore y reduce sus estados.',
   '**Hay que contar tres bits aunque no importen.** En un suspenso, el primer bit (0) decide, pero hay que dejar pasar los otros dos antes de aceptar el examen siguiente; por eso aparecen cadenas de estados «de relleno» (SUSP1, SUSP2, SUSP3 y APRO1, APRO2).',
   [('Estados', 'Suspenso: INICIO, SUSP1, SUSP2, SUSP3 (cuentan 3 bits sin salida). Aprobado: EMPIE, APRO1, APRO2 (luz $L_A$). Notable/sobresaliente: SIGUE (ha llegado «11»), NOTAB ($L_N$) y SOBRE ($L_S$). Desde los estados finales (SUSP3, APRO2, NOTAB, SOBRE) el siguiente bit es el primero de otro examen.'),
    ('Reducción', 'INICIO y SUSP3 son **equivalentes**: la misma salida (000) y los mismos siguientes (0→SUSP1, 1→EMPIE). Se fusionan y quedan **nueve estados** (cuatro biestables). El algoritmo de particiones no encuentra más.')],
   '**Con diez estados**\n\n' + tabs(M831) + '\n\n**Reducido a nueve** (INICIO y SUSP3 fusionados)\n\n' + fsmfig(M831r, 'Calificaciones (9 estados). Etiqueta: $E$; estado: $L_AL_NL_S$') + tabs(M831r)
   + '\n\nSimulados 300 flujos de entre 1 y 6 exámenes de tres bits aleatorios: las luces se encienden sólo tras el tercer bit y con el resultado correcto; las dos versiones se comportan igual. El libro desarrolla este ejemplo con diagrama y sin ecuaciones.')

# ============================================================ 8.32 reloj CK' con primer flanco ascendente
M832 = moore(['CLEAR', 'CK'], {
    'INICIO': [('0X', 'INICIO'), ('1X', 'ACTIV')], 'ACTIV': [('01', 'ACTIV'), ('1X', 'ACTIV'), ('00', 'CK0')],
    'CK0': [('00', 'CK0'), ('01', 'CK1'), ('1X', 'ACTIV')], 'CK1': [('01', 'CK1'), ('00', 'CK0'), ('1X', 'ACTIV')]},
    {'INICIO': (0,), 'ACTIV': (0,), 'CK0': (0,), 'CK1': (1,)})
check('lb8.p832.completo', M832.complete())
ok = True
for _ in range(400):
    s_ = [(RNG.choice([0, 0, 0, 1]), RNG.randint(0, 1)) for _ in range(40)]
    started = False; arm = False; ex = []
    for cl, ck in s_:
        if cl: started = True; arm = False; ex.append(0)
        elif not started: ex.append(0)
        else:
            if ck == 0: arm = True
            ex.append(ck if arm else 0)
    if [r[2][0] for r in M832.run(s_)] != ex: ok = False
check('lb8.p832.referencia', ok)
ok = True
for _ in range(300):
    s_ = [(1, RNG.randint(0, 1))] + [(0, RNG.randint(0, 1)) for _ in range(30)]
    o = [r[2][0] for r in M832.run(s_)]
    ch = [(a, b) for a, b in zip(o, o[1:]) if a != b]
    if ch and ch[0] != (0, 1): ok = False
check('lb8.p832.primer_flanco_ascendente', ok)
ej('lb8-32', 'Generar un reloj CK′ cuyo primer flanco tras CLEAR sea ascendente', 'Libro · Cap. 8 · P8.32', 'moore,reloj,industrial', 'lb8.p832',
   'Se quiere generar a partir de un reloj $CK$ y una señal $CLEAR$ un reloj $CK\'$ que, al activarse $CLEAR$ (nivel alto), se ponga a 0 y, tras liberarse, **empiece siempre con un flanco ascendente**: nunca debe aparecer un flanco o un pulso incompleto aunque $CLEAR$ se suelte con $CK=1$. Entradas $CLEAR\\,CK$, salida $CK\'$. Diseña el autómata.',
   '**Hay que esperar a ver un 0 de $CK$ antes de seguir al reloj.** Si $CLEAR$ se libera cuando $CK$ vale 1 y se copiara $CK$ sin más, saldría un pulso recortado. Basta un estado de espera (ACTIV) que no copie $CK$ hasta que $CK=0$.',
   [('Estados', 'INICIO: sin activar (sólo $CLEAR=1$ lo saca de ahí). ACTIV: $CLEAR$ aplicado; espera un 0 de $CK$ (con $CK=1$ se queda). CK0 y CK1: reproducen $CK$ (salida 0 y 1).'),
    ('Transiciones', 'ACTIV con $CLEAR=0$ y $CK=0$ pasa a CK0. CK0 pasa a CK1 con $CK=1$ y CK1 a CK0 con $CK=0$. En CK0, CK1 y ACTIV, $CLEAR=1$ lleva (y mantiene) en ACTIV, con la salida a 0.'),
    ('Garantía', 'Como se llega a CK0 antes que a CK1, el primer cambio de la salida es siempre $0\\to1$, un flanco ascendente. Se ha comprobado en 300 secuencias aleatorias.'),
    ('Ojo con el uso', 'Una señal generada así no debería usarse como reloj de otros biestables: es una señal derivada de un autómata y rompe el principio de no mezclar relojes. Es preferible usar el $CK$ original con una entrada de habilitación (**ENABLE**).')],
   fsmfig(M832, 'Generador de CK′ (entradas $CLEAR\\,CK$). Estado: salida $CK\'$') + tabs(M832)
   + '\n\nSimulados 400 flujos de 40 pares $CLEAR\\,CK$ contra el modelo «0 hasta que haya habido un CLEAR y después un 0 de $CK$; a partir de ahí, la salida es $CK$». El libro presenta sólo el diagrama y los comentarios.')

# ============================================================ 8.33 un pulso de un ciclo por cada pulso de entrada
M833a = moore(['E0'], {'INICIO': [('0', 'INICIO'), ('1', 'PULSO')], 'PULSO': [('X', 'FINAL')], 'FINAL': [('1', 'FINAL'), ('0', 'INICIO')]},
              {'INICIO': (0,), 'PULSO': (1,), 'FINAL': (0,)})
M833b = moore(['E0'], {'INICIO': [('0', 'INICIO'), ('1', 'EMPIE')], 'EMPIE': [('1', 'EMPIE'), ('0', 'PULSO')], 'PULSO': [('X', 'INICIO')]},
              {'INICIO': (0,), 'EMPIE': (0,), 'PULSO': (1,)})
M833c = moore(['E0'], {'INICIO': [('0', 'INICIO'), ('1', 'PULS1')], 'PULS1': [('X', 'MANT')], 'MANT': [('0', 'PULS0'), ('1', 'MANT')], 'PULS0': [('X', 'INICIO')]},
              {'INICIO': (0,), 'PULS1': (1,), 'MANT': (0,), 'PULS0': (1,)})
# la tabla del libro de la opción 3 es (INICI:(INICI,PULS1) PULS1:(MANT,MANT) MANT:(PULS0,MANT) PULS0:(INICI,INICI))
ok = [True, True, True]
for _ in range(400):
    s_ = runs_stream(2, 4, rr(2, 8), RNG.randint(0, 1)); e = [x[0] for x in s_]
    prev = [0] + e[:-1]
    ex1 = [int(a == 1 and p == 0) for a, p in zip(e, prev)]
    ex2 = [int(a == 0 and p == 1) for a, p in zip(e, prev)]
    ex3 = [int(a != p) for a, p in zip(e, prev)]
    if [r[2][0] for r in M833a.run(s_)] != ex1: ok[0] = False
    if [r[2][0] for r in M833b.run(s_)] != ex2: ok[1] = False
    if [r[2][0] for r in M833c.run(s_)] != ex3: ok[2] = False
check('lb8.p833.subida', ok[0]); check('lb8.p833.bajada', ok[1]); check('lb8.p833.ambos', ok[2])
bk833 = [({'J1': 'q0', 'K1': '/E0', 'J0': 'E0*/q1', 'K0': '1'}, ['q0'], {'INICIO': 0, 'PULSO': 1, 'FINAL': 2}, M833a),
         ({'J1': '/E0*q0', 'K1': '1', 'J0': 'E0*/q1', 'K0': '/E0'}, ['q1'], {'INICIO': 0, 'EMPIE': 1, 'PULSO': 2}, M833b),
         ({'J1': 'q0', 'K1': 'q0', 'J0': 'E0*/q1 + /E0*q1', 'K0': '1'}, ['q0'], {'INICIO': 0, 'PULS1': 1, 'MANT': 2, 'PULS0': 3}, M833c)]
rows833 = []
for k, (bk, so, enc, M) in enumerate(bk833, 1):
    rs, mn, br, *_ = diseno('lb8.p833_%d' % k, M, enc, 2, 'JK', bk, so); rows833.append((br, enc, M))
e_demo = ''.join(str(x) for x in [0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]); sd = [(int(c),) for c in e_demo]
o1 = ''.join(str(r[2][0]) for r in M833a.run(sd)); o2 = ''.join(str(r[2][0]) for r in M833b.run(sd)); o3 = ''.join(str(r[2][0]) for r in M833c.run(sd))
book('lb8.p833', False, 'diagrama con PULS1 de salida 0 (debe ser 1)')
ej('lb8-33', 'Un pulso de un ciclo de reloj por cada pulso de entrada (3 variantes)', 'Libro · Cap. 8 · P8.33', 'moore,detector-de-flanco,jk,cronograma', 'lb8.p833',
   'Una señal $E_0$, manual y mucho más lenta que el reloj (cada nivel dura **más de un periodo** de reloj), debe generar **un pulso de exactamente un ciclo de reloj**. Diséñalo de tres maneras: (1) que el pulso aparezca al **subir** $E_0$, (2) al **bajar**, (3) en **los dos** flancos (dos pulsos por cada pulso de entrada). Autómatas de Moore con J‑K.',
   '**Es un detector de flancos síncrono.** Un flanco no es un nivel: es un cambio. El autómata debe recordar dos cosas: que ya vio el flanco (para no repetir el pulso aunque $E_0$ siga a 1) y, en los dos últimos casos, qué nivel tenía $E_0$.',
   [('Opción 1: flanco de subida', 'INICIO (espera un 1) → PULSO (salida 1, dura un ciclo) → FINAL (espera a que $E_0$ baje, sin repetir). Código 00, 01, 10 y $S_0=q_0$. Ecuaciones: $J_1=q_0$, $K_1=\\overline{E_0}$, $J_0=E_0\\overline{q_1}$, $K_0=1$.'),
    ('Opción 2: flanco de bajada', 'INICIO → EMPIE (hay un 1; espera que baje) → PULSO (salida 1) → INICIO. Código 00, 01, 10 y $S_0=q_1$. Ecuaciones: $J_1=\\overline{E_0}q_0$, $K_1=1$, $J_0=E_0\\overline{q_1}$, $K_0=\\overline{E_0}$.'),
    ('Opción 3: los dos flancos', 'INICIO → PULS1 (salida 1) → MANT (mantiene el nivel alto) → PULS0 (salida 1, tras caer) → INICIO. Código 00, 01, 10 y 11, con $S_0=q_0$. Ecuaciones: $J_1=K_1=q_0$, $J_0=E_0\\overline{q_1}+\\overline{E_0}q_1$, $K_0=1$.'),
    ('Por qué se exige un nivel mayor que un periodo', 'El autómata sólo mira $E_0$ una vez por ciclo. Si el pulso de entrada durara menos de un ciclo, podría pasar inadvertido; y si los niveles duran un solo ciclo, las transiciones de espera (FINAL, PULSO, …) no llegan a ver el cambio siguiente. Con niveles de al menos dos ciclos funcionan las tres.')],
   '**Opción 1: flanco de subida**\n\n' + fsmfig(M833a, 'Pulso en el flanco de subida') + tabs(M833a) + '\n\n' + encs(M833a, rows833[0][1], 2) + '\n\n' + tab(['Función', 'Ecuación'], rows833[0][0])
   + '\n\n**Opción 2: flanco de bajada**\n\n' + fsmfig(M833b, 'Pulso en el flanco de bajada') + tabs(M833b) + '\n\n' + tab(['Función', 'Ecuación'], rows833[1][0])
   + '\n\n**Opción 3: los dos flancos**\n\n' + fsmfig(M833c, 'Pulso en los dos flancos') + tabs(M833c) + '\n\n' + tab(['Función', 'Ecuación'], rows833[2][0])
   + '\n\n**Cronograma** de las tres opciones con la misma entrada\n\n' + cron([['E₀', e_demo], ['S↑', o1], ['S↓', o2], ['S↑↓', o3]], '', 34, 10)
   + '\n\nLas ecuaciones del libro se han comprobado en todas las transiciones de las tres variantes, y se han simulado 400 secuencias con niveles de 2 a 4 ciclos contra «el estado actual difiere del anterior» (y sus dos casos particulares).'
   + ojo('En el diagrama del libro de la opción 3, el estado PULS1 aparece con salida 0. Debe ser 1: sin ella no habría pulso en el flanco de subida, y contradice la tabla de estados codificada y el cronograma ($S_0=q_0$).'))

# ============================================================ 8.34 transmisor serie
M834 = moore(['P', 'E1', 'E0'], {
    'INICIO': [('0XX', 'INICIO'), ('1XX', 'TRANS')], 'TRANS': [('1XX', 'TRANS'), ('0XX', 'EMPIE')], 'EMPIE': [('X0X', 'UNO0'), ('X1X', 'UNO1')],
    'UNO0': [('XX0', 'DOS0'), ('XX1', 'DOS1')], 'UNO1': [('XX0', 'DOS0'), ('XX1', 'DOS1')], 'DOS0': [('XXX', 'FINAL')], 'DOS1': [('XXX', 'FINAL')],
    'FINAL': [('1XX', 'TRANS'), ('0XX', 'INICIO')]},
    {'INICIO': (1,), 'TRANS': (1,), 'EMPIE': (0,), 'UNO0': (0,), 'UNO1': (1,), 'DOS0': (0,), 'DOS1': (1,), 'FINAL': (0,)})
check('lb8.p834.completo', M834.complete())
check('lb8.p834.ocho_estados', len(M834.classes()) == 8)
ok = True
for _ in range(300):
    e1, e0 = RNG.randint(0, 1), RNG.randint(0, 1)
    s_ = [(0, RNG.randint(0, 1), RNG.randint(0, 1)) for _ in range(rr(0, 3))] + [(1, e1, e0)] * rr(1, 3) + [(0, e1, e0)] * 4 + [(0, e1, e0)] * 2
    o = [r[2][0] for r in M834.run(s_)]
    k1 = next(i for i, x in enumerate(s_) if x[0] == 1); k0 = next(i for i in range(k1, len(s_)) if s_[i][0] == 0)
    if o[k0:k0 + 5] != [0, e1, e0, 0, 1]: ok = False
check('lb8.p834.trama', ok)
ej('lb8-34', 'Transmisor serie de dos bits con arranque y parada', 'Libro · Cap. 8 · P8.34', 'moore,serie,industrial', 'lb8.p834',
   'Un transmisor envía por una línea serie $S$ los dos bits $E_1E_0$ que tiene en sus entradas cuando se acciona un pulsador $P$ (entradas $P\\,E_1\\,E_0$). La línea en reposo está a 1. Cada transmisión es una trama de **cuatro símbolos**: un bit de arranque a 0, el bit $E_1$, el bit $E_0$ y un bit final a 0; después la línea vuelve a 1. Debe transmitirse al **soltar** el pulsador. Diseña el autómata de Moore.',
   '**El autómata es un secuenciador con ramificaciones sólo para copiar los datos.** Hay una espera, una confirmación de soltado y luego tres pasos fijos. En los pasos de datos hay que elegir entre dos estados según el bit que se copia (UNO0/UNO1 y DOS0/DOS1) porque la salida es parte del estado.',
   [('Esperar y arrancar', 'INICIO (línea a 1): con $P=1$ pasa a TRANS; TRANS espera a que $P$ se suelte; al soltar, EMPIE saca el bit de arranque (0).'),
    ('Copiar los datos', 'De EMPIE se pasa a UNO0 o UNO1 según $E_1$ (salida igual al bit copiado); de ahí a DOS0 o DOS1 según $E_0$; y de DOS siempre a FINAL (salida 0).'),
    ('Fin', 'En FINAL, si $P$ vuelve a estar pulsado se encadena otra trama (TRANS); si no, se vuelve a INICIO con la línea a 1. La salida recorre pues 1, 0, $E_1$, $E_0$, 0, 1.')],
   fsmfig(M834, 'Transmisor serie (entradas $P\\,E_1\\,E_0$). Estado: salida $S$') + tabs(M834)
   + '\n\nSimulado con 300 tramas de datos aleatorios y pulsaciones de longitud variable: la secuencia de salida tras soltar $P$ es siempre 0, $E_1$, $E_0$, 0, 1. El libro lo presenta sólo con diagrama y comentarios.')

# ============================================================ 8.35 receptor serie
r835 = {'INICI': [('1', 'INICI'), ('0', 'EMPIE')], 'EMPIE': [('0', 'UNO0'), ('1', 'UNO1')], 'UNO0': [('0', 'DOS0'), ('1', 'DOS1')], 'UNO1': [('0', 'TRES0'), ('1', 'TRES1')]}
for s in ('DOS0', 'DOS1', 'TRES0', 'TRES1'): r835[s] = [('0', 'BIEN'), ('1', 'ERROR')]
r835['BIEN'] = [('1', 'INICI'), ('0', 'EMPIE')]; r835['ERROR'] = [('X', 'ERROR')]
o835 = {'INICI': (0, 0, 0), 'EMPIE': (0, 0, 0), 'UNO0': (0, 0, 0), 'UNO1': (1, 0, 0), 'DOS0': (0, 0, 0), 'DOS1': (0, 1, 0), 'TRES0': (1, 0, 0), 'TRES1': (1, 1, 0), 'BIEN': (0, 0, 0), 'ERROR': (0, 0, 1)}
M835 = moore(['E'], r835, o835)
r835b = {k: v for k, v in r835.items() if k != 'BIEN'}
for s, f in (('DOS0', 'FIJO0'), ('DOS1', 'FIJO1'), ('TRES0', 'FIJO2'), ('TRES1', 'FIJO3')): r835b[s] = [('0', f), ('1', 'ERROR')]
o835b = {k: v for k, v in o835.items() if k != 'BIEN'}
for k, v in (('FIJO0', (0, 0, 0)), ('FIJO1', (0, 1, 0)), ('FIJO2', (1, 0, 0)), ('FIJO3', (1, 1, 0))):
    r835b[k] = [('1', k), ('0', 'EMPIE')]; o835b[k] = v
M835b = moore(['E'], r835b, o835b)
check('lb8.p835.completo', M835.complete() and M835b.complete())
ok = ok2 = True
for _ in range(300):
    s_ = []; pos = []; exp = []; err = False; last = None; held = []
    for _ in range(rr(1, 5)):
        s_ += [(1,)] * rr(0, 2)
        b1, b0 = RNG.randint(0, 1), RNG.randint(0, 1); stop = 1 if RNG.random() < .12 else 0
        s_ += [(0,), (b1,), (b0,), (stop,)]; pos.append((len(s_) - 2, (b1, b0), stop))
        if stop: break
    o = outs_s(M835, s_); o2 = outs_s(M835b, s_)
    for p, (b1, b0), stop in pos:
        if o[p] != '%d%d0' % (b1, b0) or o2[p] != '%d%d0' % (b1, b0): ok = False
        if stop and (o[p + 1] != '001' or o2[p + 1] != '001'): ok = False
    # aut. 2: el valor se mantiene en los 1 de reposo posteriores a una trama correcta
    for k, (p, (b1, b0), stop) in enumerate(pos):
        if stop: continue
        q = p + 2
        while q < len(s_) and s_[q] == (1,) and q <= (pos[k + 1][0] - 3 if k + 1 < len(pos) else 10 ** 6):
            if o2[q] != '%d%d0' % (b1, b0): ok2 = False
            q += 1
check('lb8.p835.recepcion', ok); check('lb8.p835.mantiene', ok2)
book('lb8.p835', False, 'DOS1 impreso con salida 110 (es 010)')
ej('lb8-35', 'Receptor serie de dos bits con detección de error', 'Libro · Cap. 8 · P8.35', 'moore,serie,industrial', 'lb8.p835',
   'Un receptor recibe por una línea serie $E$ las tramas del problema anterior: la línea en reposo está a 1 y cada trama es 0 (arranque), dos bits de datos, 0 (final). Salidas $I_1I_0\\,AL$: los dos bits recibidos y una alarma $AL$ que se activa si el bit final no vale 0. Diseña el autómata de Moore. Después modifícalo para que **mantenga los datos** en las salidas hasta que empiece la trama siguiente.',
   '**Es el recíproco del transmisor:** hay que recordar los dos bits conforme llegan. Los estados que recuerdan el primer bit (UNO0/UNO1) se ramifican otra vez con el segundo (DOS0, DOS1, TRES0, TRES1), y en todos ellos se comprueba el bit final. Si vale 1, el receptor cae en ERROR, que es **absorbente**.',
   [('Primer autómata', 'INICI espera el 0 de arranque; EMPIE lo ha recibido; UNO0/UNO1 recuerdan el primer dato ($I_1$ ya vale ese bit); DOS0, DOS1, TRES0 y TRES1 recuerdan los dos y presentan $I_1I_0$ (00, 01, 10 y 11) con $AL=0$. Con 0 de cierre se pasa a BIEN y con 1 a ERROR ($AL=1$).'),
    ('Después de BIEN', 'Con 1 (reposo) a INICI; con 0, la trama siguiente empieza ya: a EMPIE.'),
    ('Autómata que mantiene el dato', 'En lugar de BIEN se tienen cuatro estados FIJO0 a FIJO3, que **conservan los mismos valores de salida** durante el reposo (1 se queda; 0 es el arranque de la trama siguiente: EMPIE). Así los datos se mantienen estables hasta el siguiente 0.')],
   '**Primer autómata** (10 estados; las «X» de salida se toman como 0)\n\n' + tabs(M835) + '\n\n**Autómata que mantiene el dato** (13 estados)\n\n' + tabs(M835b)
   + '\n\nSimuladas 300 secuencias de entre una y cinco tramas con datos aleatorios y algún final erróneo: los datos aparecen en el ciclo en que se recibe el segundo bit, la alarma se activa y permanece tras un final erróneo, y en el segundo autómata el dato se mantiene durante el reposo. El libro no incluye ecuaciones (diagramas y comentarios).'
   + ojo('En el primer diagrama el estado DOS1 (los dos bits recibidos son 0 y 1) aparece con salida 110. Debe ser 010: $I_1=0$ e $I_0=1$, que es además lo que dice el segundo autómata para el estado equivalente FIJO1.'))
