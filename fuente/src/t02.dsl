%% id=t02
%% group=tema
%% n=2
%% title=Tema 2 · Sistemas de numeración, operaciones y códigos
%% short=T2 · Numeración y códigos
%% sub=Cómo escribe números un circuito: binario, complemento a dos, BCD, Gray y detección de errores.

@box idea | Desde cero
Un circuito solo guarda ceros y unos. Para guardar el número 156, el 37 negativo o la letra «A», hace falta un **acuerdo** sobre qué significa cada combinación de bits. Ese acuerdo es un **código**. Este tema recoge los códigos que vas a usar siempre: binario natural, hexadecimal, complemento a dos, BCD, Gray y paridad.
@end

## Binario, octal y hexadecimal

En decimal cada posición vale una potencia de 10. En binario, una potencia de 2:

$$1011_2 = 1\cdot 2^3 + 0\cdot 2^2 + 1\cdot 2^1 + 1\cdot 2^0 = 11_{10}$$

**Del decimal al binario:** divide entre 2 una y otra vez y apunta los restos. Lee los restos de abajo arriba.

**Hexadecimal:** agrupa los bits de 4 en 4 desde la derecha. Cada grupo es una cifra (0-9, A=10, B=11, … F=15). Es la forma corta de escribir binario. **Octal:** agrupa de 3 en 3.

@ej t2-e1|De decimal a binario, hexadecimal y octal|Ejemplo T2|arit|t2.dec2bin
@enun
Pasa $156_{10}$ a binario, hexadecimal y octal.
@end
@antes
Usas la división sucesiva entre 2 y la agrupación de bits en bloques de 4 (hex) y de 3 (octal).
@end
@paso Divisiones entre 2
$156\to78\to39\to19\to9\to4\to2\to1\to0$ con restos $0,0,1,1,1,0,0,1$. Leídos de abajo arriba: $10011100_2$.
@end
@paso Agrupa de 4 en 4
$1001\;1100$ = $9\;C$. Es decir, $9C_{16}$.
@end
@paso Agrupa de 3 en 3
$010\;011\;100$ = $2\;3\;4$. Es decir, $234_8$. (Se rellena con un 0 a la izquierda.)
@end
@res
$156_{10}=10011100_2=9C_{16}=234_8$. Comprobación: $9\cdot16+12=156$.
@end
@end

**Parte fraccionaria:** multiplica por 2 y apunta la parte entera cada vez. Ejemplo: $0{,}6875\to 1{,}375\to 0{,}75\to 1{,}5\to 1{,}0$ da $0{,}1011_2$.

@box ojo | Muchos decimales no caben en binario
$0{,}1_{10}$ en binario es periódico, igual que $1/3$ en decimal. Por eso un circuito nunca guarda $0{,}1$ exacto: guarda una aproximación.
@end

## Números con signo: complemento a dos

Con $n$ bits hay $2^n$ combinaciones. Para repartirlas entre positivos y negativos se usa el **complemento a dos (C2)**. El bit más significativo (MSB) es el **signo**: 0 positivo, 1 negativo.

**Rango con $n$ bits:**

$$-2^{\,n-1}\;\le\; N\;\le\; 2^{\,n-1}-1$$

Con 8 bits: de $-128$ a $+127$. Hay un negativo más que positivos.

**Cambiar de signo:** invierte todos los bits y suma 1. Ejemplo con $37=00100101$: invierto, $11011010$; sumo 1, $11011011=-37$.

**Intuición:** en C2 el peso del MSB es $-2^{n-1}$ (negativo). Por eso $11011011=-128+64+16+8+2+1=-37$.

@ej t2-e2|Sumar en complemento a dos y detectar desbordamiento|Ejemplo T2|arit|t2.c2_37,t2.ov1,t2.ov_carry
@enun
Con 8 bits en C2: (a) escribe $-37$; (b) calcula $45+(-20)$; (c) calcula $100+50$ y di qué pasa.
@end
@antes
Teoría: C2 = invertir y sumar 1; la suma de C2 es la suma binaria normal; hay **desbordamiento** si el resultado no cabe en el rango $[-128,127]$.
@end
@paso (a) $-37$
$37=00100101$. Invierto: $11011010$. Sumo 1: $11011011$.
@end
@paso (b) $45+(-20)$
$45=00101101$, $-20=11101100$. Suma: $1\,00011001$. Se descarta el acarreo que sale del byte: queda $00011001=25$. Correcto.
@end
@paso (c) $100+50$
$100=01100100$, $50=00110010$. Suma: $10010110$. El MSB vale 1, así que se lee como negativo: $-106$. Es **incorrecto**: $150>127$. Hay desbordamiento.
@end
@res
(a) $11011011$. (b) $00011001=25$. (c) $10010110$ (se leería $-106$) y hay **desbordamiento**.
@end
@end

@box formula | Cómo detectar el desbordamiento en C2
- Dos positivos que suman un negativo, o dos negativos que suman un positivo: hay desbordamiento.
- Equivale a: el acarreo que entra al bit de signo es distinto del acarreo que sale de él.
- Un positivo más un negativo **nunca** desborda.
@end

@sim bcdadd

## BCD: decimal en cuatro bits

En **BCD** (decimal codificado en binario) cada cifra decimal se escribe con 4 bits, y solo se usan las combinaciones $0000$ a $1001$. Así $47_{10}=0100\;0111_{BCD}$. Es cómodo para mostrar números en displays, pero ocupa más bits y sumar es más difícil.

**Suma en BCD:** suma cada cifra en binario. Si el resultado de una cifra supera 9 (o hay acarreo), **suma 6** para saltarte las 6 combinaciones prohibidas ($1010$ a $1111$).

