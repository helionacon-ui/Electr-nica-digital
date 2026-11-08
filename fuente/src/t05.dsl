%% id=t05
%% group=tema
%% n=5
%% title=Tema 5 · Funciones de la lógica combinacional
%% short=T5 · Bloques combinacionales
%% sub=Sumadores, comparadores, multiplexores, decodificadores, codificadores y displays de 7 segmentos.

@box idea | Desde cero
Los mismos circuitos se necesitan una y otra vez: sumar, comparar, elegir una entrada entre varias, convertir un número en una línea activa. Los fabricantes los venden ya hechos (bloques **MSI**). Diseñar «a nivel de subsistema» es **usar estos bloques como piezas** en lugar de dibujar puertas. Saber qué hace cada pieza y cómo conectarla es la mitad del examen de combinacional.
@end

## Sumadores

- **Semisumador** (suma 2 bits): $S=A\oplus B$, $C_{out}=A\cdot B$.
- **Sumador completo** (suma 2 bits y el acarreo de entrada $C_{in}$): $S=A\oplus B\oplus C_{in}$ y $C_{out}=AB+C_{in}(A\oplus B)$.

Se ha comprobado por código con las 8 combinaciones que da la suma binaria correcta.

**Sumador de $n$ bits con acarreo en cascada (*ripple carry*):** encadenas $n$ sumadores completos, el $C_{out}$ de uno es el $C_{in}$ del siguiente. Es barato, pero el acarreo tiene que **viajar** por todos: con 4 etapas y 2 puertas de 10 ns por etapa, el retardo es $4\cdot2\cdot10=80$ ns. Los **sumadores con acarreo anticipado** (*carry look-ahead*) calculan los acarreos en paralelo y son más rápidos.

**Restar con un sumador:** $A-B=A+\overline{B}+1$ (invertir $B$ y poner $C_{in}=1$). Con XOR en la entrada $B$ el mismo circuito suma o resta según una señal de control.

@ej t5-e1|Sumador de 4 bits|Ejemplo T5|arit,msi|t5.fa,t5.ripple4
@enun
Dibuja cómo se construye un sumador de 4 bits con sumadores completos y calcula su retardo en el peor caso si cada puerta tarda 10 ns y cada sumador completo tiene dos niveles de puertas en el camino del acarreo.
@end
@antes
Teoría: sumador completo, cascada de acarreo, retardo = suma de retardos de la ruta más larga.
@end
@paso Cascada
Los bits $A_3A_2A_1A_0$ y $B_3B_2B_1B_0$ entran por pares en cuatro sumadores completos. $C_{in}$ del primero es 0 y cada $C_{out}$ va al $C_{in}$ siguiente.
@end
@paso Ruta crítica
El peor caso es cuando el acarreo nace en el bit 0 y viaja hasta el bit 3: pasa por 4 sumadores.
@end
@paso Retardo
$4\ \text{etapas}\times 2\ \text{puertas}\times10\ \text{ns}=80$ ns.
@end
@res
Cuatro sumadores completos en cascada. Retardo del acarreo: **80 ns**.
@end
@end

## Comparadores

Un comparador de 1 bit da tres salidas: $A>B=A\overline{B}$, $A=B=\overline{A\oplus B}$ y $A<B=\overline{A}B$. Para $n$ bits se compara **de más a menos significativo**: manda el primer bit que difiere. Los circuitos integrados tienen entradas de cascada para unir varios.

## Multiplexores

Un **multiplexor** (MUX) de $2^k$ a 1 tiene $2^k$ entradas de datos, $k$ entradas de **selección** y una salida: copia a la salida la entrada que indica el número de selección. Es un «selector de vía».

$$Y=\sum_{i=0}^{2^k-1} m_i(S)\cdot D_i$$

**Truco de examen: implementar una función con un MUX.** Una función de $n$ variables cabe en un MUX de $2^{n-1}$ a 1. Las $n-1$ primeras variables van a la selección y la última variable (o su negada, 0 o 1) a cada entrada de datos.

@ej t5-e2|Implementar una función con un MUX 4:1|Ejemplo T5|comb,msi|t5.mux_ok
@enun
Implementa $f(A,B,C)=\Sigma m(1,2,4,7)$ con un multiplexor 4:1. Usa $A$ y $B$ como selección.
@end
@antes
Teoría: para cada valor de $(A,B)$, mira cómo depende $f$ de $C$ en las dos filas correspondientes: da 0, 1, $C$ o $\overline{C}$. Eso es lo que va a la entrada $D_i$ de ese valor.
@end
@paso Mira las parejas de filas
$AB=00$: filas 0 y 1. $f(0)=0$, $f(1)=1$ $\Rightarrow$ $D_0=C$.
$AB=01$: filas 2 y 3. $f=1,0$ $\Rightarrow$ $D_1=\overline{C}$.
$AB=10$: filas 4 y 5. $f=1,0$ $\Rightarrow$ $D_2=\overline{C}$.
$AB=11$: filas 6 y 7. $f=0,1$ $\Rightarrow$ $D_3=C$.
@end
@paso Conecta
Selección: $S_1=A$, $S_0=B$. Entradas: $D_0=C$, $D_1=\overline{C}$, $D_2=\overline{C}$, $D_3=C$. Solo hace falta un inversor.
@end
@res
$Y=\text{MUX}(A,B;\,C,\overline{C},\overline{C},C)$. Comprobado con las 8 combinaciones.
@end
@end

