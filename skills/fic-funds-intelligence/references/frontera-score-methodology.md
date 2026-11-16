# Frontera Score — metodología de referencia

**Versión del port MCP:** 1.0.0  
**Fuente de verdad:** repositorio `jairoalonso1/Frontera`, `components/FundAnalysisPage.tsx`, función de asignación de rating, líneas 1685–1743 de la revisión consultada.  
**Alcance:** adaptación independiente en el MCP. No se modifica Frontera SaaS.

## Ponderaciones

| Métrica | Peso | Dirección |
|---|---:|---|
| CAGR | 35 % | Mayor es mejor |
| Sharpe Ratio | 25 % | Mayor es mejor |
| Sortino Ratio | 10 % | Mayor es mejor |
| Maximum Drawdown | 15 % | Mayor (menos negativo) es mejor |
| Recovery Factor | 10 % | Mayor es mejor |
| Volatilidad | 5 % | Menor es mejor |

## Algoritmo reproducido

1. Se consideran elegibles los elementos con métricas no vacías y sin error.
2. Para cada métrica se construye una lista de valores numéricos finitos, sin duplicados.
3. Se ordena esa lista según la dirección de preferencia. Los valores iguales comparten rango.
4. La contribución de cada métrica es `(rango + 1) × peso`.
5. Si el fondo no tiene un valor numérico finito para una métrica, recibe una penalización de `número de elegibles × peso`.
6. Se ordenan los puntajes de menor a mayor. El ordenamiento estable conserva el orden de entrada en caso de empate de puntaje compuesto.
7. Se asignan estrellas mediante quintiles fraccionarios: inicialmente 5; desde los límites de 1, 2, 3 y 4 quintiles se asignan 4, 3, 2 y 1 estrellas, respectivamente.
8. Un único fondo elegible recibe puntaje 0 y tres estrellas. Sin fondos elegibles, el resultado es vacío.

## Advertencias de equivalencia

- La metodología es relativa al conjunto de fondos comparados, no a una categoría de referencia.
- La asignación por índice puede separar en estrellas distintas a fondos con puntaje idéntico si quedan a lados distintos de un límite de quintil. No se corrige en este port.
- Para grupos pequeños, los límites fraccionarios pueden generar saltos (por ejemplo, tres fondos pueden recibir 5, 4 y 2 estrellas).
- Los valores infinitos y no numéricos se tratan como faltantes, incluyendo `Infinity` en Recovery Factor. Esto reproduce la comprobación `isFinite` del código SaaS.
- El motor de score no calcula métricas: recibe las seis métricas ya calculadas. La equivalencia integral depende de que el MCP calcule cada métrica con las mismas convenciones, ventana temporal, periodicidad y tasa libre de riesgo que la SaaS.

## Estado de integración

El módulo está integrado en la rama de trabajo del MCP. El generador de ficha individual ya consume el motor de métricas; el comparativo Peer Group todavía debe integrar el score y sus gráficas. La equivalencia de las métricas calculadas frente a SaaS sigue pendiente de validación con casos reales y ventanas idénticas.
