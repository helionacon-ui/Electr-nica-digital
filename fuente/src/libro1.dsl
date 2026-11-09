%% id=libro1
%% group=ejer
%% n=3.1
%% title=Libro de problemas · Capítulo 1 · Códigos binarios
%% short=Libro · Cap. 1 Códigos
%% sub=13 problemas resueltos: conversiones entre decimal, binario, hexadecimal, octal, BCD y Gray; rangos; complemento a 1, a 2 y a 10; sumas y desbordamiento.

@box idea | Cómo se usa esta sección
Son los problemas resueltos del capítulo 1 del libro *Problemas resueltos de electrónica digital* (ITES‑Paraninfo), reformulados con otras palabras y resueltos de nuevo. Cada resultado se ha calculado con un programa y se ha comparado con el valor que da el libro. Si hay alguna diferencia, aparece una nota «Ojo». La teoría está en [[t02|el tema 2]].
@end

@ej lb1-1|Binario a decimal y decimal a binario|Libro · Cap. 1 · P1.1|arit|lb1.p11
@enun
Pasa a decimal veinte números binarios sin signo y pasa a binario veinte números decimales.
@end
@antes
**Método:** de binario a decimal se suman los pesos $2^i$ de los bits que valen 1. De decimal a binario se divide entre 2 y se leen los restos de abajo arriba. Los ceros a la izquierda no cambian el valor.
@end
@paso Binario a decimal
- $01_2=1$
- $1101_2=13$
- $1100_2=12$
- $1111_2=15$
- $0011_2=3$
- $0101_2=5$
- $1010_2=10$
- $0000_2=0$
- $000000_2=0$
- $110011_2=51$
- $10101_2=21$
- $0100011_2=35$
- $01111000_2=120$
- $0110011_2=51$
- $000000011_2=3$
- $11011_2=27$
- $011_2=3$
- $1111111111_2=1023$
- $100000001_2=257$
- $00110_2=6$
@end
@paso Decimal a binario
- $1=1_2$
- $7=111_2$
- $9=1001_2$
- $12=1100_2$
- $34=100010_2$
- $32=100000_2$
- $33=100001_2$
- $1=1_2$
- $1=1_2$
- $100=1100100_2$
- $205=11001101_2$
- $63=111111_2$
- $64=1000000_2$
- $4=100_2$
- $56=111000_2$
- $62=111110_2$
- $1023=1111111111_2$
- $1024=10000000000_2$
- $0=0_2$
- $15=1111_2$
@end
@paso Ejemplo con el método de aproximación
Para $205$: cabe $128$ (resto $77$), cabe $64$ (resto $13$), no cabe $32$ ni $16$, cabe $8$ (resto $5$), no cabe $2$, cabe $4$ y cabe $1$: $205=128+64+8+4+1=11001101_2$.
@end
@res
Todas las conversiones se han calculado con código y coinciden con el libro. Regla útil: $2^{10}-1=1023$ es diez unos.
@end
@end


