%% id=p4
%% group=prac
%% n=4
%% title=Práctica 4 · Desarrollo de sistemas digitales mediante VHDL
%% short=P4 · VHDL (con IA)
%% sub=Un sistema completo en VHDL: se permite usar IA, pero hay que entender, revisar y justificar el código.
%% kicker=Prácticas (20 % de la nota)

@box ojo | Sobre el uso de IA
Se permite usar IA como apoyo, pero el código debe ser **comprendido, revisado y justificado por ti**. En la defensa pueden pedirte que expliques una línea, que encuentres un error o que lo modifiques. La forma segura de prepararte: pide el código, **simúlalo**, tradúcelo a un diagrama y **busca los fallos típicos** (latches, reset, reloj dividido, señales no asignadas).
@end

## Objetivo

Construir un sistema completo combinando bloques: el ejemplo de la guía muestra cuatro cifras en el display multiplexado de la Basys.

@fig blocks {"blocks": {"cnt": [20, 80, 120, 70, "Contador\nde 18 bits"], "mux": [190, 20, 120, 70, "MUX 4:1\ncifras BCD"], "d7": [350, 20, 120, 70, "Decodificador\n7 segmentos"], "an": [190, 140, 120, 60, "Decodificador\n2→4 (ánodos)"]}, "arrows": [[140, 100, 190, 55, "sel"], [140, 130, 190, 170, "sel"], [310, 55, 350, 55, "cifra"], [470, 55, 570, 55, "segmentos"], [310, 170, 430, 170, "ánodos"]], "W": 580, "H": 215, "title": "Display de 4 dígitos multiplexado", "cap": "El contador de refresco elige a la vez la cifra y el dígito que se enciende."}

@ej p4-s1|Display de 4 dígitos multiplexado|Práctica 4|vhdl,msi|t12.refresco,t12.disp
@enun
Muestra cuatro cifras BCD en el display de 4 dígitos de la Basys. Calcula la frecuencia de refresco.
@end
@antes
Teoría: multiplexación en el tiempo, contador de refresco, decodificador de 7 segmentos activo a nivel bajo, múltiples dígitos con ánodo común.
@end
@paso Idea
Los 4 dígitos comparten los 7 segmentos. Solo uno está activo cada vez. Se alternan tan rápido que el ojo los ve todos encendidos.
@end
@paso Contador de refresco
Un contador libre de 18 bits. Sus dos bits altos eligen el dígito: cada dígito dura $2^{16}$ ciclos.
@end
@paso Selección
Un `with sel select` elige la cifra y activa el ánodo correspondiente (activo a 0).
@end
@paso Frecuencias
Cambio de dígito: $50\,\text{MHz}/2^{16}=762{,}9$ Hz. Refresco de cada dígito: $762{,}9/4=190{,}7$ Hz.
@end
@res
Cuatro cifras estables, sin parpadeo visible, con refresco de $190{,}7$ Hz por dígito.
@end
@end

@codefile vhdl|p4_display4.vhd|vhdl/p4_display4.vhd

@codefile text|Resultado del modelo Python|salidas/p4.txt

## Qué escribir en la memoria

- Las prompts que usaste y qué cambiaste del código generado, y por qué.
- Un diagrama de bloques jerárquico del sistema.
- Los cálculos de frecuencias y tiempos.
- Una lista de **tres errores** que detectaste al revisar el código.
