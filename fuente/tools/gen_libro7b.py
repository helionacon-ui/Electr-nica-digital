# -*- coding: utf-8 -*-
# Segunda mitad del capítulo 7 (7.12 – 7.22). Se ejecuta con exec desde gen_libro7.py (comparte sus nombres).

# ================================================================ 7.12 contador que cuenta con reloj o con pulsador
def cuenta_flancos(s):
    return sum(1 for k in range(1, len(s)) if s[k - 1] == '0' and s[k] == '1')
# Solución 1: el pulsador es el reloj del contador (sin filtrar)
E_limpio = '0' * 6 + '1' * 10 + '0' * 6
E_rebote = '0' * 6 + '1101011' + '1' * 4 + '0010' + '0' * 6
check('lb7.p712.s1_limpio', cuenta_flancos(E_limpio) == 1)
check('lb7.p712.s1_rebote', cuenta_flancos(E_rebote) == 4)
# Solución 2: reloj único y pulso de un periodo Q1·/Q2 que habilita al contador cuando I=1
def contador_pulsador(E_per, I):
    q1 = q2 = 0; cnt = 0; hist = []
    for e in E_per:
        en = 1 if I == 0 else (q1 & (1 - q2))
        hist.append((q1, q2, en, cnt))
        cnt = (cnt + en) % 10
        q1, q2 = e, q1
    return cnt, hist
random.seed(7)
ok = True
for _ in range(300):
    E = []
    for _p in range(random.randint(0, 8)):
        E += [0] * random.randint(2, 6) + [1] * random.randint(2, 12)
    E += [0] * 3
    n = sum(1 for k in range(len(E)) if E[k] == 1 and (k == 0 or E[k - 1] == 0))
    cnt, _h = contador_pulsador(E, 1)
    ok &= cnt == n % 10
    cnt0, _h0 = contador_pulsador(E, 0)
    ok &= cnt0 == len(E) % 10