@ej lb1-2|Hexadecimal, octal, decimal y binario|Libro · Cap. 1 · P1.2|arit|lb1.p12
@enun
Dado un número escrito en una de las bases (hexadecimal, octal o decimal), escribe su valor en las otras tres bases y en binario. Una de las filas está mal escrita: detéctala.
@end
@antes
**Atajo:** el hexadecimal agrupa los bits de 4 en 4 y el octal de 3 en 3. Para ir de decimal a otra base, lo más cómodo es pasar antes por binario.
@end
@paso Tabla de resultados
| Dato | Hex | Octal | Decimal | Binario |
|---|---|---|---|---|
| 12A (hex) | 12A | 452 | 298 | 100101010 |
| 1700 (octal) | 3C0 | 1700 | 960 | 1111000000 |
| 4 (dec) | 4 | 4 | 4 | 100 |
| FF (hex) | FF | 377 | 255 | 11111111 |
| 6432 (octal) | D1A | 6432 | 3354 | 110100011010 |
| 17 (dec) | 11 | 21 | 17 | 10001 |
| 055 (hex) | 55 | 125 | 85 | 1010101 |
| 034 (octal) | 1C | 34 | 28 | 11100 |
| 8 (dec) | 8 | 10 | 8 | 1000 |
| 3F (hex) | 3F | 77 | 63 | 111111 |
| 25 (dec) | 19 | 31 | 25 | 11001 |
| 178 (octal) | — | — | — | Error |
| 38 (dec) | 26 | 46 | 38 | 100110 |
| 0A1 (hex) | A1 | 241 | 161 | 10100001 |
| 3154 (octal) | 66C | 3154 | 1644 | 11001101100 |
| 16 (dec) | 10 | 20 | 16 | 10000 |
| 10 (octal) | 8 | 10 | 8 | 1000 |
| 09 (hex) | 9 | 11 | 9 | 1001 |
@end
@paso La fila con error
El dato $178_8$ lleva el dígito $8$, y en octal solo existen $0$ a $7$. No es un número octal válido: es una «falta de ortografía», no una operación mal hecha.
@end
@res
$12A_{16}=452_8=298_{10}$, $FF_{16}=377_8=255_{10}$, $D1A_{16}=6432_8=3354_{10}$ y $66C_{16}=3154_8=1644_{10}$.

@box ojo | Errata del libro
En la fila de $D1A_{16}$ el libro imprime $3348$ en decimal. Con los otros tres datos de esa fila ($6432_8$, $110100011010_2$) el valor correcto es $3354$: $13\cdot256+1\cdot16+10=3354$.
@end
@end
@end


@ej lb1-3|Leer una combinación de 4 bits con seis códigos decimales|Libro · Cap. 1 · P1.3|arit|lb1.p13
@enun
Para cada una de las 16 combinaciones de 4 bits, indica qué dígito decimal representa en BCD puro, BCD exceso 3, Aiken, BCD 3321, Gray exceso 3 y BCD 5421. Si la combinación no es válida en ese código, pon un guion.
@end
@antes
**Idea:** un código decimal usa solo 10 de las 16 combinaciones. Las otras 6 son «prohibidas». Aquí se parte de la definición de cada código.
- BCD puro: el dígito en binario.
- Exceso 3: el dígito $+3$.
- Aiken: $0$ a $4$ como en binario y $5$ a $9$ como $11$ a $15$.
- 3321 y 5421: los pesos de los bits valen $3,3,2,1$ y $5,4,2,1$.
- Gray exceso 3: el Gray de $d+3$.
@end
@paso Cómo se construye cada columna
Para obtener las 10 palabras de cada código se aplica su definición a $d=0\ldots9$ y se invierte la tabla: la palabra que no aparece se marca con un guion. Se han verificado los pesos del 3321 y del 5421, que Aiken y exceso 3 son autocomplementarios ($\bar d=9-d$ al invertir los 4 bits) y que el Gray exceso 3 cambia un solo bit entre dígitos consecutivos.
@end
@paso Tabla
| Bits | BCD puro | BCD XS3 | Aiken | BCD 3321 | Gray XS3 | BCD 5421 |
|---|---|---|---|---|---|---|
| 0000 | 0 | — | 0 | 0 | — | 0 |
| 0001 | 1 | — | 1 | 1 | — | 1 |
| 0010 | 2 | — | 2 | 2 | 0 | 2 |
| 0011 | 3 | 0 | 3 | 3 | — | 3 |
| 0100 | 4 | 1 | 4 | — | 4 | 4 |
| 0101 | 5 | 2 | — | 4 | 3 | — |
| 0110 | 6 | 3 | — | 5 | 1 | — |
| 0111 | 7 | 4 | — | — | 2 | — |
| 1000 | 8 | 5 | — | — | — | 5 |
| 1001 | 9 | 6 | — | — | — | 6 |
| 1010 | — | 7 | — | — | 9 | 7 |
| 1011 | — | 8 | 5 | — | — | 8 |
| 1100 | — | 9 | 6 | 6 | 5 | 9 |
| 1101 | — | — | 7 | 7 | 6 | — |
| 1110 | — | — | 8 | 8 | 8 | — |
| 1111 | — | — | 9 | 9 | 7 | — |
@end
@res
Cada columna tiene exactamente seis guiones. El código más ordenado y simétrico es el exceso 3, porque cada dígito y su complemento a 9 se obtienen invirtiendo los bits.
@end
@end


