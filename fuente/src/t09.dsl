%% id=t09
%% group=tema
%% n=9
%% title=Tema 9 · Registros de desplazamiento
%% short=T9 · Registros
%% sub=Registros serie/paralelo, contadores en anillo y Johnson, y generadores pseudoaleatorios (LFSR).

@box idea | Desde cero
Un **registro** es un grupo de biestables D que guardan una palabra. Un **registro de desplazamiento** además puede **mover** cada bit un lugar a la derecha o a la izquierda en cada flanco, como una cola. Sirve para pasar datos de serie a paralelo (y al revés), para retardar señales, y para construir contadores y generadores de secuencias.
@end

## Cómo funciona

Cada biestable toma como entrada la salida del anterior: $D_i=Q_{i-1}$. En cada flanco, todo se mueve una posición y entra un bit nuevo por un extremo.

Si metes en serie los bits $1,0,1,1$ en un registro de 4 bits, tras 4 flancos tiene $1011$ en paralelo. Se ha comprobado por código.

@fig timing {"signals":[["CLK",null],["Din",[1,0,1,1,0,0,0,0]],["Q0",[0,1,0,1,1,0,0,0]],["Q1",[0,0,1,0,1,1,0,0]],["Q2",[0,0,0,1,0,1,1,0]]],"title":"Registro de desplazamiento de 3 bits: el dato avanza una posición por flanco","slots":8,"cap":"Cada bit tarda un ciclo en pasar de una etapa a la siguiente."}

## Los cuatro modos

| Entrada → Salida | Nombre | Uso |
|---|---|---|
| Serie → serie | SISO | Línea de retardo |
| Serie → paralelo | SIPO | Recibir datos de un puerto serie |
| Paralelo → serie | PISO | Transmitir una palabra por un solo cable |
| Paralelo → paralelo | PIPO | Registro de almacenamiento |

Los registros universales (74x194) tienen entradas de **modo** que eligen entre cargar en paralelo, desplazar a la izquierda, a la derecha o mantener.

## Contadores basados en registros

- **Contador en anillo:** se realimenta la salida del último en la entrada del primero con **un solo 1** circulando: $1000\to0100\to0010\to0001\to1000$. Con $n$ biestables da **$n$ estados**. Es un decodificador gratis: cada salida es un estado.
- **Contador Johnson (anillo retorcido):** se realimenta la salida **negada**. Para 4 bits: $0000,\allowbreak 1000,\allowbreak 1100,\allowbreak 1110,\allowbreak 1111,\allowbreak 0111,\allowbreak 0011,\allowbreak 0001$. Da **$2n$ estados** y cada transición cambia un solo bit (como un Gray).

@ej t9-e1|Secuencias de anillo y de Johnson|Ejemplo T9|cont|t9.anillo,t9.johnson
@enun
Un registro de 4 bits parte de $0000$ (Johnson) y de $1000$ (anillo). Escribe la secuencia y cuántos estados distintos tiene cada uno.
@end
@antes
Teoría: anillo: $D_3=Q_0$ (se desplaza a la derecha y el LSB vuelve al MSB). Johnson: $D_3=\overline{Q_0}$.
@end
@paso Anillo
$1000\to0100\to0010\to0001\to1000$. **4 estados** para 4 biestables.
@end
@paso Johnson
$0000\to1000\to1100\to1110\to1111\to0111\to0011\to0001\to0000$. **8 estados** para 4 biestables.
@end
@res
Anillo: 4 estados. Johnson: 8 estados ($2n$).
@end
@end

## LFSR: registro con realimentación lineal

Si se realimenta la entrada con un **XOR** de algunas salidas, el registro recorre una secuencia pseudoaleatoria. Con 4 bits y realimentación $Q_3\oplus Q_2$ se recorren los **15** estados no nulos antes de repetir (periodo $2^4-1$). Se usa en comunicaciones, cifrado sencillo y generadores de pruebas. El estado todo ceros es un **atasco**: nunca sale de él.

@box falla | Qué suele fallar
- Dirección del desplazamiento: dibuja siempre qué bit entra y cuál sale.
- Confundir anillo ($n$ estados) con Johnson ($2n$ estados).
- Olvidar poner el estado inicial (un solo 1 en el anillo): si arranca en 0000 no hay nada que circule.
- En un LFSR, arrancar en todo ceros.
@end

@box formula | Fórmulas clave
- Anillo: $n$ estados; Johnson: $2n$; LFSR máximo: $2^n-1$.
- Serie → paralelo de $n$ bits: $n$ ciclos de reloj.
@end

@card ¿Cuántos estados tiene un contador Johnson de $n$ bits? || $2n$.
@card ¿Qué entra en el primer biestable de un contador en anillo? || La salida del último.
@card ¿Qué es SIPO? || Registro serie-entrada, paralelo-salida.
@card ¿Periodo máximo de un LFSR de $n$ bits? || $2^n-1$.
@gloss Registro de desplazamiento | Cadena de biestables en la que cada uno toma el valor del anterior en cada flanco.
@gloss Contador en anillo | Registro de desplazamiento realimentado con un único 1 que circula.
@gloss Contador Johnson | Registro de desplazamiento que realimenta la salida negada; $2n$ estados.
@gloss LFSR | Registro de desplazamiento con realimentación lineal (XOR) que genera secuencias pseudoaleatorias.

@q t9
Un contador Johnson de 5 bits tiene:
+ 10 estados
- 5 estados
- 32 estados
- 25 estados
> $2n=10$.
@end
@q t9
Un registro de desplazamiento de 8 bits recibe un dato serie. ¿Cuántos flancos de reloj hacen falta para cargar una palabra completa?
+ 8
- 1
- 16
- 3
> Entra un bit por flanco.
@end