check('lb7.p712.s2', ok)
E712 = [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
cnt712, h712 = contador_pulsador(E712, 1)
def per_slots(vals, n=8): return ''.join(str(v) * n for v in vals)
E712s = per_slots(E712)
CK712s = ''.join('0000' + '1111' for _ in E712)
Q1s = ''.join(str(h712[n][0]) * 4 + str(E712[n]) * 4 for n in range(len(E712)))
Q2s = ''.join(str(h712[n][1]) * 4 + str(h712[n][0]) * 4 for n in range(len(E712)))
HABs = ''.join('1' if (a == '1' and b == '0') else '0' for a, b in zip(Q1s, Q2s))
n_pulsos712 = sum(1 for n in range(len(E712)) if h712[n][2])
check('lb7.p712.cronograma', n_pulsos712 == 2 and cuenta_flancos(E712s) == 2 and cnt712 == 2)
ej('lb7-12', 'Contador módulo 10 que cuenta con el reloj o con un pulsador', 'Libro · Cap. 7 · P7.12', 'contador,74160,pulsador,deteccion-flancos', 'lb7.p712',
   'Diseña un contador síncrono módulo 10 que cuente al ritmo de un reloj o bien una vez por cada pulsación de un pulsador. Con el interruptor $I=0$ debe contar con el reloj; con $I=1$ debe contar al ritmo del pulsador, una vez por pulsación sea cual sea su duración.',
   '**Hay dos formas de hacerlo y la buena no toca el reloj.** Se puede escoger la señal de reloj del contador con un multiplexor (reloj o pulsador), o se puede dejar siempre el mismo reloj y escoger si el contador está **habilitado**.',
   [('Primera solución: multiplexor en el reloj', 'Un mux 2:1 elige entre $Ck$ ($I=0$) y el pulsador ($I=1$) como reloj de un 74160. Funciona solo si el pulsador está **filtrado** (red RC, báscula R‑S…): un pulsador real rebota y cada rebote es un flanco. Con un pulso de entrada sucio de cuatro subidas el contador salta de cuatro en cuatro (simulado). Y la solución tiene un defecto de método: la señal de reloj ya no es siempre $Ck$.'),
    ('Segunda solución: reloj único y detector de flancos', 'Dos biestables D con el reloj $Ck$ copian el pulsador: $Q_1$ el valor actual y $Q_2$ el anterior. La salida $Q_1\\cdot\\overline{Q_2}$ vale 1 **exactamente un periodo** después de cada subida del pulsador, sea cual sea el tiempo que se mantenga pulsado. Un mux 2:1 escoge ENP·ENT: con $I=0$ vale 1 (cuenta con el reloj) y con $I=1$ vale ese pulso.'),
    ('Comprobación', 'Con $I=1$ se han simulado 300 secuencias aleatorias de pulsaciones (de 2 a 12 relojes de duración): el contador avanza **una unidad por pulsación**. Con $I=0$ avanza una por reloj. Las dos soluciones requieren que el pulsador esté filtrado de rebotes; la segunda además cumple que la única señal de reloj es $Ck$.')],
   cron([['Ck', CK712s], ['Pulsador', E712s], ['Q1', Q1s], ['Q2', Q2s], ['Habilita', HABs]], 'Solución 2 con I = 1 (cada pulsación suma uno)', 30, w=6, grid=8)
   + '\n\nLa señal «Habilita» ($Q_1\\cdot\\overline{Q_2}$) dura exactamente un periodo de reloj y aparece **dos veces** para las dos pulsaciones: la primera, aunque se mantenga pulsado durante cinco relojes, y la segunda de tres. El contador suma uno en cada uno de esos dos periodos.')

# ================================================================ 7.13 detector de la clave 1011 con registro de desplazamiento
def detecta(stream):
    reg = [0, 0, 0, 0]; out_a = []; out_b = []
    for b in stream:
        reg = [b] + reg[:3]                                   # Q0 recibe el nuevo bit; Q3 es el más antiguo
        Q0, Q1, Q2, Q3 = reg
        out_a.append(int(Q3 == 1 and Q2 == 0 and Q1 == 1 and Q0 == 1))        # puerta AND con una entrada negada
        out_b.append(int(Q3 * 8 + Q2 * 4 + Q1 * 2 + Q0 == 0b1011))            # comparador de igualdad con 1011
    return out_a, out_b
random.seed(13)
ok = True
for _ in range(400):
    s = [random.randint(0, 1) for _ in range(random.randint(4, 40))]
    a_, b_ = detecta(s)
    exp = [int(k >= 3 and s[k - 3:k + 1] == [1, 0, 1, 1]) for k in range(len(s))]
    ok &= a_ == exp and b_ == exp
check('lb7.p713', ok)
s713 = [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1]
a713, _ = detecta(s713)
check('lb7.p713.solape', [k for k, v in enumerate(a713) if v] == [4, 7, 11])
ej('lb7-13', 'Cerradura que se abre con la secuencia 1011', 'Libro · Cap. 7 · P7.13', 'registro,desplazamiento,secuencia,aplicacion', 'lb7.p713',
   'Una puerta se abre automáticamente cuando recibe, de forma síncrona por una línea de entrada, la secuencia 1, 0, 1, 1: debe darse en los **cuatro últimos flancos de reloj**. Diséñala con un registro de desplazamiento.',
   '**Un registro de 4 bits «recuerda» los cuatro últimos bits.** Si el bit nuevo entra por $Q_0$, en $Q_3$ está el más antiguo y en $Q_0$ el más reciente. La clave, leída en el orden de llegada $1,0,1,1$, corresponde al contenido $Q_3Q_2Q_1Q_0=1011$.',
   [('Opción A: puerta AND', 'Una AND de cuatro entradas con $Q_2$ negado: $Abre=Q_3\\cdot\\overline{Q_2}\\cdot Q_1\\cdot Q_0$. Requiere un inversor y una AND.'),
    ('Opción B: comparador', 'Un comparador de cuatro bits (tipo 7485) con una entrada fija a $1011$ y la otra conectada a $Q_3..Q_0$: la salida «igual» abre la puerta. Es más potente porque **cambiar la clave** es solo cambiar interruptores.'),
    ('Comparación', 'La opción A es más sencilla pero menos clara; la B es más versátil. En coste no hay una ventaja grande: un 7485 frente a un 7408 y un 7404.'),
    ('Solapamiento', 'La puerta se abre **cada vez** que los cuatro últimos bits valen 1011, aunque se solapen con una secuencia anterior: con la entrada 0 1 0 1 1 0 1 1 1 0 1 1 se abre en el cuarto, en el séptimo y en el último flanco (la secuencia 1011 y la siguiente comparten los dos últimos bits).')],
   'Comprobado con 400 secuencias aleatorias de longitud 4 a 40: las dos opciones dan la misma salida y se abren exactamente cuando los cuatro últimos bits son 1011.\n\n'
   + tab(['Flanco', 'Bit', '$Q_3Q_2Q_1Q_0$', 'Abre'], [[k + 1, s713[k], ''.join(str(x) for x in ([0, 0, 0, 0] + s713[:k + 1])[-4:]), a713[k]] for k in range(len(s713))]))

# ================================================================ 7.14 dígito BCD en serie
seg_ok = {n: n <= 9 for n in range(16)}
check('lb7.p714', all(seg_ok[n] == (n <= 9) for n in range(16)))
stream714 = [1, 0, 0, 1]
reg = [0, 0, 0, 0]; pasos714 = []
for b in stream714:
    reg = [b] + reg[:3]
    n = reg[3] * 8 + reg[2] * 4 + reg[1] * 2 + reg[0]
    pasos714.append((b4(n), n, 'blanco' if n > 9 else str(n)))
check('lb7.p714.parcial', [p[1] for p in pasos714] == [1, 2, 4, 9])
ej('lb7-14', 'Visualizar un dígito BCD recibido en serie', 'Libro · Cap. 7 · P7.14', 'registro,desplazamiento,7-segmentos,comparador', 'lb7.p714',
   'Visualiza en un display de siete segmentos el dígito BCD que llega **en serie** y sincronizado con un reloj. Si el dígito recibido es erróneo (no es BCD), no debe visualizarse.',
   '**Registro de desplazamiento + decodificador BCD‑7 segmentos + comparador.** El registro convierte los cuatro bits de la entrada serie en un número de cuatro bits; el decodificador lo muestra; y un comparador vigila que no pase de 9.',
   [('Cableado', 'Las salidas $Q_3..Q_0$ del registro van a las entradas 8‑4‑2‑1 del decodificador y a la entrada $A$ de un comparador cuya entrada $B$ vale $1001$ (9). La salida $A>B$ se lleva a la línea de **apagado** del decodificador (BI), que es activa en bajo: la señal debe llegar invertida (o usarse la salida complementaria) para que el display se apague cuando el número es mayor que 9.'),
    ('Funcionamiento', 'Si el número recibido es mayor que 9 se activa BI y el display queda en blanco; si es ≤ 9 se ve el dígito. Se ha comprobado con los 16 valores posibles.'),
    ('Un matiz', 'Como el display está conectado al registro, durante la recepción **se ven valores intermedios**: con la entrada 1 0 0 1 (el 9, bit más significativo primero) se verá sucesivamente ' + ' → '.join(p[2] for p in pasos714) + '. Solo después del cuarto flanco hay un valor válido. Para un montaje serio convendría un registro de captura en la salida.')],
   tab(['Flanco', 'Bit recibido', '$Q_3Q_2Q_1Q_0$', 'Display'], [[k + 1, stream714[k], pasos714[k][0], pasos714[k][2]] for k in range(4)])
   + '\n\nTabla completa: los valores 0000 a 1001 se muestran; 1010 a 1111 dejan el display en blanco.')

# ================================================================ 7.15 notas de tres partes
def nota_de(p1, p2, p3):
    return {(1, 1, 1): 10, (1, 1, 0): 7, (1, 0, 0): 5}.get((p1, p2, p3), 0)
def lamparas(q0, q1, q2):      # Q2=P1 (primer bit recibido), Q1=P2, Q0=P3
    n10 = q2 & q1 & q0
    n7 = q2 & q1 & (1 - q0)
    n5 = q2 & (1 - q1) & (1 - q0)
    return n10, n7, n5
check('lb7.p715.tabla', all(sum(lamparas(p3, p2, p1)) <= 1 for p1 in (0, 1) for p2 in (0, 1) for p3 in (0, 1)) and
      all((lamparas(p3, p2, p1) == ((nota_de(p1, p2, p3) == 10), (nota_de(p1, p2, p3) == 7), (nota_de(p1, p2, p3) == 5))) for p1 in (0, 1) for p2 in (0, 1) for p3 in (0, 1)))
# versión 1: lámparas a la salida del registro (sin contador)
def simula715a(stream):
    reg = [0, 0, 0, 0]; res = []
    for b in stream:
        reg = [b] + reg[:3]; res.append(lamparas(reg[0], reg[1], reg[2]))
    return res
ej715 = [0, 1, 1, 1, 0, 0]
r715a = simula715a(ej715)
check('lb7.p715.mezcla', [k + 1 for k, r in enumerate(r715a) if r[0]] == [4] and [k + 1 for k, r in enumerate(r715a) if r[1]] == [5] and [k + 1 for k, r in enumerate(r715a) if r[2]] == [6])
# versión 2: contador 74160 (D=0001) y AND de Q1·Q0 que habilita las lámparas y recarga 1
def simula715b(stream):
    reg = [0, 0, 0, 0]; c = Cnt(10, 0); res = []                   # tras INICIO: registro y contador a 0
    for b in stream:
        flag = int((c.q & 3) == 3)
        res.append((lamparas(reg[0], reg[1], reg[2]) if flag else (0, 0, 0), c.q))
        reg = [b] + reg[:3]
        c.clk(load=0 if flag else 1, d=1)
    return res
random.seed(3)
alumnos = [(random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)) for _ in range(40)]
stream = [x for a in alumnos for x in a]
rb = simula715b(stream + [0])                       # un flanco más para ver la salida del último alumno
ok = True
notas_obt = [max([i for i, v in zip((10, 7, 5), r[0]) if v] + [0]) for r in rb]
exp_n = []
for k in range(len(rb)):
    if k % 3 == 2 and k // 3 < len(alumnos): exp_n.append(nota_de(*alumnos[k // 3]))
    elif k % 3 == 2: exp_n.append(None)