@ej lb1-4|De decimal a BCD, exceso 3 y Aiken|Libro · Cap. 1 · P1.4|arit|lb1.p14
@enun
Escribe en BCD puro, BCD exceso 3 y BCD Aiken los números decimales de la tabla.
@end
@antes
**Regla:** cada **dígito** decimal se codifica por separado en 4 bits. No se convierte el número entero a binario: $12$ en BCD es $0001\;0010$ y no $1100$.
@end
@paso Tabla
| Decimal | BCD puro | BCD XS3 | Aiken |
|---|---|---|---|
| 4 | 0100 | 0111 | 0100 |
| 32 | 00110010 | 01100101 | 00110010 |
| 99 | 10011001 | 11001100 | 11111111 |
| 63 | 01100011 | 10010110 | 11000011 |
| 0 | 0000 | 0011 | 0000 |
| 1 | 0001 | 0100 | 0001 |
| 55 | 01010101 | 10001000 | 10111011 |
| 00 | 00000000 | 00110011 | 00000000 |
| 36 | 00110110 | 01101001 | 00111100 |
| 82 | 10000010 | 10110101 | 11100010 |
| 11 | 00010001 | 01000100 | 00010001 |
| 12 | 00010010 | 01000101 | 00010010 |
| 04 | 00000100 | 00110111 | 00000100 |
| 100 | 000100000000 | 010000110011 | 000100000000 |
| 44 | 01000100 | 01110111 | 01000100 |
| 56 | 01010110 | 10001001 | 10111100 |
@end
@paso Dos comprobaciones
Las 16 filas se han decodificado de vuelta y dan el mismo decimal. Además $99$ en Aiken es $1111\;1111$ y en exceso 3 es $1100\;1100$.
@end
@res
Cada dígito ocupa 4 bits: $100$ ocupa 12 bits en BCD ($0001\;0000\;0000$) frente a 7 en binario puro. El BCD es más largo, pero se lee dígito a dígito.
@end
@end


@ej lb1-5|De binario a Gray y de Gray a binario|Libro · Cap. 1 · P1.5|arit|lb1.p15
@enun
Convierte entre binario puro y código Gray las parejas de la tabla. En unas se conoce el binario y en otras el Gray.
@end
@antes
**Binario a Gray:** $G_{n-1}=B_{n-1}$ y $G_i=B_{i+1}\oplus B_i$.
**Gray a binario:** $B_{n-1}=G_{n-1}$ y $B_i=B_{i+1}\oplus G_i$ (se va de izquierda a derecha).
@end
@paso Ejemplo: $11000$ a Gray
$G_4=1$; $G_3=1\oplus1=0$; $G_2=1\oplus0=1$; $G_1=0\oplus0=0$; $G_0=0\oplus0=0$. Resultado $10100$.
@end
@paso Ejemplo: $1000_{Gray}$ a binario
$B_3=1$; $B_2=1\oplus0=1$; $B_1=1\oplus0=1$; $B_0=1\oplus0=1$. Resultado $1111$.
@end
@paso Tabla completa
| Binario | Gray |
|---|---|
| 0011 | 0010 |
| 001 | 001 |
| 11000 | 10100 |
| 01010101 | 01111111 |
| 11110000 | 10001000 |
| 01 | 01 |
| 1111 | 1000 |
| 10000 | 11000 |
| 10111100 | 11100010 |
| 00001 | 00001 |
| 0101001111 | 0111101000 |
| 1000 | 1100 |
| 0010 | 0011 |
| 0110 | 0101 |
| 1001111 | 1101000 |
| 1100 | 1010 |
@end
@res
Las 16 parejas se comprueban en los dos sentidos. En Gray dos números consecutivos se diferencian en un solo bit (comprobado para 0 a 63).
@end
@end


