# 10 — Los productos finales (resumen ejecutivo)

**Fase 10 de 10 del proyecto HCI Ecuador — completada el 6 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Las nueve fases anteriores construyeron el índice HCI y todo su
análisis, pero vivían dentro de notebooks técnicos — útiles para
quien programa, no para quien necesita mirar un mapa o revisar el
perfil de un cantón en una reunión. Esta fase convierte todo ese
trabajo en los productos finales que el proyecto prometía desde su
diseño original: mapas, un tablero interactivo, perfiles y un reporte
ejecutivo.

## ¿Qué se hizo?

1. **Ocho mapas temáticos**, cada uno en dos versiones: estática (para
   imprimir o incluir en un informe) e interactiva (para explorar en
   el navegador, con zoom y detalle por cantón al pasar el cursor) —
   frecuencia de inundaciones, severidad, frecuencia en meses El Niño,
   población afectada, pérdidas agrícolas, pérdidas de vivienda,
   cronicidad HCI, y hotspots.

2. **Un workbook de Excel** con los rankings de cantones y provincias,
   tendencias mensuales y anuales, y un análisis por categoría de El
   Niño — todo en una sola tabla lista para revisar o filtrar.

3. **Un tablero interactivo**, en dos versiones: un archivo HTML
   autónomo que se abre con doble clic (sin necesitar internet ni
   instalar nada) con filtros por provincia, categoría de El Niño,
   año, mes y variable de impacto; y una versión dentro de Jupyter
   para quien quiera seguir ajustándolo con código.

4. **Perfiles individuales de las 24 provincias y los 221 cantones**
   (246 páginas en total) — cada uno con su puntaje HCI, sus 4
   componentes, su posición en el ranking nacional, y sus principales
   indicadores de impacto histórico.

5. **Un reporte ejecutivo nacional en Word** que resume todo el
   proyecto — antecedentes, metodología, hallazgos principales, mapas,
   recomendaciones y limitaciones — pensado para lectores que no
   necesitan entrar al detalle técnico.

## ¿Qué encontramos?

Esta fase no genera hallazgos nuevos — organiza y presenta los ya
documentados en las Fases 1 a 9. El reporte ejecutivo (sección
"Anexo — Entregables del Proyecto") reúne el listado completo de todo
lo producido, y su sección de hallazgos principales resume lo más
importante: Quito lidera el ranking nacional por persistencia y
frecuencia (no por gravedad de un evento puntual), su entorno
inmediato es la zona de mayor agrupamiento estadístico del país,
Tungurahua/Manabí/Pichincha encabezan el ranking provincial, y el
proyecto documentó de forma transparente la verificación y corrección
de un dato de origen (Baños de Agua Santa) antes de dar el índice por
definitivo.

## Un par de decisiones prácticas que vale la pena explicar

**El tablero HTML no se actualiza solo.** Es un archivo con los datos
ya incluidos, para que cualquiera pueda abrirlo sin depender de una
conexión o un servidor — pero eso significa que si el pipeline
produce datos nuevos en el futuro, hay que volver a generarlo (una
sola ejecución de un notebook), no se refresca automáticamente.

**El documento de perfiles cubre las 221 cantones, no solo los más
críticos.** Se decidió así explícitamente para que cualquier cantón
—tenga o no un historial relevante— tenga su propia página de
referencia, en vez de dejar fuera a la mayoría del país.

## ¿Cómo contribuye esto al objetivo final?

Con esta fase, el proyecto HCI Ecuador entrega su primer ciclo
completo: de una base de datos cruda de 69,718 reportes de desastre a
un conjunto de productos listos para apoyar decisiones de Acción
Anticipatoria — mapas para visualizar, un tablero para explorar,
perfiles para consultar un territorio específico, y un reporte para
compartir con quienes toman las decisiones.

## Una adición (18 de septiembre de 2026): Educación y Salud

El equipo preguntó si había centros de salud y educativos afectados en
la base que no estuvieran incluidos en el análisis. Se revisó
directamente: sí hay — 1,128 establecimientos educativos y 320 centros
de salud afectados en total (2015-2025, dentro del alcance de los 4
peligros del proyecto), además de 5 establecimientos educativos
destruidos. Ese dato ya se usaba matemáticamente (era parte del cálculo
de Severidad), pero nunca tuvo su propio mapa ni tabla, a diferencia de
Población, Vivienda y Agricultura. Se agregó como noveno y décimo mapa
del atlas rápido, una hoja nueva en el Excel, y un filtro nuevo en el
tablero interactivo. Falta que Jerson incorpore estos 2 mapas al atlas
profesional de ArcGIS Pro que está maquetando — los datos ya están
listos para eso.

## Otra adición (18 de septiembre de 2026): tablas master

El equipo pidió los indicadores y la susceptibilidad en tablas listas
para compartir, sin tener que entrar a los notebooks. Se entregaron 2
archivos Excel nuevos en `outputs/tables/`:

**`HCI_Ecuador_Tabla_Master_Indicadores.xlsx`** — los 4 sub-índices y
el HCI de los 221 cantones, en 5 hojas (Combinado, Inundación,
Aluvión, Deslizamiento, Socavamiento), cada una ordenada de mayor a
menor cronicidad, con su clase y su resultado de hotspot (Gi*). La
hoja Combinado incluye además los totales históricos por sector
(Población, Vivienda, Agricultura, Educación, Salud).

**`HCI_Ecuador_Tabla_Master_Susceptibilidad.xlsx`** — cada centro de
salud (2,094), centro educativo (15,665) y centro poblado (1,340) del
país, con su clasificación en las 3 capas oficiales de susceptibilidad
(Inundación / Movimientos en Masa / Deslizamientos) del geoproceso de
ArcGIS Pro — no el historial de desastres del HCI. Incluye una hoja
de resumen con los totales agregados. Dos limitaciones de origen
quedan documentadas en la propia hoja Léame del archivo: la tabla de
centros educativos no trae coordenadas utilizables, y la de centros
poblados no trae provincia/cantón (ninguna de las dos capas se unió en
el geoproceso original).

## ¿Qué falta?

- Validación externa del HCI contra fuentes internacionales de
  desastres (UNOSAT, EM-DAT, DesInventar, Copernicus EMS) antes de
  considerarlo apto para uso operativo pleno.
- El componente predictivo (modelos que estimen el impacto esperado
  ante un nuevo evento El Niño) sigue siendo una fase futura, no
  desarrollada en esta entrega.
- Incorporar capas físicas adicionales (lluvia, extensión de
  inundación satelital, elevación del terreno) si se decide ampliar el
  proyecto.
- Replicar la metodología en otros países o para otros peligros,
  consistente con la visión de largo plazo del proyecto.