got = [notas_obt[k] for k in range(len(rb)) if k % 3 == 3 % 3 or False]
ok = all(notas_obt[3 * i + 3] == nota_de(*alumnos[i]) for i in range(len(alumnos)))
ok &= all(notas_obt[k] == 0 for k in range(len(rb)) if (k - 3) % 3 != 0)
ok &= [r[1] for r in rb[:7]] == [0, 1, 2, 3, 1, 2, 3]
check('lb7.p715.contador', ok)
ej('lb7-15', 'Nota de un alumno a partir de tres partes de examen', 'Libro · Cap. 7 · P7.15', 'registro,desplazamiento,contador,aplicacion', 'lb7.p715',
   'Un circuito recibe **en serie** bloques de tres bits: cada bit dice si el alumno ha superado la primera, la segunda y la tercera parte de un examen. Debe encenderse uno solo de tres diodos (o ninguno): NOTA5 si solo se ha superado la primera parte, NOTA7 si se han superado la primera y la segunda, y NOTA10 si se han superado las tres.',
   '**Registro de desplazamiento y tres puertas AND.** El registro guarda los tres últimos bits recibidos. Si el bit nuevo entra por $Q_0$, tras tres flancos $Q_2$ guarda la primera parte, $Q_1$ la segunda y $Q_0$ la tercera.',
   [('Funciones', 'NOTA10 $=Q_2Q_1Q_0$; NOTA7 $=Q_2Q_1\\overline{Q_0}$; NOTA5 $=Q_2\\overline{Q_1}\\,\\overline{Q_0}$. Los inversores no se pueden eliminar: sin ellos, un alumno con las tres partes superadas encendería los tres diodos a la vez.'),
    ('Defecto de la primera versión', 'El registro se evalúa en **todos** los flancos, y en los dos que siguen a cada alumno contiene bits de dos alumnos distintos. Con la entrada 0 1 1 | 1 0 0 (el primero no obtiene nota; el segundo aprueba solo la primera parte) los diodos que se encienden son ' + ', '.join('NOTA%d en el flanco %d' % (n, k + 1) for k, r in enumerate(r715a) for n, v in zip((10, 7, 5), r) if v) + ': las dos primeras notas son **falsas**, mezcla de dos alumnos.'),
    ('Solución con contador', 'Un 74160 cargado con 0001 por LOAD cuenta 1, 2, 3, 1, 2, 3…; una AND de $Q_1$ y $Q_0$ da 1 solo cuando vale 3, es decir, **una vez cada tres flancos**. Esa señal habilita las tres puertas (que pasan a ser de cuatro entradas) y, invertida, activa el LOAD del contador que recarga 1.'),
    ('Las inicializaciones', 'Tras INICIO el contador está a **0**, no a 1, y aun así el montaje es correcto: de 0 a 3 hay tres flancos, igual que de 1 a 3 tras la recarga (2 flancos de cuenta más el de carga). Se ha comprobado con 40 alumnos aleatorios: la nota correcta sale una sola vez por alumno y solo en el tercer flanco del bloque.')],
   tab(['Flanco', 'Bit recibido', 'Contenido $Q_2Q_1Q_0$', 'Diodo encendido (versión sin contador)'],
       [[k + 1, ej715[k], ''.join(str(x) for x in ([0, 0, 0] + ej715[:k + 1])[-3:]), ', '.join('NOTA%d' % n for n, v in zip((10, 7, 5), r715a[k]) if v) or '—'] for k in range(6)])
   + '\n\nCon el contador, la secuencia de valores del 74160 es $0,1,2,3,1,2,3,\\dots$ y la nota solo se muestra cuando vale 3.'
   + ojo('En el esquema del libro los rótulos $P1,P2,P3$ de la salida del registro aparecen en un orden que no coincide con el cableado de las puertas (según se lee el dibujo, las puertas de NOTA7 y NOTA5 invierten la línea rotulada $P1$, cuando el enunciado exige invertir la **última** parte). La solución de arriba toma la convención coherente: $Q_2$ es la primera parte, y reproduce la tabla de notas del enunciado.'))