@ej lb1-6|Rango de valores según el número de bits|Libro · Cap. 1 · P1.6|arit|lb1.p16
@enun
Escribe el intervalo de valores que se puede representar con $n$ bits (de 1 a 16) en binario puro sin signo, con bit de signo, en complemento a 1 y en complemento a 2. Después calcula cuántos bits necesitan varias magnitudes reales.
@end
@antes
**Fórmulas:** sin signo $[0,2^n-1]$; bit de signo y C1 $[-(2^{n-1}-1),\,2^{n-1}-1]$; C2 $[-2^{n-1},\,2^{n-1}-1]$. Con un solo bit no cabe el signo: hacen falta al menos 2.
@end
@paso Tabla de rangos
| $n$ | Sin signo | Bit de signo | C1 | C2 |
|---|---|---|---|---|
| 1 | [0, 1] | al menos 2 bits | al menos 2 bits | al menos 2 bits |
| 2 | [0, 3] | [−1, +1] | [−1, +1] | [−2, +1] |
| 3 | [0, 7] | [−3, +3] | [−3, +3] | [−4, +3] |
| 4 | [0, 15] | [−7, +7] | [−7, +7] | [−8, +7] |
| 5 | [0, 31] | [−15, +15] | [−15, +15] | [−16, +15] |
| 6 | [0, 63] | [−31, +31] | [−31, +31] | [−32, +31] |
| 7 | [0, 127] | [−63, +63] | [−63, +63] | [−64, +63] |
| 8 | [0, 255] | [−127, +127] | [−127, +127] | [−128, +127] |
| 9 | [0, 511] | [−255, +255] | [−255, +255] | [−256, +255] |
| 10 | [0, 1023] | [−511, +511] | [−511, +511] | [−512, +511] |
| 11 | [0, 2047] | [−1023, +1023] | [−1023, +1023] | [−1024, +1023] |
| 12 | [0, 4095] | [−2047, +2047] | [−2047, +2047] | [−2048, +2047] |
| 13 | [0, 8191] | [−4095, +4095] | [−4095, +4095] | [−4096, +4095] |
| 14 | [0, 16383] | [−8191, +8191] | [−8191, +8191] | [−8192, +8191] |
| 15 | [0, 32767] | [−16383, +16383] | [−16383, +16383] | [−16384, +16383] |
| 16 | [0, 65535] | [−32767, +32767] | [−32767, +32767] | [−32768, +32767] |
@end
@paso Por qué C2 llega más lejos
Bit de signo y C1 tienen dos ceros ($+0$ y $-0$), así que pierden una combinación. C2 tiene un solo cero y la combinación sobrante es el $-2^{n-1}$ (un 1 seguido de ceros).
@end
@paso Magnitudes reales
| Aplicación | Rango | Bits |
|---|---|---|
| Temperatura ambiente | [-30, 50] | 7 bits en BP con C2 |
| Notas de 100 alumnos (cada una) | [0, 10] | 4 bits en BP |
| Suma de las notas de 100 alumnos | [0, 1000] | 10 bits en BP |
| Pesetas por cajetilla | [0, 500] | 9 bits en BP |
| Velocidad de un coche | [0, 300] | 9 bits en BP |
| Peso de una persona | [0, 200] | 8 bits en BP |
| Suma de 100 pesos | [0, 20000] | 15 bits en BP |
| Altura sobre/bajo el mar (avión incluido) | [-12000, 9000] | 15 bits en BP con C2 |
| Diferencia horaria | [-12, 12] | 5 bits en BP con C2 |
| Puntos de un equipo de baloncesto (supuesto 0 a 200) | [0, 200] | 8 bits en BP |
@end
@paso Lecturas útiles
Para sumar $100$ notas hay que mirar el rango de la **suma** ($0$ a $1000$ ⇒ 10 bits), no solo el de cada nota (4 bits). Con 7 bits en C2 se cubre $-64$ a $+63$ y los $-30\ldots+50$ °C caben.
@end
@res
Se ha comprobado por enumeración de todas las combinaciones hasta 10 bits que los intervalos y el número de valores distintos son los de la tabla.
@end
@end


