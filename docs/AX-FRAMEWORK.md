# AX — Agent Experience
## Diseño de experiencias agénticas

**AX (Agent Experience)** es la disciplina que diseña cómo las personas expresan objetivos, colaboran con agentes, delegan tareas, supervisan su ejecución y alcanzan resultados.

AX amplía el foco tradicional de UX/UI. No se limita a diseñar pantallas, controles o conversaciones: diseña la experiencia de trabajo completa entre personas y sistemas agénticos, desde la intención inicial hasta la validación y el cierre. AX no elimina UX/UI; los integra dentro de un sistema en el que agentes pueden planificar, utilizar capacidades, delegar, ejecutar y solicitar intervención humana.

## Los cuatro componentes

### 1. Workflow Experience
Diseña el recorrido del trabajo desde el objetivo hasta el resultado:
- Capturar objetivo, contexto, restricciones y criterios de éxito.
- Convertir objetivos en etapas, tareas y entregables verificables.
- Mantener visible el estado y el siguiente paso útil.
- Adaptar el flujo ante hallazgos, bloqueos o cambios de alcance.
- Definir validación, aceptación y cierre.

Pregunta: **¿Cómo fluye el trabajo hasta alcanzar el resultado?**

### 2. Agent Behavior & Orchestration
Diseña el comportamiento y la coordinación de capacidades:
- Decidir cuándo preguntar, investigar, razonar, ejecutar, delegar o detenerse.
- Seleccionar Skills, herramientas, modelos y runtimes disponibles.
- Descomponer tareas y asignar responsabilidades.
- Gestionar dependencias, errores, reintentos y escalamiento.
- Mantener trazabilidad y no afirmar ejecuciones que no ocurrieron.

Pregunta: **¿Qué debe hacer el agente, en qué orden, con qué capacidades y bajo qué condiciones?**

### 3. Conversational & Multimodal Interface
Diseña cómo las personas y los agentes intercambian y representan información:
- Chat, voz, imágenes, documentos y otros medios.
- Tarjetas de tareas, resúmenes, tablas, gráficos y visualizaciones.
- Controles para revisar, corregir, aprobar o rechazar.
- Progreso, historial, fuentes, resultados y errores.

La interfaz debe responder a la actividad. No todo requiere un formulario o dashboard: la conversación puede ser la interfaz principal, complementada con visualizaciones y controles cuando aporten valor.

Pregunta: **¿Cómo entiende la persona qué está pasando y cómo puede intervenir?**

### 4. Human–Agent Coordination
Diseña delegación, supervisión y control:
- Definir permisos, límites de autonomía y niveles de aprobación.
- Determinar qué ejecuta el agente y qué requiere autorización.
- Facilitar intervención, corrección, pausa, cancelación y recuperación.
- Exponer evidencia, fuentes, supuestos y acciones realizadas.
- Mantener responsabilidad humana en decisiones de alto impacto.

Pregunta: **¿Quién decide, quién ejecuta, quién supervisa y cómo se recupera el control?**

## AX como sistema integrado

Los cuatro componentes no son etapas estrictamente lineales. Se influyen durante todo el trabajo: el workflow cambia por hallazgos; el comportamiento puede requerir aprobación; la interfaz hace visible esa necesidad; la coordinación humana puede modificar permisos, prioridades o alcance.

AX diseña el sistema completo y sus transiciones.

## Relación con Agent Skills Factory

- **AX** diseña la experiencia de trabajo persona–agente.
- **Agent Skills Factory** crea, valida, versiona y distribuye capacidades especializadas.
- **El agente/orquestador** planifica, razona y selecciona capacidades.
- **El runtime** ejecuta código y procesos.
- **Los conectores/proveedores** aportan datos y servicios externos.
- **La interfaz anfitriona** presenta la interacción y los resultados.

Una Skill no es el workflow AX completo, ni la interfaz, ni el orquestador, ni el runtime. Es una capacidad especializada invocable dentro de un workflow y reutilizable por distintos agentes.

Una Skill debe declarar qué hace, cuándo se usa, qué entradas necesita, qué metodología sigue, qué recursos o dependencias son opcionales/obligatorios para ciertas operaciones, qué produce, cómo verifica el resultado y cómo se degrada cuando faltan capacidades.

## Ejemplo: análisis institucional de una acción

1. **Workflow Experience:** la persona solicita analizar una acción; se identifican emisor, horizonte, moneda, datos, análisis, valoración y entregables.
2. **Agent Behavior & Orchestration:** el agente invoca la Skill de equity research, selecciona fuentes autorizadas, ejecuta cálculos en el sandbox disponible y delega si hace falta.
3. **Conversational & Multimodal Interface:** la persona ve preguntas, avance, tablas, gráficos, supuestos, fuentes y archivos.
4. **Human–Agent Coordination:** la persona define alcance, autoriza conexiones o acciones externas, revisa supuestos y acepta o corrige el informe.

La Skill aporta metodología financiera y rutinas especializadas; no asume el control de los cuatro componentes.

## Principios AX

1. Outcome-first: diseñar alrededor del resultado, no de la pantalla o el prompt.
2. Workflow continuity: mantener contexto, estado y siguiente paso entre interacciones.
3. Progressive autonomy: ajustar autonomía al riesgo, permisos y confianza.
4. Explicit handoffs: hacer visibles delegaciones y transferencias.
5. Evidence and provenance: permitir inspeccionar fuentes, supuestos, acciones y resultados.
6. Graceful recovery: gestionar errores, bloqueos y cambios de alcance.
7. Human agency: conservar capacidad real de decisión e intervención.
8. Interface proportionality: usar la representación más simple que permita comprender y controlar el trabajo.
9. Capability honesty: no afirmar que se ejecutó código, consulta o acción que no ocurrió.
10. Measurable completion: definir criterios observables de finalización.

## Métricas AX

Medir, según tipo de tarea y riesgo:
- Tiempo desde intención hasta resultado aceptado.
- Porcentaje de workflows completados correctamente.
- Reformulaciones, repeticiones y reintentos.
- Número y calidad de intervenciones humanas.
- Errores y tasa de recuperación.
- Resultados con evidencia y trazabilidad suficientes.
- Acciones no autorizadas (objetivo: cero).
- Claridad sobre estado, responsabilidades y siguiente paso.
- Reutilización efectiva de Skills.
- Calidad y aceptación del resultado.

Optimizar velocidad a costa de calidad, seguridad o control humano no constituye una buena experiencia agéntica.
