# Distribución de las Skills de Frontera Funds

## Regla de responsabilidad

- **Agent Skills Factory** es el catálogo y el canal de distribución de capacidades portables, incluyendo Skills no relacionadas con Frontera.
- **frontera-funds-intelligence-skills** es el repositorio canónico de desarrollo del motor de informes, su código TypeScript, Frontera Score, plantillas y pruebas.
- `skills/fic-funds-intelligence` en Factory es una **distribución versionada**; sus plantillas históricas no se consideran fuente de verdad para nuevas implementaciones.
- La publicación debe proceder de un paquete reproducible y un commit etiquetado en el repositorio especializado. No mantener forks manuales de métricas ni renderizadores en Factory.

## Perfiles oficiales de comparación

Dos ejemplos HTML suministrados como referencias de aceptación:
- `analitico_completo`: Frontera Funds Factsheet (comparativo extendido, A4 vertical), SHA-256 `d969138f6774a0b2b8e2d3c30b9b84de23907720b24d5ffcacb8032d9972330e`.
- `tabla_ejecutiva`: comparativo ejecutivo, A4 horizontal, SHA-256 `79fd527d57fd135c90b3a4b4ad3f70bfe117c9b305fc2691bb75b3145aee4d2e`.

Estos dos reportes no equivalen a “ficha individual + comparativo”: ambos comparan fondos. La ficha individual sigue siendo otra capacidad.

## Estado y compuerta de publicación

Las plantillas locales de la Skill Factory y el renderizador de Frontera Funds son diferentes en estructura. **No afirmar todavía paridad exacta** con los HTML de referencia.

Antes de publicar una versión nueva se exige:
1. incorporar los originales inalterados con comprobación SHA-256;
2. fijar los fixtures y criterios de aceptación financieros y visuales;
3. aprobar pruebas automáticas de perfiles `analitico_completo` y `tabla_ejecutiva`;
4. adjuntar versión del renderizador y commit de procedencia al paquete;
5. probar en los runtimes/modelos declarados compatibles.

Si el usuario no da período, solicitarlo antes de ejecutar. No imponer un rango predeterminado de un año.

Información general: https://github.com/jairoalonso1/frontera-funds-intelligence-skills