@ej lb1-7|Las 16 combinaciones de 4 bits leídas como sin signo, C1 y C2|Libro · Cap. 1 · P1.7|arit|lb1.p17
@enun
Escribe el valor decimal de cada combinación de 4 bits según tres lecturas: binario sin signo, binario con signo en C1 y binario con signo en C2.
@end
@antes
**Pista:** si el primer bit es 0, el número es positivo y se lee como binario normal. Si es 1, se obtiene el complemento del número (a 1 o a 2) y se lee con signo menos.
@end
@paso Tabla
| Bits | Sin signo | C1 | C2 |
|---|---|---|---|
| 0000 | 0 | +0 | 0 |
| 0001 | 1 | +1 | +1 |
| 0010 | 2 | +2 | +2 |
| 0011 | 3 | +3 | +3 |
| 0100 | 4 | +4 | +4 |
| 0101 | 5 | +5 | +5 |
| 0110 | 6 | +6 | +6 |
| 0111 | 7 | +7 | +7 |
| 1000 | 8 | −7 | −8 |
| 1001 | 9 | −6 | −7 |
| 1010 | 10 | −5 | −6 |
| 1011 | 11 | −4 | −5 |
| 1100 | 12 | −3 | −4 |
| 1101 | 13 | −2 | −3 |
| 1110 | 14 | −1 | −2 |
| 1111 | 15 | −0 | −1 |
@end
@paso El caso $1000$
En C1: el complemento a 1 de $1000$ es $0111=+7$, luego vale $-7$. En C2: el complemento a 2 es $0111+1=1000$ otra vez. Es el único número que se «muerde la cola»: vale $-2^{n-1}=-8$. Conviene memorizarlo: **un 1 seguido de ceros es $-2^{n-1}$ en C2**.
@end
@res
En C1 existen dos ceros ($0000=+0$ y $1111=-0$). En C2 solo hay uno y por eso llega hasta $-8$.
@end
@end


@ej lb1-8|De decimal con signo a binario con signo|Libro · Cap. 1 · P1.8|arit|lb1.p18
@enun
Escribe cada número decimal con signo en binario puro con bit de signo, en C1 y en C2, usando el menor número de bits posible en cada código.
@end
@antes
**Positivos:** se escriben igual en los tres códigos (un 0 delante y la magnitud).
**Negativos:** con bit de signo se pone un 1 y la magnitud. En C1 se invierten los bits del positivo. En C2 se invierten y se suma 1.
**Anchura:** se cuentan los bits de la magnitud y se añade uno para el signo; en C2 el $-2^{n-1}$ cabe en $n$ bits.
@end
@paso Ejemplo con $-17$
El positivo es $010001$. Bit de signo: $110001$. C1: $101110$. C2: $101110+1=101111$.
@end
@paso Tabla
| Decimal | Bit de signo | C1 | C2 |
|---|---|---|---|
| +15 | 01111 | 01111 | 01111 |
| +36 | 0100100 | 0100100 | 0100100 |
| +8 | 01000 | 01000 | 01000 |
| +1 | 01 | 01 | 01 |
| 0 | 00 | 00 | 00 |
| −10 | 11010 | 10101 | 10110 |
| −4 | 1100 | 1011 | 100 |
| −9 | 11001 | 10110 | 10111 |
| +17 | 010001 | 010001 | 010001 |
| −17 | 110001 | 101110 | 101111 |
| −1 | 11 | 10 | 11 |
| −106 | 11101010 | 10010101 | 10010110 |
| −64 | 11000000 | 10111111 | 1000000 |
| −63 | 1111111 | 1000000 | 1000001 |
| −44 | 1101100 | 1010011 | 1010100 |
| −0 | 10 | 11 | 00 |
| +99 | 01100011 | 01100011 | 01100011 |
| −99 | 11100011 | 10011100 | 10011101 |
| −1585 | 111000110001 | 100111001110 | 100111001111 |
| +1260 | 010011101100 | 010011101100 | 010011101100 |
@end
@paso Cómo se ha comprobado
Cada palabra se ha vuelto a leer con una función independiente y da el decimal de partida. Además $\text{C2}=\text{C1}+1$ para todos los negativos de 12 bits.
@end
@res
Los positivos son iguales en los tres códigos. En un cero negativo ($-0$) el bit de signo da $10$, el C1 da $11$ y el C2 no lo distingue: $00$.
@end
@end