## Decodificadores y codificadores

- **Decodificador** $k$ a $2^k$: activa **una** salida según el número de entrada. Cada salida es un **minitérmino** de las entradas. Por eso con un decodificador y una puerta OR puedes implementar cualquier función: juntas las salidas de los minitérminos que valen 1. Tiene entrada de habilitación (*enable*).
- **Codificador:** hace lo inverso: de $2^k$ líneas, activa el código de la línea activa. El **codificador de prioridad** decide cuando hay varias líneas a 1: gana la de mayor índice. Para las entradas $0110$ da $2$ y para $1010$ da $3$.

**Ampliar:** con decodificadores 2:4 puedes montar uno de 4:16 en árbol: uno de 2:4 habilita a cuatro más.

@fig dectree {"cap":"Un decodificador 4:16 hecho con cinco 2:4. Los dos bits altos eligen cuál de los cuatro de la derecha se habilita; los dos bajos eligen la salida dentro de él."}

## Display de 7 segmentos

Un display tiene 7 LED (a a g). Un **decodificador BCD a 7 segmentos** recibe 4 bits (cifra de 0 a 9) y da 7 salidas. Las combinaciones $1010$ a $1111$ no existen en BCD: son **indiferentes**, y se aprovechan para simplificar. En las placas Basys los segmentos son **activos a nivel bajo**: se encienden con 0.

@box falla | Qué suele fallar
- Montar el sumador sin poner $C_{in}=0$ en el primer bit.
- Confundir qué es selección y qué es dato en un MUX.
- Olvidar la habilitación (*enable*) de un decodificador o mezclar su polaridad (activa a nivel bajo).
- En el codificador de prioridad, ignorar que **la entrada de mayor índice gana**.
- En el display, olvidar que en la Basys se enciende con 0.
@end

@box formula | Fórmulas clave
- $S=A\oplus B\oplus C_{in}$; $C_{out}=AB+C_{in}(A\oplus B)$.
- $A-B=A+\overline{B}+1$.
- MUX $2^k:1$ implementa cualquier función de $k+1$ variables.
- Salida $i$ de un decodificador $=m_i$ (minitérmino).
@end

@card ¿Ecuación del acarreo de un sumador completo? || $C_{out}=AB+C_{in}(A\oplus B)$.
@card ¿Cómo se resta con un sumador? || $A+\overline{B}+1$: se invierte $B$ y se pone $C_{in}=1$.
@card ¿Qué número de selección necesita un MUX de 8 a 1? || 3 bits ($2^3=8$).
@card ¿Qué es cada salida de un decodificador? || Un minitérmino de las entradas.
@card ¿Qué hace un codificador de prioridad? || Entrega el código de la entrada activa de mayor índice cuando hay varias.
@gloss MSI | Integración de media escala: bloques como sumadores, multiplexores o decodificadores.
@gloss Multiplexor | Selector que copia a la salida una de varias entradas según un código de selección.
@gloss Decodificador | Activa una única salida según el código binario de entrada.
@gloss Codificador de prioridad | Da el código de la línea activa de mayor prioridad.
@gloss Acarreo anticipado | Técnica que calcula los acarreos en paralelo para acelerar un sumador.

@q t5
Para implementar una función de 4 variables con un solo multiplexor, ¿cuál es el mínimo?
+ MUX 8:1
- MUX 4:1
- MUX 16:1 y nada más
- Imposible con un solo MUX
> Con $2^{n-1}=8$ entradas de datos y 3 variables en selección; la cuarta va a los datos.
@end
@q t5
Un decodificador 3:8 tiene la entrada $101$. ¿Qué salida se activa?
+ $S_5$
- $S_3$
- $S_6$
- $S_1$
> $101_2=5$. Se activa la salida $S_5$.
@end
@q t5
Un sumador de 8 bits con acarreo en cascada tiene un retardo de 15 ns por etapa. El retardo del acarreo es:
+ 120 ns
- 15 ns
- 23 ns
- 8 ns
> $8\cdot15=120$ ns: el acarreo atraviesa las 8 etapas.
@end
