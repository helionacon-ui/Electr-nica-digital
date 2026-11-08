%% id=p567
%% group=prac
%% n=5
%% title=Prácticas 5 a 7 · Proyecto integrador
%% short=P5–P7 · Proyecto integrador
%% sub=Especificación, implementación e integración de un sistema distribuido que monitoriza una incubadora neonatal.
%% kicker=Prácticas (20 % de la nota)

## En qué consisten

Es un **proyecto colaborativo** basado en la monitorización de una incubadora neonatal (Dräger Caleo) usada como **entorno de simulación**.

| Práctica | Qué se hace |
|---|---|
| **P5** | Especificación y diseño del proyecto integrador |
| **P6** | Cada grupo implementa y depura el **módulo asignado** del sistema distribuido, con pruebas individuales y documentación técnica |
| **P7** | Integración de todos los módulos, validación y **defensa pública** de la solución |

@box ojo | Qué no sé de tu proyecto
El programa solo describe el proyecto en general. El módulo concreto que te asignen y los datos exactos de la incubadora se fijan en el curso. El ejemplo de abajo (una alarma de temperatura con histéresis) **no es tu módulo asignado**: está para mostrar cómo se diseña, se prueba y se documenta un módulo típico de un sistema de monitorización.
@end

## Método para cada módulo

1. **Especifica** entradas, salidas, rangos y qué debe hacer, con una tabla.
2. **Diseña** en bloques: qué es combinacional, qué es secuencial.
3. **Escribe** el código (VHDL) y **simula** con casos límite.
4. **Prueba** el módulo aislado en la placa.
5. **Documenta**: interfaz, funcionamiento, pruebas y resultados.
6. **Integra**: conecta con los demás módulos y comprueba temporización y niveles.

## Ejemplo: alarma de temperatura con histéresis

Un sensor da la temperatura en décimas de grado. Se quiere una alarma de alta ($\ge37{,}5\ ^\circ$C) y una de baja ($<36{,}0\ ^\circ$C). Sin histéresis, una medida que oscile alrededor del umbral haría **parpadear** la alarma. Con histéresis, la alarma se **desactiva** solo cuando la medida baja del umbral menos un margen (0,5 °C).

@ej p567-s1|Alarma con histéresis|Prácticas 5-7|vhdl,sec|
@enun
Diseña un módulo `p6_alarma` que reciba `temp` (10 bits, décimas de grado) y active `al_alta` si $T\ge375$ y `al_baja` si $T<360$, con histéresis de 5 décimas.
@end
@antes
Teoría: comparadores ([[t05|T5]]), biestable que recuerda el estado de la alarma ([[t06|T6]]), proceso síncrono ([[t13|T13]]).
@end
@paso Qué hay que recordar
La alarma depende del **pasado** (si ya estaba activa o no) y no solo de la entrada: es un circuito **secuencial** con un biestable por alarma.
@end
@paso Reglas
Alta: se activa con $T\ge T_{ALTA}$ y se desactiva con $T<T_{ALTA}-H$. Baja: se activa con $T<T_{BAJA}$ y se desactiva con $T\ge T_{BAJA}+H$. Entre ambos valores **mantiene** el estado.
@end
@paso Código
Ver abajo.
@end
@paso Casos límite que hay que probar
$T=374$ (no activa), $375$ (activa), $373$ (sigue activa por la histéresis), $369$ (se desactiva), y los equivalentes para la baja.
@end
@res
Para las medidas $365,370,374,375,376,373,371,369,\dots$ la alarma de alta se activa en $375$ y se desactiva en $369$.
@end
@end

@codefile vhdl|p6_alarma_incubadora.vhd|vhdl/p6_alarma_incubadora.vhd|alarma

@codefile text|Resultado del modelo Python|salidas/p6.txt

## Qué debe contener la documentación y la defensa

- Una **tabla de interfaz** (señales, ancho, sentido, significado).
- Un **diagrama de bloques** del módulo y de cómo encaja en el sistema.
- La **estrategia de pruebas** (casos normales y límite) y los resultados.
- La **justificación** de cada decisión de diseño (por qué histéresis, por qué ese ancho de bits).
- Si usaste IA: qué pediste, qué cambiaste y cómo comprobaste que es correcto.

@box falla | Qué suele fallar
- Integrar sin haber probado cada módulo por separado.
- Interfaces mal acordadas (anchos, polaridad activo-alto/bajo, qué unidad lleva cada dato).
- No documentar las suposiciones.
- Defender código que no entiendes.
@end