@ej lb1-9|Leer una combinación con signo: bit de signo, C1 y C2|Libro · Cap. 1 · P1.9|arit|lb1.p19
@enun
Para cada secuencia binaria de la tabla, indica qué número decimal con signo representa si se lee como binario con bit de signo, como C1 y como C2.
@end
@antes
**Lectura:** primer bit 0 → positivo, se lee normal. Primer bit 1 → negativo. Con bit de signo se lee la magnitud del resto. En C1 se invierten los bits y se lee. En C2 se invierten, se suma 1 y se lee (o se usa el peso $-2^{n-1}$ del primer bit).
@end
@paso Ejemplo con $1011001$
Bit de signo: $-25$ (magnitud $011001$). C1: invierto $0100110=38$, luego $-38$. C2: $0100110+1=0100111=39$, luego $-39$.
@end
@paso Tabla
| Secuencia | Bit de signo | C1 | C2 |
|---|---|---|---|
| 100 | −0 | −3 | −4 |
| 00111 | +7 | +7 | +7 |
| 10100 | −4 | −11 | −12 |
| 11000 | −8 | −7 | −8 |
| 10011101 | −29 | −98 | −99 |
| 1100 | −4 | −3 | −4 |
| 011111 | +31 | +31 | +31 |
| 10000 | −0 | −15 | −16 |
| 11111 | −15 | −0 | −1 |
| 01111 | +15 | +15 | +15 |
| 1111 | −7 | −0 | −1 |
| 10010100 | −20 | −107 | −108 |
| 11111111 | −127 | −0 | −1 |
| 1011001 | −25 | −38 | −39 |
| 100000 | −0 | −31 | −32 |
| 0000001 | +1 | +1 | +1 |
@end
@res
La misma secuencia cambia de valor según el código: **primero hay que saber en qué código está escrita**. Cada fila se ha vuelto a codificar con el decimal obtenido y se recupera la secuencia original.
@end
@end


@ej lb1-10|Suma en binario sin signo y desbordamiento|Libro · Cap. 1 · P1.10|arit|lb1.p110
@enun
Suma las parejas de números binarios sin signo de la tabla. Indica el resultado en decimal y si hay desbordamiento al usar tantos bits como tiene el sumando más largo.
@end
@antes
**Regla:** se suma como en decimal, de derecha a izquierda, llevando acarreos. En binario sin signo hay desbordamiento cuando **sale un acarreo del bit más significativo**: el resultado no cabe en $n$ bits. Si un sumando es más corto, se rellena con ceros a la izquierda.
@end
@paso Tabla
| A | B | $n$ | A+B | Decimal | Desborda |
|---|---|---|---|---|---|
| 1100 (12) | 0001 (1) | 4 | 1101 | 13 | no |
| 101000 (40) | 000001 (1) | 6 | 101001 | 41 | no |
| 0001011001 (89) | 1111001010 (970) | 10 | 10000100011 | 1059 | sí |
| 1101001010 (842) | 0000010011 (19) | 10 | 1101011101 | 861 | no |
| 111111111 (511) | 000000001 (1) | 9 | 1000000000 | 512 | sí |
| 00110 (6) | 00110 (6) | 5 | 01100 | 12 | no |
| 11000 (24) | 10011 (19) | 5 | 101011 | 43 | sí |
| 00010 (2) | 00010 (2) | 5 | 00100 | 4 | no |
| 0100001 (33) | 0000101 (5) | 7 | 0100110 | 38 | no |
| 0011011010 (218) | 1110000101 (901) | 10 | 10001011111 | 1119 | sí |
@end
@paso Qué significa «desborda»
Con $n=9$: $111111111+1=1\;000000000$. El 1 de la izquierda no cabe y queda $000000000=0$ en 9 bits, pero el valor real es $511+1=512$. Un contador de 9 bits que pasa de $511$ vuelve a $0$ por el mismo motivo.
@end
@res
Hay desbordamiento exactamente cuando la suma real $\ge 2^n$ (comprobado en las 10 sumas).