@ej t2-e3|Suma en BCD: 38 + 45|Ejemplo T2|arit|t2.bcdadd,t2.bcdadd_bits,t2.bcd47
@enun
Suma $38+45$ en BCD.
@end
@antes
Teoría: BCD, y la corrección «+6» cuando una cifra pasa de 9.
@end
@paso Escribe los sumandos
$38=0011\;1000$ y $45=0100\;0101$.
@end
@paso Suma binaria
$0011\,1000+0100\,0101=0111\,1101$.
@end
@paso Corrige la cifra de abajo
Las cifras bajas suman $1101=13>9$: es inválido. Suma $0110$: $0111\,1101+0110=1000\,0011$.
@end
@res
$1000\;0011_{BCD}=83$. Comprobación: $38+45=83$.
@end
@end

## Código Gray y detección de errores

**Gray:** una secuencia de códigos donde de uno al siguiente **cambia un solo bit**. Para 3 bits: $000,001,011,010,110,111,101,100$. Se usa en codificadores de posición: si dos bits cambiaran a la vez y uno llegara antes, leerías una posición falsa. Con Gray el error máximo es una posición.

**Paso de binario a Gray:** $g_i=b_i\oplus b_{i+1}$ (el MSB se copia). Es decir, $g=b\oplus(b\gg1)$.

**Paridad:** se añade un bit para que el número total de unos sea par (paridad par) o impar. Detecta **un** error, pero no sabe dónde está. Para $1011001$ hay cuatro unos: el bit de paridad par es 0.

**Hamming (7,4):** añade 3 bits de paridad a 4 de datos de forma que se **corrige** un error. Los bits $p_1,p_2,p_3$ están en las posiciones 1, 2 y 4. Para los datos $1011$ la palabra es $0110011$. Si falla un bit, los tres chequeos de paridad forman un número binario que **es la posición del bit erróneo**.

@box mas | Más a fondo: distancia de Hamming
La **distancia** entre dos palabras es el número de bits en que difieren. Un código con distancia mínima $d$ detecta $d-1$ errores y corrige $\lfloor (d-1)/2\rfloor$. La paridad simple tiene $d=2$ (detecta 1, corrige 0). Hamming (7,4) tiene $d=3$ (corrige 1). Se ha comprobado por código que corrige cualquiera de los 7 posibles errores de un bit en las 16 palabras.
@end

@box falla | Qué suele fallar
- Olvidar que en C2 el rango **no es simétrico**: con 8 bits el mínimo es $-128$, y no tiene opuesto positivo.
- Descartar el acarreo final y creer que ya está: hay que mirar el **desbordamiento** aparte.
- En BCD, sumar 6 a todas las cifras en vez de solo a las que pasan de 9.
- Mezclar «mayor que 9» con «hay acarreo»: ambas condiciones obligan a corregir.
@end

@box formula | Fórmulas clave
- $N$ combinaciones $\Rightarrow$ $n=\lceil\log_2 N\rceil$ bits.
- C2 de $n$ bits: $-2^{n-1}\le N\le 2^{n-1}-1$.
- $-N = \overline{N}+1$ (invertir y sumar 1).
- Gray: $g=b\oplus(b\gg1)$.
- Suma BCD: si cifra $>9$, sumar $0110$.
@end

@card ¿Rango de un número en C2 de $n$ bits? || $-2^{n-1}$ a $2^{n-1}-1$.
@card ¿Cómo se niega un número en C2? || Invertir todos los bits y sumar 1.
@card ¿Cuándo hay desbordamiento en C2? || Cuando sumas dos números del mismo signo y el resultado tiene signo contrario.
@card ¿Corrección en la suma BCD? || Si la cifra pasa de 9 (o hay acarreo), sumar $0110$.
@card ¿Qué caracteriza al código Gray? || Entre dos códigos consecutivos cambia un solo bit.
@gloss BCD | Decimal codificado en binario: cada cifra decimal en 4 bits.
@gloss Complemento a dos | Representación de enteros con signo: el MSB pesa $-2^{n-1}$.
@gloss Desbordamiento | El resultado de una operación no cabe en el número de bits disponible.
@gloss Código Gray | Código en el que dos palabras consecutivas difieren en un solo bit.
@gloss Distancia de Hamming | Número de bits en que difieren dos palabras de un código.
@gloss Paridad | Bit extra que hace par (o impar) el número de unos de una palabra.

@q t2
¿Cuál es el rango de un entero en complemento a dos con 6 bits?
+ de $-32$ a $+31$
- de $-31$ a $+32$
- de $-32$ a $+32$
- de $0$ a $63$
> Con $n=6$: $-2^{5}=-32$ hasta $2^{5}-1=31$.
@end
@q t2
En C2 de 8 bits sumas $01100100+00110010$. ¿Qué ocurre?
+ Hay desbordamiento: dos positivos dan un resultado con MSB igual a 1
- No hay problema: $150$ cabe en 8 bits
- Hay un error de paridad
- Se produce acarreo y el resultado es correcto
> $100+50=150>127$. El resultado $10010110$ se lee como $-106$.
@end
@q t2
$0100\,0111$ en BCD representa:
+ 47
- 71
- 4,7
- 0x47 en decimal, es decir, 71
> Cada grupo de 4 bits es una cifra decimal: 4 y 7.
@end
@q t2
Para 3 bits, ¿qué código de Gray sigue a $011$?
+ $010$
- $100$
- $111$
- $000$
> La secuencia es 000, 001, 011, 010, 110, 111, 101, 100.
@end
