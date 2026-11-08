%% id=formulario1p
%% group=ref
%% n=1.5
%% title=Formulario de una página
%% short=Formulario de 1 página
%% sub=Todo lo esencial en una hoja: numeración, Boole, bloques, biestables, contadores, autómatas y VHDL.

| Tema | Lo imprescindible |
|---|---|
| **T2 Numeración** | $n=\lceil\log_2N\rceil$ bits. C2 de $n$ bits: $-2^{n-1}\dots2^{n-1}-1$; $-N=\overline{N}+1$. Desbordamiento: acarreo que entra al signo $\ne$ acarreo que sale. Gray: $g=b\oplus(b\gg1)$. BCD: cifra $>9$ suma $0110$. |
| **T3 Boole** | $\overline{A+B}=\overline{A}\,\overline{B}$; $\overline{AB}=\overline{A}+\overline{B}$. $A+AB=A$; $AB+A\overline{B}=A$; $AB+\overline{A}C+BC=AB+\overline{A}C$. $A\oplus B=A\overline{B}+\overline{A}B$. Karnaugh: grupos de $2^k$ unos adyacentes (también en los bordes); las X solo se usan si ayudan. NAND-NAND = suma de productos. |
| **T4 Familias** | $NM_H=V_{OH}-V_{IH}$; $NM_L=V_{IL}-V_{OL}$. Fan-out $=\min(I_{OL}/I_{IL},\,I_{OH}/I_{IH})$. $P_{din}=CV_{DD}^2f$. |
| **T5 Combinacional** | Sumador completo: $S=A\oplus B\oplus C_{in}$; $C_{out}=AB+C_{in}(A\oplus B)$. $A-B=A+\overline{B}+1$. MUX $2^k{:}1$ implementa funciones de $k+1$ variables. Decodificador: salida $i=m_i$. |
| **T6 Biestables** | $Q^+_{JK}=J\overline{Q}+\overline{K}Q$; $Q^+_D=D$; $Q^+_T=T\oplus Q$. Excitación JK: $0\to0$: $J=0,K=X$; $0\to1$: $J=1,K=X$; $1\to0$: $J=X,K=1$; $1\to1$: $J=X,K=0$. $T_{clk}\ge t_{cq}+t_{pd}+t_{su}$. |
| **T7 Memorias** | bits $=2^k\cdot m$. Chips $=\frac{N}{N_c}\cdot\frac{m}{m_c}$. ROM $2^n\times m$ = $m$ funciones de $n$ variables. |
| **T8 Contadores** | $n=\lceil\log_2N\rceil$; $f_{out}=f_{clk}/N$. Síncrono binario: $T_i=Q_{i-1}\cdots Q_0$. Asíncrono: $t=n\,t_{pd}$. Estados no usados: $2^n-N$ (¡cuidado con el bloqueo!). |
| **T9 Registros** | Anillo: $n$ estados. Johnson: $2n$. LFSR máximo: $2^n-1$. Serie a paralelo de $n$ bits: $n$ ciclos. |
| **T10 Autómatas** | Estados $\to$ $n=\lceil\log_2(\#)\rceil$ biestables. Moore: $Z=f(Q)$. Mealy: $Z=f(Q,X)$. D: $D=Q^+$. T: $T=Q\oplus Q^+$. Detector con solapamiento: el estado es el mayor prefijo que es sufijo. |
| **T12–T13 FPGA y VHDL** | LUT de $k$ entradas: $2^k$ bits. Divisor: $DIV=f_{in}/f_{out}$; conmuta cada $DIV/2$ ciclos. `case` completo: `when others`. Lo concurrente (fuera de `process`) ocurre a la vez. |