@box ojo | Errata del libro
En la tercera fila el libro imprime $25+970$ y un resultado $1\;0000100011$ (desbordamiento, valor $35$). Pero $25+970=995$ cabe en 10 bits y no desborda. El resultado impreso corresponde a $89+970=1059=1\;0000100011$, es decir, al sumando $0001011001$. La tabla de arriba usa ese sumando.
@end
@end
@end


@ej lb1-11|Suma con signo en C1 y en C2|Libro · Cap. 1 · P1.11|arit|lb1.p111
@enun
Suma las parejas de números binarios con signo, una vez interpretadas en C1 y otra en C2. Escribe el resultado en binario y en decimal y comprueba si hay desbordamiento.
@end
@antes
**C2:** se suma como si no tuvieran signo y se **tira** el acarreo final.
**C1:** igual, pero el acarreo final se **recircula**: se vuelve a sumar al resultado.
**Desbordamiento (ambos):** hay desbordamiento si el acarreo que entra en el bit de signo es distinto del que sale de él.
@end
@paso Ejemplo C1: $00101+11100$
Suma: $100001$. El acarreo final es 1: se recircula, $00001+1=00010=+2$. Decimal: $+5+(-3)=+2$.
@end
@paso Resultados en C1
| A | B | A+B | A (dec) | B (dec) | Resultado | Desborda |
|---|---|---|---|---|---|---|
| 00101 | 11100 | 00010 | +5 | −3 | +2 | no |
| 11010 | 00011 | 11101 | −5 | +3 | −2 | no |
| 0001101 | 1101000 | 1110101 | +13 | −23 | −10 | no |
| 1111001 | 0110000 | 0101010 | −6 | +48 | +42 | no |
| 0011 | 1100 | 1111 | +3 | −3 | −0 | no |
@end
@paso Resultados en C2
| A | B | A+B | A (dec) | B (dec) | Resultado | Desborda |
|---|---|---|---|---|---|---|
| 00101 | 11100 | 00001 | +5 | −4 | +1 | no |
| 11010 | 00011 | 11101 | −6 | +3 | −3 | no |
| 0001101 | 1101000 | 1110101 | +13 | −24 | −11 | no |
| 1111001 | 0110000 | 0101001 | −7 | +48 | +41 | no |
| 0011 | 1100 | 1111 | +3 | −4 | −1 | no |
@end
@res
En ninguna suma hay desbordamiento: el número de bits está bien elegido. Los resultados decimales coinciden con la suma de los decimales de partida.
@end
@end


