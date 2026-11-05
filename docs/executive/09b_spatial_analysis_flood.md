# 09b — Análisis espacial de inundación, por separado (resumen ejecutivo)

**Primera de 4 versiones independientes por tipo de amenaza — completada el 17 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Hasta ahora, el análisis de agrupamientos geográficos (Fase 9) mezclaba los 4 tipos de amenaza del proyecto (inundación, deslizamiento, socavamiento, aluvión) en un solo resultado, aunque se podía filtrar por columna. Jerson pidió separarlos completamente: un análisis propio, independiente, para cada tipo de amenaza — empezando por inundación, para poder revisar el resultado antes de replicarlo a los otros tres.

## ¿Qué se hizo?

Se repitió exactamente el mismo método ya validado en agosto (contigüidad geográfica entre cantones vecinos, detección de puntos calientes/fríos, mapa de densidad, agregación en hexágonos), pero usando **solo** los eventos y el índice HCI calculados específicamente para inundación, no la mezcla de los 4 tipos.

Una decisión que se confirmó contigo antes de programar: 7 de los 221 cantones nunca tuvieron un evento de inundación registrado. Se decidió asignarles cronicidad de inundación = 0 (en vez de excluirlos del mapa) porque es la lectura correcta: esos cantones genuinamente no tienen historial de inundación, no es un dato que falte.

## ¿Qué encontramos?

**El patrón geográfico de inundación es visiblemente distinto al del análisis combinado que ya conocías.** El análisis combinado mostraba un arco de cronicidad alrededor de Quito y la sierra centro-norte (dominado por deslizamientos). El análisis específico de inundación muestra algo geográficamente muy coherente y distinto: **la costa** (Esmeraldas, Manabí, Guayas, Los Ríos) concentra los puntos calientes, y **el oriente amazónico** (Sucumbíos, Napo, Orellana, Pastaza) concentra los puntos fríos.

El ranking de cantones por cronicidad de inundación específicamente también cambia: **Chone (Manabí) pasa a ser el cantón con mayor cronicidad de inundación del país**, seguido de Quito, Guayaquil, Babahoyo y Santo Domingo — un ranking centrado en la costa y las cuencas bajas, muy distinto del ranking combinado (donde Quito lideraba).

Un hallazgo con matiz: aunque Quito tiene un HCI de inundación individualmente alto (2º lugar nacional), **no aparece como un "punto caliente" en el análisis de agrupamiento** — es decir, Quito es alto por sí mismo, pero sus vecinos no forman el mismo patrón consistente que sí se ve en la franja costera. Es información real sobre cómo se distribuye el riesgo, no un error.

## ¿Cómo contribuye esto al objetivo final?

Separar el análisis por tipo de amenaza responde directamente a lo que Jerson identificó como una limitación: mezclar inundación con deslizamientos, aunque ambos a veces sean causados por la misma lluvia, esconde patrones geográficos genuinamente distintos que requieren respuestas de Acción Anticipatoria distintas (protección de cuencas bajas costeras vs. estabilización de laderas andinas). Este primer resultado confirma que la separación vale la pena — el mapa de inundación por sí solo cuenta una historia mucho más clara y específica que la versión mezclada.

## ¿Qué falta?

- Tu revisión de este primer resultado (inundación) antes de replicar el mismo trabajo a deslizamiento, socavamiento y aluvión.
- Los mapas del índice HCI y de puntos calientes/fríos específicos de inundación ya están listos — ver `09b_spatial_analysis_flood.md` (versión técnica) y el atlas `Atlas_HCI_Ecuador_Flood.pdf`.
