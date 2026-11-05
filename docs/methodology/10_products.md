# 10 — Productos (Mapas, Salidas Estadísticas, Dashboard, Perfiles, Reporte)

**Fase:** 10 de 10 (ver Fase 0, §9, §14)
**Notebooks asociados:** `notebooks/Step10a` a `Step10f_*.ipynb`
**Estado:** implementado y ejecutado — 2026-08-06
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de la fase

Transformar las salidas analíticas de las Fases 1-9 (índices,
hotspots, tablas) en los productos finales orientados a decisión que
el diseño original (Fase 0 §9, §14) especifica: mapas, salidas
estadísticas, un dashboard interactivo, perfiles por unidad
administrativa, y un reporte ejecutivo nacional. Esta fase no calcula
ningún indicador nuevo — es la fase de "empaquetado" de todo lo
construido hasta ahora.

## 2. Alcance confirmado por Jerson (AskUserQuestion, 2026-08-06)

Cuatro decisiones de alcance, todas con implicaciones directas de
volumen de trabajo:

1. **Mapas:** ambos formatos — atlas estático (PNG/PDF) e interactivo
   (HTML) — no solo uno.
2. **Dashboard:** ambas versiones — HTML autónomo (para compartir) y
   notebook Jupyter/`ipywidgets` (para editar) — "para después editar
   de ser necesario".
3. **Perfiles:** cobertura completa — 24 provincias + 221 cantones
   (245 páginas), no solo una muestra de los más crónicos.
4. **Reporte final:** solo Word (no PDF adicional en esta entrega).

## 3. Sub-fases y notebooks

| Notebook | Contenido | Salida principal |
|---|---|---|
| `Step10a_Ecuador_Static_Maps.ipynb` | Dataset maestro cantonal + 8 mapas estáticos + atlas PDF | `outputs/maps/*.png`, `outputs/reports/Atlas_EFCI_Ecuador.pdf` |
| `Step10b_Ecuador_Interactive_Maps.ipynb` | 8 mapas interactivos (Leaflet/folium) | `outputs/maps/interactivos/*.html` |
| `Step10c_Ecuador_Statistical_Outputs.ipynb` | Rankings, tendencias mensual/anual, análisis ENSO | `outputs/tables/EFCI_Ecuador_Estadisticas.xlsx` |
| `Step10d_Ecuador_Dashboard_HTML.ipynb` | Dashboard HTML autónomo con datos embebidos | `outputs/dashboard/EFCI_Ecuador_Dashboard.html` |
| `Step10e_Ecuador_Dashboard_Interactive.ipynb` | Dashboard editable (ipywidgets) | (uso interactivo dentro de Jupyter, no exporta archivo) |
| `Step10f_Ecuador_Profiles.ipynb` | Perfiles de 24 provincias + 221 cantones | `outputs/reports/Perfiles_EFCI_Ecuador.pdf` (246 páginas) |
| `build_report_final.js` (Node.js/docx-js, fuera del árbol `notebooks/` por ser JS, no Python) | Reporte ejecutivo nacional | `outputs/reports/EFCI_Ecuador_Reporte_Ejecutivo.docx` |

## 4. Decisiones metodológicas y su justificación

### 4.1 Dataset maestro cantonal (`mapa_master_canton.gpkg`)

Construido una sola vez en Step10a y reutilizado por Step10b, d, e, f
— evita recalcular la misma unión de tablas 5 veces. Combina, por
`canton_code`: los 4 sub-índices + EFCI (Fase 8), frecuencia de
inundaciones y años afectados (Fase 3), frecuencia de eventos en
meses "El Niño" (mismo criterio de Fase 5 §4.3), clasificación de
hotspot Gi* (Fase 9), y máximos históricos de población/agricultura/
vivienda recalculados directamente de `hazard_event_geo` (misma
filosofía de "peor escenario" que Severidad, Fase 4 §4.1 — no se
reutiliza `hist_impactos_canton` porque viene en formato largo,
una variable a la vez, y aquí se necesitan combinadas).