@ej lb1-12|Sumar números decimales pasando antes a C1 o C2|Libro · Cap. 1 · P1.12|arit|lb1.p112
@enun
Codifica los dos sumandos decimales en C1 y en C2, súmalos en binario y di si hay desbordamiento. Usa el menor número de bits que permita escribir los dos sumandos.
@end
@antes
**Orden de trabajo:** 1) elegir $n$; 2) codificar cada sumando (el negativo, como complemento del positivo); 3) sumar; 4) mirar el desbordamiento con los dos últimos acarreos; 5) leer el resultado.
@end
@paso Caso $(-12)+(-20)$
Necesita 6 bits. En C1: $110011+101011=1\;011110$; recirculo y queda $011111$: el resultado debería ser $-32$ y no cabe (el mínimo de C1 con 6 bits es $-31$). **Desbordamiento.** En C2: $110100+101100=1\;100000$, que es $-32$ y sí cabe. **Sin desbordamiento.**
@end
@paso Caso $(+3)+(+3)$
Con el menor $n$ (3 bits) hay desbordamiento en los dos códigos: $011+011=110$, que se leería como negativo. Con 4 bits ($0011+0011=0110=+6$) el resultado es correcto. Elegir $n$ bien evita el desbordamiento.
@end
@paso Todas las sumas
| Código | Suma | $n$ | A | B | A+B | Real | Leído | Desborda |
|---|---|---|---|---|---|---|---|---|
| C1 | +5 + −3 | 4 | 0101 | 1100 | 0010 | +2 | +2 | no |
| C2 | +5 + −3 | 4 | 0101 | 1101 | 0010 | +2 | +2 | no |
| C1 | −5 + +3 | 4 | 1010 | 0011 | 1101 | −2 | −2 | no |
| C2 | −5 + +3 | 4 | 1011 | 0011 | 1110 | −2 | −2 | no |
| C1 | 0 + −12 | 5 | 00000 | 10011 | 10011 | −12 | −12 | no |
| C2 | 0 + −12 | 5 | 00000 | 10100 | 10100 | −12 | −12 | no |
| C1 | −12 + −20 | 6 | 110011 | 101011 | 011111 | −32 | +31 | sí |
| C2 | −12 + −20 | 6 | 110100 | 101100 | 100000 | −32 | −32 | no |
| C1 | +3 + +3 | 3 | 011 | 011 | 110 | +6 | −1 | sí |
| C2 | +3 + +3 | 3 | 011 | 011 | 110 | +6 | −2 | sí |
| C1 | −37 + +37 | 7 | 1011010 | 0100101 | 1111111 | 0 | −0 | no |
| C2 | −37 + +37 | 7 | 1011011 | 0100101 | 0000000 | 0 | 0 | no |
| C1 | +3 + +3 | 4 | 0011 | 0011 | 0110 | +6 | +6 | no |
| C2 | +3 + +3 | 4 | 0011 | 0011 | 0110 | +6 | +6 | no |
@end
@res
La regla «acarreo que entra en el bit de signo distinto del que sale» coincide en todos los casos con «el resultado real no cabe en $n$ bits».

@box ojo | Posible errata en el libro
Para $(-37)+(+37)$ el libro marca «desborde». Aplicando la regla no lo hay: en C1 no hay ningún acarreo y el resultado es $1111111=-0$; en C2 el acarreo que entra en el signo y el que sale son ambos 1 y el resultado es $0000000$. El 0 es representable.
@end
@end
@end


@ej lb1-13|Suma en decimal con signo en complemento a 10|Libro · Cap. 1 · P1.13|arit|lb1.p113
@enun
Suma en decimal con signo en complemento a 10 (cuatro dígitos) las parejas $99+103$, $-99+103$ y $99-103$. Indica los dos últimos acarreos para decidir el desbordamiento.
@end
@antes
**C10:** un positivo se escribe con un 0 delante y un negativo es el complemento a 10 del positivo (empieza por 9). Se suma dígito a dígito, se tira el acarreo final y se mira si el acarreo que entra en el dígito de signo coincide con el que sale.
@end
@paso Codificación
$+99=0099$, $+103=0103$, $-99=10^4-99=9901$, $-103=9897$.
@end
@paso Sumas
| Operación | A | B | A+B | Decimal | Acarreos (entra y sale) | Desborda |
|---|---|---|---|---|---|---|
| +99 + +103 | 0099 | 0103 | 0202 | +202 | 0 y 0 | no |
| −99 + +103 | 9901 | 0103 | 0004 | +4 | 1 y 1 | no |
| +99 + −103 | 0099 | 9897 | 9996 | −4 | 0 y 0 | no |
@end
@paso Ejemplo dígito a dígito: $9901+0103$
$1+3=4$; $0+0=0$; $9+1=10$ (llevo 1); $9+0+1=10$ (llevo 1, se tira). Resultado $0004=+4$, con acarreos $1$ y $1$: no hay desbordamiento.
@end
@res
Resultados: $+202$, $+4$ y $-4$. La regla de los dos acarreos se ha comprobado de forma exhaustiva para todas las sumas de 2 y 3 dígitos.
@end
@end

