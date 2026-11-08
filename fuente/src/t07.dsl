%% id=t07
%% group=tema
%% n=7
%% title=Tema 7 · Memorias y circuitos lógicos programables
%% short=T7 · Memorias y PLD
%% sub=ROM, RAM, cómo se calcula su tamaño y cómo una memoria o una PLA implementan funciones.

@box idea | Desde cero
Una **memoria** es una tabla: das una **dirección** y te devuelve el **dato** guardado ahí. Con $k$ líneas de dirección hay $2^k$ posiciones, y cada una guarda $m$ bits. Una memoria $2^k\times m$ guarda $m\cdot2^k$ bits. Ese mismo hecho (una tabla indexada por la entrada) significa que **una ROM es una tabla de verdad con otra forma**: cualquier función combinacional cabe en una ROM.
@end

## Tipos de memoria

| Tipo | Se puede escribir | Se pierde al apagar | Uso típico |
|---|---|---|---|
| **ROM** | No (se programa en fábrica) | No | Código fijo |
| **PROM / EPROM / EEPROM / Flash** | Sí, pocas veces y despacio | No | Firmware, pendrive |
| **SRAM** | Sí, rápido | Sí | Cachés, registros |
| **DRAM** | Sí, necesita refresco | Sí | Memoria principal |

## Tamaño y organización

$$\text{bits totales}=2^{k}\cdot m\qquad k=\log_2(\text{posiciones})$$

- Una memoria de $8$K$\times8$ necesita $k=13$ líneas de dirección ($2^{13}=8192$).
- Una de $64$K$\times16$ guarda $64\cdot1024\cdot16=1\,048\,576$ bits.

**Ampliar la memoria:**

- **Más ancho** (más bits por dato): pon chips en paralelo con las mismas direcciones.
- **Más largo** (más posiciones): pon chips con las líneas altas de dirección pasando por un **decodificador** que habilita un solo chip cada vez.

@ej t7-e1|Ampliar una memoria|Ejemplo T7|msi|t7.chips,t7.dir
@enun
Con chips de $2$K$\times8$ construye una memoria de $8$K$\times16$. ¿Cuántos chips necesitas y cuántas líneas de dirección tiene el conjunto?
@end
@antes
Teoría: ampliar a lo ancho (bits) y a lo largo (posiciones), y el número de líneas de dirección $k=\log_2 N$.
@end
@paso Direcciones
$8$K $=2^{13}$ posiciones: **13** líneas de dirección. Cada chip usa 11 ($2^{11}=2$K).
@end
@paso Ancho
Cada chip da 8 bits y necesito 16: hacen falta **2 chips** en paralelo.
@end
@paso Largo
Cada chip tiene 2K posiciones y necesito 8K: hacen falta $8/2=4$ filas de chips. Las 2 líneas altas ($A_{12},A_{11}$) entran en un decodificador 2:4 que habilita una fila.
@end
@paso Total
$4\times2=8$ chips.
@end
@res
**8 chips** y **13** líneas de dirección.
@end
@end

## La memoria como circuito combinacional

Una ROM de $2^k$ palabras de $m$ bits **es** un circuito de $k$ entradas y $m$ salidas: cada dirección es una fila de la tabla de verdad. Ejemplo: un **sumador completo** ($C_{in},A,B$ como dirección) cabe en una ROM de $8\times2$ cuyo contenido es $0,1,1,2,1,2,2,3$ (el número de unos de la dirección, en binario).

## Lógica programable: PLA, PAL

- **PLA** (*programmable logic array*): un plano **AND programable** genera términos producto y un plano **OR programable** los suma.
- **PAL:** plano AND programable y plano OR **fijo**. Más barata y rápida.
- **Ventaja sobre la ROM:** una ROM genera **todos** los minitérminos ($2^n$), la PLA solo los **términos producto simplificados** que necesitas. Por eso, si simplificas antes (Karnaugh), cabe mucho más en una PLA.

@box mas | Más a fondo: PLD, CPLD y FPGA
Las **PLD** simples (PAL, GAL) tienen decenas de funciones. Las **CPLD** juntan varias PLD con una red de interconexión. Las **FPGA** ([[t12|Tema 12]]) cambian el plano AND-OR por miles de pequeñas tablas (*LUT*) y registros, con interconexión programable: son las más flexibles y las que se usan en el laboratorio.
@end

@box falla | Qué suele fallar
- Calcular las líneas de dirección con el número de bits del dato en vez del número de posiciones.
- Olvidar que 1K = 1024, no 1000.
- Al ampliar «a lo largo», conectar todos los chips habilitados a la vez: solo debe estar activo uno.
- Pensar que la ROM guarda datos «que cambian»: solo se lee.
@end

@box formula | Fórmulas clave
- bits totales $=2^k\cdot m$; $k=\log_2 N$.
- Chips necesarios $=\dfrac{N_{total}}{N_{chip}}\cdot\dfrac{m_{total}}{m_{chip}}$.
- Una ROM $2^n\times m$ implementa $m$ funciones de $n$ variables.
@end

@card ¿Cuántos bits tiene una memoria de $2^k\times m$? || $m\cdot 2^k$ bits.
@card ¿Cuántas líneas de dirección tiene una memoria de 16K posiciones? || 14 ($2^{14}=16384$).
@card ¿Qué diferencia hay entre ROM y RAM? || La ROM solo se lee y no se borra al apagar; la RAM se lee y escribe y (volátil) se borra.
@card ¿Qué plano es fijo en una PAL? || El plano OR.
@gloss ROM | Memoria de solo lectura: guarda una tabla fija.
@gloss RAM | Memoria de lectura y escritura, volátil.
@gloss PLA | Matriz lógica programable con plano AND y plano OR programables.
@gloss PAL | Matriz con plano AND programable y plano OR fijo.
@gloss Volátil | Que pierde su contenido al quitar la alimentación.

@q t7
¿Cuántas líneas de dirección tiene una memoria de 32K$\times$8?
+ 15
- 8
- 32
- 5
> $32\text{K}=2^{5}\cdot2^{10}=2^{15}$.
@end
@q t7
¿Cuántos chips de 4K$\times$4 hacen falta para una memoria de 8K$\times$8?
+ 4
- 2
- 8
- 16
> A lo ancho, $8/4=2$; a lo largo, $8\text{K}/4\text{K}=2$. Total $2\cdot2=4$.
@end
@q t7
Una ROM de 8 posiciones y 2 bits puede implementar:
+ Un sumador completo (3 entradas, 2 salidas)
- Un contador de 8 bits
- Un biestable
- Cualquier función de 4 entradas
> Tiene 3 líneas de dirección (entradas) y 2 bits de dato (salidas).
@end