### 4.2 Nivel de agregación: cantón, no provincia, para los mapas

Los 8 mapas (estáticos e interactivos) se generan a nivel cantón
(221 unidades) — el nivel más detallado disponible en el proyecto
desde la Fase 2, consistente con los rankings y perfiles del resto de
la fase. No se generó un segundo set de mapas a nivel provincia
(los rankings estadísticos sí cubren ambos niveles, ver §4.3).

### 4.3 Clasificación de mapas: Jenks para las 6 variables continuas + reutilización de clases ya fijadas para EFCI y Hotspots

Los 6 mapas de variables continuas (frecuencia, severidad, frecuencia
ENSO, población, agricultura, vivienda) se clasifican con quiebres
naturales (Jenks, 5 clases) — misma convención que el resto del
proyecto desde la Fase 8. Los mapas de EFCI y de Hotspots **no
recalculan clases**: reutilizan las ya fijadas en Fase 8
(`clase_efci`, 5 categorías Jenks) y Fase 9 (`gi_clase_efci`, 7
niveles de significancia) — evita que el mismo cantón aparezca en una
clase distinta en el mapa de esta fase que en la tabla de la fase que
lo originó.

### 4.4 Dashboard HTML: datos embebidos, sin servidor

El dashboard (`Step10d`) es un único archivo HTML con los datos ya
incrustados como JSON (geometría de cantones simplificada + eventos
agregados por año/mes/provincia/cantón/categoría ICEN/tipo de
peligro) — no se conecta a ninguna base de datos ni requiere un
servidor corriendo. El filtrado (Provincia, Categoría ENSO, Año, Mes,
Variable de Impacto) ocurre enteramente en JavaScript, del lado del
navegador. **Límite documentado, no oculto:** el archivo no se
actualiza solo si el pipeline produce datos nuevos — hay que
regenerarlo ejecutando `Step10d` de nuevo.

Para reducir el tamaño del archivo (los eventos agregados y la
geometría completos pesarían decenas de MB), se aplicaron dos
optimizaciones: (a) la geometría de los cantones se simplifica con
tolerancia 0.002° (~200 m, imperceptible a escala nacional); (b) los
21,743 eventos individuales se agregan por (año, mes, provincia,
cantón, categoría ICEN, tipo de peligro) antes de exportar — el
dashboard nunca necesita el detalle evento-por-evento, solo sumas
agregadas por esas 6 dimensiones. Resultado: ~4.5 MB, manejable para
un archivo que se abre con doble clic.

### 4.5 Segunda versión del dashboard: ipywidgets, no una segunda página HTML

Jerson pidió explícitamente "ambos, para después editar de ser
necesario" — interpretado como: una versión compartible sin
dependencias (HTML, Step10d) y una versión que él mismo pueda seguir
editando con código Python normal (notebook con `ipywidgets`,
Step10e), no dos archivos HTML redundantes. La versión Jupyter
reutiliza los mismos datos fuente (no el JSON embebido del HTML) para
que cualquier edición futura opere sobre datos "vivos" del pipeline,
no sobre una copia congelada.

### 4.6 Perfiles: agrupados por provincia, no en dos bloques separados

El PDF de 246 páginas (portada + 24 + 221) agrupa cada provincia
inmediatamente seguida de sus cantones — no "24 provincias, luego 221
cantones sin agrupar" — para que un lector que busca una provincia
específica encuentre también sus cantones sin tener que saltar a otra
sección del documento.

### 4.7 Reporte ejecutivo: generado con `docx-js` (Node.js), no python-docx