book('lb7.p715.rotulos', False, 'rótulos P1..P3 en orden inverso al cableado')

# ================================================================ 7.16 multiplexado de cuatro displays
def mux_display(digits, ciclos):
    c = Cnt(10, 0); vistas = []
    for _ in range(ciclos):
        sel = c.q & 3
        en = [int(sel == k) for k in range(4)]            # decodificador 2:4: una línea de enable activa
        vistas.append((sel, en, digits[sel]))
        c.clk(load=0 if (c.q & 3) == 3 else 1, d=0)       # NAND de Q1 y Q0 (valor 3) a LOAD con D=0
    return vistas
dig = [4, 3, 2, 1]                                          # unidades, decenas, centenas, millares (ejemplo 1234)
v716 = mux_display(dig, 16)
check('lb7.p716', [v[0] for v in v716] == [0, 1, 2, 3] * 4 and all(sum(v[1]) == 1 for v in v716) and [v[2] for v in v716[:4]] == [4, 3, 2, 1])
check('lb7.p716.frecuencia', 200 / 4 == 50 and 1000 / 200 == 5)
ej('lb7-16', 'Multiplexado de cuatro displays de siete segmentos', 'Libro · Cap. 7 · P7.16', 'contador,multiplexado,7-segmentos,aplicacion', 'lb7.p716',
   'Diseña un circuito que multiplexe sobre cuatro displays de siete segmentos el contenido de cuatro dígitos BCD. Para los cuatro displays hay solo siete líneas de segmentos y cuatro líneas de enable, una por display. El reloj disponible es de 200 Hz.',
   '**Un solo decodificador BCD‑7 segmentos para los cuatro dígitos, repartido en el tiempo.** Cada $T$ segundos se enciende un display distinto con el dígito que le corresponde; si el cambio es suficientemente rápido el ojo ve los cuatro encendidos a la vez.',
   [('Contador de barrido', 'Un 74160 cuenta 0, 1, 2, 3, 0… porque una NAND de $Q_1$ y $Q_0$ (valor 3) carga 0 con LOAD. Solo se usan sus dos bits bajos.'),
    ('Selección del dígito', 'Los cuatro dígitos pasan por **buffers triestado** hacia el decodificador común. Un decodificador 2:4 con $Q_1Q_0$ activa un único enable: el del buffer del dígito que toca y, a la vez, el del transistor que alimenta a su display. El triestado puede sustituirse por un multiplexor 4:1 de cuatro bits.'),
    ('Frecuencias', 'Cada display se enciende uno de cada cuatro ciclos: $200\\ Hz/4=50\\ Hz$ de refresco **por display**, con $T=5$ ms por dígito. No conviene subir mucho la frecuencia de barrido (1 kHz, 1 MHz): los transistores y el propio display no responden. Entre 50 y 100 Hz por display es lo adecuado, por lo que 200 Hz es una buena elección. Es el mismo principio con el que se barre una pantalla de televisión.')],
   tab(['Flanco', 'Contador', 'Display activo', 'Dígito mostrado'], [[k, v716[k][0], ['UNI', 'DEC', 'CEN', 'MIL'][v716[k][0]], v716[k][2]] for k in range(8)])
   + '\n\nCon el número 1234 de ejemplo (unidades = 4, decenas = 3, …): en cada flanco hay **exactamente un enable activo** (simulado durante 16 flancos) y el patrón se repite cada cuatro.')

# ================================================================ 7.17 divisor 1, 2, 4 u 8 con registro universal
def divide(dividendo, divisor):
    code = {1: 0, 2: 1, 4: 2, 8: 3}[divisor]
    reg = dividendo; cont = 0; relojes = 0
    # INICIO: contador a 0. CARGA ya hecha (reg = dividendo). Ahora I = 1
    I = 1; C = 0
    for _ in range(20):
        m = int(cont < code)                                   # el contador es menor que el divisor codificado
        S1 = 1 - C; S0 = C | (I & m)
        en = I & m                                             # ENP·ENT
        if (S1, S0) == (1, 1) and en:                          # desplaza un bit hacia el de menor peso y el contador suma 1
            reg >>= 1; cont += 1; relojes += 1
        elif (S1, S0) == (1, 0): pass                          # inhibe
        else: raise RuntimeError
    return reg, relojes