Se usó la librería `docx` de Node.js (siguiendo la guía de creación de
documentos Word del proyecto) para tener control fino de estilos
(fuente Arial en todo el documento, tabla de página con encabezado/pie,
numeración de página) y para insertar directamente las imágenes PNG de
los mapas ya generados en Step10a — evita mantener dos toolchains de
generación de Word distintas. **Verificado renderizando el `.docx` a
PDF e inspeccionando cada página como imagen** (protocolo estándar del
proyecto para verificar documentos Word) antes de darlo por
completo — 9 páginas, sin errores de formato ni de datos.

## 5. Validaciones aplicadas

- Atlas estático: 8 PNG + 1 PDF de 9 páginas (portada + 8 mapas).
- Mapas interactivos: 8 archivos HTML, todos >1 KB (no vacíos/corruptos).
- Workbook de estadísticas: 6 hojas, ranking de cantones con 221 filas
  (verificado único por (Provincia, Cantón), no por nombre de cantón
  solo — hay nombres de cantón repetidos entre provincias, p. ej.
  "Bolívar" existe como cantón en Carchi y en Manabí), ranking de
  provincias con 24 filas únicas, suma de la tendencia anual = 21,743
  eventos (coincide exactamente con el total del proyecto).
- Dashboard HTML: >1 MB, sin placeholders sin reemplazar, contiene las
  librerías Leaflet y Plotly.
- Perfiles: exactamente 246 páginas (1 portada + 24 + 221).
- Reporte ejecutivo: renderizado a PDF y cada página inspeccionada
  visualmente antes de dar la fase por completa.

## 6. Esquema de salida (resumen — detalle en cada notebook)

- `outputs/maps/*.png` (8) + `outputs/maps/interactivos/*.html` (8)
- `outputs/reports/Atlas_EFCI_Ecuador.pdf` (9 páginas)
- `outputs/tables/EFCI_Ecuador_Estadisticas.xlsx` (6 hojas)
- `outputs/dashboard/EFCI_Ecuador_Dashboard.html`
- `outputs/reports/Perfiles_EFCI_Ecuador.pdf` (246 páginas)
- `outputs/reports/EFCI_Ecuador_Reporte_Ejecutivo.docx`
- `data/processed/mapa_master_canton.{gpkg,csv}` (insumo intermedio reutilizado por toda la fase)

## 7. Limitaciones

- El dashboard HTML es estático (§4.4) — no refleja datos nuevos sin
  regenerarse.
- Los mapas y el dashboard trabajan a nivel cantón únicamente — no se
  generó una versión a nivel provincia de los mismos productos
  visuales (aunque las tablas estadísticas sí cubren ambos niveles).
- El reporte ejecutivo se entregó solo en Word, por decisión explícita
  de Jerson — no hay versión PDF adicional en esta entrega (se puede
  generar bajo demanda exportando el .docx).
- Los perfiles (Step10f) no incluyen mapas individuales por unidad —
  solo indicadores tabulares y 2 gráficos pequeños por página, para
  mantener el documento de 246 páginas en un tamaño manejable.

## 8. Supuestos

- Se asume que un archivo HTML con datos embebidos (sin backend) es
  una solución operativamente suficiente para uso de escritorio —
  válido para el caso de uso actual (revisión periódica, no
  monitoreo en tiempo real), documentado explícitamente como límite
  en §4.4 y §7.

## 9. Ventajas del enfoque

- Todos los productos de esta fase son regenerables desde cero
  ejecutando los notebooks en orden — no hay ningún archivo editado
  manualmente fuera del pipeline.
- El dataset maestro cantonal (§4.1) evita 5 recálculos redundantes de
  la misma unión de tablas, reduciendo el riesgo de que dos productos
  (p. ej. un mapa y el dashboard) muestren números ligeramente
  distintos por usar rutas de cálculo diferentes.
- El reporte ejecutivo se verificó visualmente antes de entregarse
  (§4.7), no solo por generarse sin errores de código.

## 10. Posibles mejoras futuras

- Publicar el dashboard HTML en un hosting estático simple (GitHub
  Pages, Netlify) para que no dependa de compartir el archivo
  manualmente.
- Añadir un mapa pequeño a cada página de perfil (Step10f) si el
  tamaño de archivo resultante (246 mapas adicionales) se considera
  aceptable.
- Automatizar la regeneración completa de la Fase 10 como un único
  script/Makefile que ejecute Step10a-f en secuencia.
- Explorar una versión PDF del reporte ejecutivo, si en el futuro se
  requiere una versión no editable para distribución externa.

## 11. Adición 2026-09-18 — Educación y Salud, confirmadas en la base y añadidas como productos propios

**Origen:** el equipo señaló preocupación por si había centros de salud y
educativos afectados en la base que no estuvieran en el análisis. Se
verificó directamente contra `hazard_event.csv` (21,743 eventos, alcance
de los 4 peligros del proyecto): sí existen — 715 eventos con
establecimientos educativos afectados (1,128 acumulados, 5 destruidos) y
231 eventos con centros de salud afectados (320 acumulados, 0 destruidos).
Estos datos **ya alimentaban** el pilar "Infraestructura" del Índice de
Severidad (Fase 4, 10% del peso, escuelas+salud combinados en un solo
puntaje), pero no tenían ningún producto propio — a diferencia de
Población, Vivienda y Agricultura, que sí tienen mapa individual.

**Se añadió:**

- `mapa_master_canton.gpkg/csv`: 2 columnas nuevas, `educacion_total` y
  `salud_total` (máximo histórico por cantón, `afectados + destruidos`,
  misma convención que `poblacion_total`/`agricultura_total`/`vivienda_total`
  ya existentes — ver Step10a_Ecuador_Static_Maps.ipynb, celda 4).
- Atlas estático (Step10a): 2 mapas nuevos (`09_educacion_afectada.png`,
  `10_salud_afectada.png`) — el atlas PDF pasa de 8 a 10 mapas (11 páginas
  con portada).
- `EFCI_Ecuador_Estadisticas.xlsx`: nueva hoja `Infraestructura_Social`
  (ranking de 221 cantones + resumen nacional).
- Dashboard interactivo: 4 variables nuevas en el filtro "Variable de
  Impacto" (`schools_affected`, `schools_destroyed`,
  `health_facilities_affected`, `health_facilities_destroyed`),
  recalculadas con la misma agregación (año/mes/provincia/cantón/ICEN/
  peligro) que las 9 variables ya existentes.

**Pendiente, fuera de mi alcance — para Jerson:** los 2 mapas nuevos
todavía no existen como layouts de ArcGIS Pro (el atlas profesional de
~40 mapas que Jerson está maquetando manualmente, distinto de este atlas
matplotlib rápido). Los campos `educacion_total` y `salud_total` ya están
listos en `mapa_master_canton.gpkg` para sourcing directo — mismo patrón
que los mapas de Población/Vivienda/Agricultura ya maquetados.

**Verificación de integridad (mismo patrón que la Fase 10d original):**
la agregación del dashboard usa `groupby` sobre 7 llaves, y pandas
descarta por defecto cualquier fila con un valor nulo en alguna de ellas.
35 de los 21,743 eventos (0.16%) tienen `province_name_official` nulo
(gap ya documentado de la unión espacial de Fase 2) y se excluyen de
*todas* las variables del dashboard, no solo las nuevas — de esos 35, 4
tenían escuelas afectadas (13 del total de 1,128) y 5 tenían centros de
salud afectados (5 del total de 320). El Excel y los mapas del Atlas
(que no usan esa agregación por mes) sí incluyen el 100% de los eventos.

## 12. Referencias

- Fase 0 — Diseño Conceptual EFCI Ecuador, §9 (productos), §14
  (entregables esperados).
- `docs/methodology/08_efci_composite.md` (fuente del EFCI y clases
  reutilizadas en los mapas), `09_spatial_analysis.md` (fuente de los
  hotspots reutilizados en el mapa 8 y el reporte ejecutivo §5.2).