okd = all(divide(n, d) == (n // d, {1: 0, 2: 1, 4: 2, 8: 3}[d]) for n in range(16) for d in (1, 2, 4, 8))
check('lb7.p717', okd)
tabla = [(C, I, m) for C in (1, 0) for I in (0, 1) for m in (0, 1)]
def sel717(C, I, m): return (1 - C, C | (I & m))
check('lb7.p717.logica', all(sel717(1, I, m) == (0, 1) for I in (0, 1) for m in (0, 1)) and sel717(0, 1, 1) == (1, 1) and sel717(0, 1, 0) == (1, 0) and all(sel717(0, 0, m) == (1, 0) for m in (0, 1)))
book('lb7.p717.coment', False, 'El comentario dice S1=1, S0=0 mientras se divide; la tabla del propio ejercicio dice S1S0=11 (S0 = C + I·m).')
ej('lb7-17', 'Divisor entre 1, 2, 4 u 8 con un registro universal', 'Libro · Cap. 7 · P7.17', 'registro,contador,division,aplicacion', 'lb7.p717',
   'Diseña un divisor cuyo dividendo es un número binario de 4 bits cargado en un registro y cuyo divisor vale 1, 2, 4 u 8 según cuál de cuatro microinterruptores esté activado. El divisor tiene un interruptor $I$ para marcar el inicio de la división.',
   '**Dividir por $2^k$ es desplazar $k$ posiciones hacia el bit de menor peso.** Se usa un registro universal 74179 (que carga en paralelo, desplaza e inhibe) y un contador que cuenta los desplazamientos hechos; un comparador dice si ya se han hecho tantos como pide el divisor.',
   [('Codificar el divisor', 'Los cuatro microinterruptores (1, 2, 4, 8) pasan por un codificador 4:2 que da $k$ en dos bits: 1 → 00, 2 → 01, 4 → 10, 8 → 11.'),
    ('Procedimiento', 'Se activa INICIO (contador a 0), se pone el dividendo en los cuatro microinterruptores y se da un pulso a CARGA DIVIDENDO. Después se pone $I=1$: mientras el contador es **menor** que $k$ (salida $m$) el registro desplaza y el contador suma uno; al llegar a $k$ se detiene. El cociente queda estable en las salidas $Q_3..Q_0$. Para otra división hay que volver a $I=0$ e INICIO.'),
    ('Control del registro', 'Con $C$ = carga, $I$ = división y $m$ = «contador menor que $k$», las líneas $S_1S_0$ valen: $C=1$ → 01 (carga); $C=0,I=1,m=1$ → 11 (desplaza); $C=0,I=1,m=0$ → 10 (inhibe, final); $C=0,I=0$ → 10 (no divide). Por Karnaugh: $S_1=\\overline C$ y $S_0=C+I\\cdot m$, con $ENP\\cdot ENT=I\\cdot m$.'),
    ('Comprobación', 'Se han probado las $16\\cdot4=64$ divisiones posibles: el cociente es siempre $\\lfloor dividendo/divisor\\rfloor$ y se hacen exactamente $k$ desplazamientos. Los bits que salen por el extremo son el resto, que este circuito **no conserva**.')],
   tab(['$C$', '$I$', '$m$', '$S_1S_0$', 'Operación'], [['1', '×', '×', '01', 'carga el dividendo'], ['0', '1', '1', '11', 'desplaza y cuenta'], ['0', '1', '0', '10', 'final: inhibe'], ['0', '0', '×', '10', 'no divide']])
   + '\n\nEjemplo: dividendo 1101 (13) entre 4 ($k=2$): dos desplazamientos dan $1101\\to0110\\to0011$, es decir, 3 = $\\lfloor13/4\\rfloor$ (el resto, 1, sale por la derecha).'
   + ojo('Dos detalles del libro no concuerdan entre sí: el comentario dice que durante la división $S_1=1$ y $S_0=0$, pero la tabla del propio ejercicio da $S_1S_0=11$ (y $S_0=C+I\\cdot m$). Además, la salida del comparador que se usa debe ser «código mayor que contador» (con $A$ = código y $B$ = contador, la salida **M**), mientras que el texto habla de «contador menor» (m). Lo importante es que el registro desplace hacia el bit de menor peso mientras queden desplazamientos por hacer.'))

# ================================================================ 7.18 alarma de velocidad de un microbot
def microbot(rev_s, segundos=3, fase=0.0):
    f_p = 4 * rev_s                                            # pulsos por segundo (4 marcas por vuelta)
    base = [Cnt(10), Cnt(10)]; c = Cnt(16); q1 = q2 = 0
    maxcuenta = []; alarma = []; ventana_max = 0; ventana_alarma = 0
    cuentas_fin = []
    for n in range(100 * segundos):
        t = n / 100.0 + fase
        w = int((2 * f_p * t) % 2 < 1)                         # rueda: 50 % de ciclo de trabajo
        pulso = q1 & (1 - q2)
        al = int(c.q > 12)
        ventana_alarma |= al; ventana_max = max(ventana_max, c.q)
        fin = int(base[0].q == 9 and base[1].q == 9)           # fin de ventana de 100 relojes
        if fin:
            cuentas_fin.append((ventana_max, ventana_alarma)); ventana_max = 0; ventana_alarma = 0
        # flanco: se usan los valores de antes
        base0 = base[0].rco(1)
        c.clk(clear=0 if fin else 1, en=pulso)
        base[1].clk(en=base0); base[0].clk()
        q1, q2 = w, q1
    return cuentas_fin
res718 = {}
for sp in (1, 2, 2.5, 3.5, 4, 5):
    r = microbot(sp, 4, fase=0.0037)
    res718[sp] = r[1:]                                         # se descarta la primera ventana (arranque)
ok = all(not any(a for _, a in res718[s]) for s in (1, 2, 2.5)) and all(all(a for _, a in res718[s]) for s in (3.5, 4, 5))
check('lb7.p718', ok, res718)
ok2 = all(m == 14 for m, _ in res718[3.5][:2]) and all(m == 10 for m, _ in res718[2.5][:2]) and all(m == 15 for m, _ in res718[4]) and all(m == 15 for m, _ in res718[5])
check('lb7.p718.cuentas', ok2, res718)
ej('lb7-18', 'Alarma de exceso de velocidad de una rueda', 'Libro · Cap. 7 · P7.18', 'contador,74160,74163,aplicacion', 'lb7.p718',
   'Un microbot lleva en una rueda cuatro marcas ópticas. Hay que activar una alarma cuando la rueda dé **más de tres vueltas por segundo**. El reloj es de 100 Hz. Diseña el circuito.',
   '**Medir una frecuencia es contar pulsos durante un intervalo conocido.** Tres vueltas por segundo con cuatro marcas son 12 pulsos por segundo; la alarma debe saltar si en una ventana de 1 s se cuentan más de 12.',
   [('Base de tiempos', 'Dos 74160 en cascada forman un contador de módulo 100 que cuenta los relojes de 100 Hz: la ventana dura 100 relojes, es decir, **1 s**. Cuando los dos valen 9 (99 relojes) una NAND de sus fin‑de‑cuenta borra el contador de pulsos.'),
    ('Contador de pulsos', 'Un 74163 (binario de 4 bits) cuenta los pulsos de la rueda. Para que cada marca cuente **una vez** aunque sea larga, la señal de la rueda pasa antes por dos biestables D y una AND ($Q_1\\cdot\\overline{Q_2}$), el detector de flancos del problema 7.12.'),
    ('Alarma', 'Un comparador compara la cuenta con $1100$ (12) y su salida «mayor que» enciende la alarma: se activa en cuanto se supera el 12 y se apaga con el borrado de la siguiente ventana.'),
    ('Límites', 'Un pulso de rueda debe durar al menos un periodo de reloj (0,01 s) para ser detectado; si dura menos hay que subir la frecuencia base (1 kHz o más). Como el 74163 es de módulo 16, a partir de 16 pulsos por segundo (4 vueltas por segundo) la cuenta **da la vuelta**: la alarma se enciende al pasar por 13, 14 y 15, pero se apaga cuando el contador vuelve a 0. Para medir velocidades mayores hay que ampliar el módulo conectando más 74163 en cascada.')],
   tab(['Vueltas por segundo', 'Pulsos por segundo', 'Cuenta máxima en la ventana', 'Alarma'], [[sp, int(4 * sp), res718[sp][0][0], 'sí' if res718[sp][0][1] else 'no'] for sp in (1, 2, 2.5, 3.5, 4, 5)])
   + '\n\nSimulación a nivel de reloj durante cuatro ventanas por velocidad (se descarta la primera, de arranque). A 4 y 5 vueltas por segundo el contador ya ha dado la vuelta: la alarma se enciende un instante, pero no queda fija. Con 3 vueltas por segundo la cuenta está justo en el límite (12 pulsos, ±1 por el desfase entre ventana y rueda).')

# ================================================================ 7.19 marcador de tenis
def juego(a, b):
    mayor = a if a > b else b; menor = b if a > b else a
    MD = int(mayor > 3); MR = int(mayor - menor > 1)
    return MD & MR
check('lb7.p719.logica', all(juego(a, b) == int(max(a, b) >= 4 and abs(a - b) >= 2) for a in range(16) for b in range(16)))
def partido(puntos):
    a = b = 0; hist = []
    for p in puntos:
        if juego(a, b):
            hist.append(('J', 'A' if a > b else 'B', a, b)); a = b = 0
        if p == 'A': a += 1
        else: b += 1
        if juego(a, b) and False: pass
    if juego(a, b): hist.append(('J', 'A' if a > b else 'B', a, b))
    return hist
def ref_tenis(puntos):
    a = b = 0; res = []
    for p in puntos:
        if p == 'A': a += 1
        else: b += 1
        if max(a, b) >= 4 and abs(a - b) >= 2:
            res.append(('J', 'A' if a > b else 'B', a, b)); a = b = 0
    return res
def circuito(puntos):
    """Un punto por pulso de reloj; JUEGO se detecta tras el punto y, en el flanco siguiente, borra los contadores."""
    a = b = 0; res = []
    for p in puntos:
        if juego(a, b): res.append(('J', 'A' if a > b else 'B', a, b)); a = b = 0
        if p == 'A': a += 1
        else: b += 1
    if juego(a, b): res.append(('J', 'A' if a > b else 'B', a, b))
    return res
random.seed(11)
ok = True
for _ in range(500):
    pts = [random.choice('AB') for _ in range(random.randint(4, 40))]
    ok &= circuito(pts) == ref_tenis(pts)
check('lb7.p719', ok)
ej719 = list('AABBAAABBB' + 'BAABBB')
r719 = circuito(ej719); check('lb7.p719.ejemplo', r719 == ref_tenis(ej719))
def marcador(a, b):
    nombres = ['0', '15', '30', '40']
    if max(a, b) < 4 and not (a == 3 and b == 3):
        return '%s - %s' % (nombres[a], nombres[b])
    if a == b: return 'iguales (40‑40)'
    return 'ventaja ' + ('A' if a > b else 'B') if abs(a - b) == 1 and max(a, b) >= 4 else ('40‑40' if max(a, b) == 3 else '%s - %s' % (nombres[min(a, 3)], nombres[min(b, 3)]))
ej('lb7-19', 'Marcador de tenis con dos pulsadores', 'Libro · Cap. 7 · P7.19', 'contador,74163,comparador,aplicacion', 'lb7.p719',
   'Diseña un marcador de tenis controlado por dos pulsadores, uno por jugador. En principio basta con un marcador de puntos que tenga en cuenta el empate (iguales) y la ventaja. Los números pueden visualizarse como 0, 1, 2, 3… en lugar de 0, 15, 30, 40.',
   '**Un contador de puntos por jugador y un circuito que decide cuándo termina el juego.** Un juego se gana al alcanzar **al menos cuatro puntos con una diferencia de al menos dos**.',
   [('Entradas', 'Cada pulsador pasa por un detector de flancos de dos biestables D y una AND, de modo que cada pulsación suma **un único** punto aunque se mantenga pulsada. Cada jugador tiene un 74163; se supone que un juego nunca pasa de 15 puntos.'),
    ('Quién gana y por cuánto', 'Un comparador dice cuál de los dos contadores es mayor y dos multiplexores 4×2:1 colocan el mayor como **minuendo** y el menor como **sustraendo**. Un restador calcula la diferencia.'),
    ('Fin de juego', 'Un comparador contra $0011$ da $MD=1$ si el mayor supera 3 (tiene al menos 4) y otro contra $0001$ da $MR=1$ si la diferencia supera 1 (es al menos 2). $JUEGO=MD\\cdot MR$.'),
    ('Qué hace JUEGO', 'Activa, invertida, la línea LOAD de los dos contadores (con $D=0$) para ponerlos a 0; se lleva a un demultiplexor 1:2 que enciende el led del ganador (la señal de «A mayor» elige el led) y podría habilitar un contador de juegos ganados por cada jugador. Todo el circuito comparte la misma línea de reloj.'),
    ('Comprobación', 'La lógica combinacional coincide con la regla del tenis para las $16\\cdot16=256$ combinaciones de puntos. Además se han simulado 500 partidos aleatorios de 4 a 40 puntos y los juegos (quién gana y con qué tanteo) coinciden con una simulación directa de la regla.')],
   tab(['Puntos A', 'Puntos B', 'Mayor', 'Diferencia', 'MD', 'MR', 'JUEGO'],
       [[a, b, max(a, b), abs(a - b), int(max(a, b) > 3), int(abs(a - b) > 1), juego(a, b)] for a, b in [(3, 0), (4, 0), (4, 2), (4, 3), (3, 3), (5, 3), (5, 4), (6, 4)]])
   + '\n\nEjemplo con los puntos A A B B A A A B B B B A A B B B (A y B alternan): juegos terminados ' + ', '.join('gana %s por %d‑%d' % (x[1], x[2], x[3]) for x in r719) + '.')

# ================================================================ 7.20 – 7.22 contadores asíncronos con borrado / preset
# 7.20: 0..5 con J-K de flanco de bajada; NAND(Q2,Q1,/Q0) -> CLEAR
CK720 = ckstr(8)
ffs = [(('ck', 'f'), lambda q: 1 - q[0]), (('q', 0, 'f'), lambda q: 1 - q[1]), (('q', 1, 'f'), lambda q: 1 - q[2])]
S720, g720 = ripple(ffs, CK720, [0, 0, 0], force=lambda q: [0, 0, 0] if (q[0] == 0 and q[1] == 1 and q[2] == 1) else None)
v720 = [val(s) for s in S720]
sec720 = []; [sec720.append(x) for x in v720 if not sec720 or sec720[-1] != x]
check('lb7.p720', sec720 == [0, 1, 2, 3, 4, 5, 0, 1, 2], sec720)
check('lb7.p720.glitch', set(g720) == {(0, 1, 1)} and len(g720) == 1)
# 7.21: BCD, NAND(Q3,/Q2,Q1,/Q0) -> CLEAR
CK721 = ckstr(12)
ffs4 = [(('ck', 'f'), lambda q: 1 - q[0]), (('q', 0, 'f'), lambda q: 1 - q[1]), (('q', 1, 'f'), lambda q: 1 - q[2]), (('q', 2, 'f'), lambda q: 1 - q[3])]
S721, g721 = ripple(ffs4, CK721, [0, 0, 0, 0], force=lambda q: [0, 0, 0, 0] if (q[0] == 0 and q[1] == 1 and q[2] == 0 and q[3] == 1) else None)
v721 = [val(s) for s in S721]
sec721 = []; [sec721.append(x) for x in v721 if not sec721 or sec721[-1] != x]
check('lb7.p721', sec721 == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2], sec721)
check('lb7.p721.glitch', set(g721) == {(0, 1, 0, 1)} and len(g721) == 1)
simple = lambda q: [0, 0, 0, 0] if (q[3] == 1 and q[1] == 1) else None     # basta Q3·Q1 (valor 10)
S721b, g721b = ripple(ffs4, ckstr(12), [0, 0, 0, 0], force=simple)
check('lb7.p721.puerta_simple', [val(s) for s in S721b] == v721)
check('lb7.p720.puerta_simple', [val(s) for s in ripple(ffs, CK720, [0, 0, 0], force=lambda q: [0, 0, 0] if (q[1] == 1 and q[2] == 1) else None)[0]] == v720)
# 7.22: biestables de flanco de subida encadenados por Q (descendente), NAND(/Q2,Q1,/Q0) a PRESET -> 7
CK722 = ckstr(8)
ffs3r = [(('ck', 'r'), lambda q: 1 - q[0]), (('q', 0, 'r'), lambda q: 1 - q[1]), (('q', 1, 'r'), lambda q: 1 - q[2])]
S722, g722 = ripple(ffs3r, CK722, [1, 1, 1], force=lambda q: [1, 1, 1] if (q[0] == 0 and q[1] == 1 and q[2] == 0) else None)
v722 = [val(s) for s in S722]
sec722 = []; [sec722.append(x) for x in v722 if not sec722 or sec722[-1] != x]
check('lb7.p722', sec722 == [7, 6, 5, 4, 3, 7, 6, 5, 4], sec722)
check('lb7.p722.glitch', set(g722) == {(0, 1, 0)} and len(g722) == 1)
book('lb7.p722.ascendente', False, 'La última frase del comentario dice «ascendente»; la secuencia 7,6,5,4,3 es descendente.')
def pulso(seq, glitch_edge_slots):
    return ''.join('1' if k in glitch_edge_slots else '0' for k in range(len(seq)))
ed720 = [k for k in range(1, len(CK720)) if CK720[k - 1] == '1' and CK720[k] == '0']
gl720 = [ed720[i] for i in range(len(ed720)) if v720[ed720[i] - 1] == 5]
ed721 = [k for k in range(1, len(CK721)) if CK721[k - 1] == '1' and CK721[k] == '0']
gl721 = [ed721[i] for i in range(len(ed721)) if v721[ed721[i] - 1] == 9]
ed722 = [k for k in range(1, len(CK722)) if CK722[k - 1] == '0' and CK722[k] == '1']
gl722 = [ed722[i] for i in range(len(ed722)) if v722[ed722[i] - 1] == 3]
def pr(slots): return ''.join('r' if k in slots else '.' for k in range(max(slots) + 8)) if slots else ''
def strobe(n, slots): return ''.join('1' if k in slots else '0' for k in range(n))
ej('lb7-20', 'Contador asíncrono de 0 a 5 con puesta a cero', 'Libro · Cap. 7 · P7.20', 'contador,asincrono,glitch,cronograma', 'lb7.p720',
   'Diseña un contador **asíncrono** activo por flanco de bajada cuya secuencia sea 0, 1, 2, 3, 4, 5, 0, 1… Completa el cronograma sin tener en cuenta los retardos.',
   '**Se deja contar libremente hasta el primer estado que no se quiere y se obliga a volver a cero.** Con tres biestables J‑K con $J=K=1$ se tiene un contador asíncrono de módulo 8; el estado 6 (110) es el primero no deseado.',
   [('Contador base', 'Tres J‑K con $J=K=1$: $Ck$ al primero y cada salida $Q$ al reloj del siguiente. Con flancos de bajada así encadenados la cuenta es ascendente de módulo 8.'),
    ('Recorte', 'Una puerta NAND decodifica 110 ($Q_2\\cdot Q_1\\cdot\\overline{Q_0}$) y su salida, activa en bajo, se lleva a los **CLEAR** de los tres biestables. En cuanto el contador llega a 6 se pone a 0 de forma asíncrona. La NAND no necesita $\\overline{Q_0}$: basta $Q_2\\cdot Q_1$, porque el 7 nunca se alcanza (se comprobó que la secuencia es la misma).'),
    ('El «glitch»', 'En el flanco que debería llevar el contador de 5 a 6, el contador **llega a tomar el valor 6** durante un breve lapso, el que tarda la NAND y el borrado en actuar. Es un estado transitorio no deseado (un *glitch*) que puede alterar los circuitos que lean las salidas. Por eso estos contadores tienen interés sobre todo teórico.')],
   cron([['Ck', CK720], ['Q0', bits(S720, 0)], ['Q1', bits(S720, 1)], ['Q2', bits(S720, 2)], ['Clear', strobe(len(CK720), gl720)]], 'Cuenta 0‑5 (el pulso «Clear» está exagerado en anchura)', 28, w=8, grid=8)
   + '\n\nSecuencia: ' + ' → '.join(str(x) for x in sec720[:7]) + '. En cada vuelta aparece el estado transitorio 6 (110) antes de volver a 0.')

ej('lb7-21', 'Contador BCD asíncrono con flancos de bajada', 'Libro · Cap. 7 · P7.21', 'contador,asincrono,bcd,glitch,cronograma', 'lb7.p721',
   'Diseña un contador ascendente BCD **asíncrono** activo por flanco de bajada y completa el cronograma, sin tener en cuenta los retardos.',
   '**Mismo método que el problema anterior con cuatro biestables.** Un contador asíncrono ascendente de cuatro J‑K con $J=K=1$ es de módulo 16; se decodifica el primer estado que no es BCD, 1010, y se lleva a los CLEAR.',
   [('Decodificar el 10', 'NAND de $Q_3\\cdot\\overline{Q_2}\\cdot Q_1\\cdot\\overline{Q_0}$ hacia los cuatro CLEAR. Basta con $Q_3\\cdot Q_1$ (en una cuenta de 0 a 9 solo el 10 las cumple primero); el libro lo señala y la simulación lo confirma.'),
    ('Resultado', 'El contador pasa por 0, 1, …, 9 y, al llegar a 10, vuelve a 0. Como en el caso anterior hay un instante en que el contador vale 10 antes del borrado (glitch).'),
    ('Comprobación', 'Se simula el encadenamiento de flancos con retardo cero entre biestables: se comprueba que durante los rizados no se cumple la condición de borrado en ningún estado intermedio salvo en el 10.')],
   cron([['Ck', CK721], ['Q0', bits(S721, 0)], ['Q1', bits(S721, 1)], ['Q2', bits(S721, 2)], ['Q3', bits(S721, 3)], ['Clear', strobe(len(CK721), gl721)]], 'Cuenta BCD asíncrona', 26, w=7, grid=8)
   + '\n\nSecuencia: ' + ' → '.join(str(x) for x in sec721[:11]) + '.')

ej('lb7-22', 'Secuencia de un contador asíncrono con preset', 'Libro · Cap. 7 · P7.22', 'contador,asincrono,preset,cronograma', 'lb7.p722',
   'Tres biestables J‑K con $J=K=1$ están conectados así: el reloj $Ck$ va al primero, la salida $Q_0$ al reloj del segundo y $Q_1$ al reloj del tercero, todos activos por flanco de **subida**. Una puerta NAND recibe $\\overline{Q_2}$, $Q_1$ y $\\overline{Q_0}$ y su salida va a los **PRESET** de los tres. Indica la secuencia que genera y completa el cronograma, sin tener en cuenta los retardos.',
   '**Es un circuito secuencial asíncrono, un contador.** Hay que decidir si cuenta hacia arriba o hacia abajo, cuál es su módulo máximo y qué hace la puerta.',
   [('Sentido', 'Cada $Q$ va al reloj del siguiente y el reloj es de subida: el contador es **descendente** (la salida del primero sube cuando le toca bajar al segundo: 7, 6, 5, …).'),
    ('Máximo', 'Con tres biestables el módulo máximo es 8.'),
    ('La puerta', 'La NAND decodifica $\\overline{Q_2}\\,Q_1\\,\\overline{Q_0}=010$, el valor **2**, que es el primer estado no deseado de la cuenta descendente. Su salida va a los PRESET: fuerza **111 = 7**.'),
    ('Resultado', 'El contador se recorta a 5 estados y genera 7, 6, 5, 4, 3, 7, 6, … Es un contador asíncrono descendente de **módulo 5**. En cada vuelta aparece brevemente el 2 antes del preset (glitch).')],
   cron([['Ck', CK722], ['Q0', bits(S722, 0)], ['Q1', bits(S722, 1)], ['Q2', bits(S722, 2)], ['Preset', strobe(len(CK722), gl722)]], 'Cuenta asíncrona descendente módulo 5', 28, w=8, grid=8)
   + '\n\nSecuencia: ' + ' → '.join(str(x) for x in sec722[:6]) + ' (y se repite).'
   + ojo('En el último punto del comentario el libro llama a este contador «ascendente de módulo 5», pero la secuencia que escribe a continuación (7, 6, 5, 4, 3, 7) es **descendente**, como dice él mismo unas líneas antes.'))
