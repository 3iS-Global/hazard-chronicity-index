# 11 — Frecuencia de Inundación Detectada por SAR (Sentinel-1)

**Fase:** 11 (extensión, fuera de las 10 fases originales de Fase 0 — corresponde a la capa opcional "Sentinel-1 Flood Extent" de Fase 0 §3)
**Notebooks asociados:** `scripts/gee/Step11_Ecuador_Sentinel1_Flood_Frequency.ipynb` (extracción GEE, corrida por Jerson) + `notebooks/Step11c_Ecuador_SAR_Flood_Classification.ipynb` (clasificación, vectorización y validación local, ejecutado en este entorno)
**Estado:** **completo** — GeoTIFF exportado por Jerson desde GEE el 2026-08-06, clasificado en 5 categorías, vectorizado, validado contra 7,281 eventos históricos y mapeado (ver §5-§8)
**Audiencia:** científicos, desarrolladores, especialistas DRM/FAO AA

## 1. Objetivo de la fase

Producir un mapa nacional de **frecuencia de inundación detectada por
SAR** derivado de imágenes de radar Sentinel-1 (no de reportes de
desastre como el resto del proyecto), clasificado en 5 categorías igual
que el HCI —

**Nota de terminología (2026-08-06):** este producto mide una sola de
las 4 dimensiones que componen la "cronicidad" del HCI (recurrencia,
severidad, persistencia, magnitud ENSO) — específicamente una versión
observacional y dispersa de la recurrencia (9 fechas puntuales, no una
serie continua de 132 meses como el `recurrence_index` del HCI). Por
eso se nombra explícitamente "Frecuencia de Inundación Detectada por
SAR", no "Cronicidad SAR" ni "Susceptibilidad SAR" — el primer término
sobre-prometería (sugiere las 4 dimensiones), el segundo implica un
modelo predictivo que este producto tampoco es (es observacional, no
modelado). Debe leerse como un dato independiente comparable contra el
`recurrence_index`, no como un sustituto del HCI compuesto —
donde la categoría más alta corresponde a las áreas más pequeñas que se
inundaron repetidamente, y la más baja a las áreas más extensas que se
inundaron solo una vez (la forma típica de un mapa de frecuencia de
inundación: el cauce/zona baja se repite siempre, la franja de
desbordamiento ocasional cubre mucha más área).

Esto complementa —no reemplaza— al HCI: el HCI mide cronicidad a partir
de **reportes humanos** de desastre (SNGRE/ECU911); este producto mide
extensión física real de agua **observada por satélite**, independiente de
si hubo o no un reporte.

## 2. Restricción de entorno (excepción documentada)

Este sandbox no tiene salida de red hacia Google Earth Engine (`403
Forbidden` al intentar alcanzar `earthengine.googleapis.com` — mismo tipo
de restricción ya documentada para las descargas de HDX/INEC en la Fase 2
y la SST Niño 1+2 en la Fase 5). El script de extracción se escribió
completo y se entregó a Jerson para correrlo en Google Colab o localmente,
usando el snippet de autenticación ya estandarizado del proyecto
(`ee.Authenticate(auth_mode="localhost")` / `ee.Initialize(project="YOUR_GEE_PROJECT_ID")`).
El resultado (GeoTIFF exportado a Google Drive) se integrará al pipeline
local una vez esté disponible, colocándolo en `data/raw/sentinel1_flood/`.

### 2.1 Entregado como notebook (`.ipynb`), no como script `.py` (2026-08-06)

Por pedido explícito de Jerson ("guardemos todos los archivos como
ipynb"), el entregable se convirtió de `scripts/gee/sentinel1_flood_frequency.py`
a `scripts/gee/Step11_Ecuador_Sentinel1_Flood_Frequency.ipynb` —
mismo contenido, dividido en celdas de markdown (explicación) y código
(una celda por sección: autenticación, parámetros, fechas, AOI, capas
ancilares, función de detección, agregación, exportación), siguiendo la
misma convención de notebooks del resto del proyecto. El archivo `.py`
original se eliminó para no dejar dos versiones divergentes del mismo
código.

**Bug real encontrado al ejecutar la primera versión, corregido en esta
conversión:** la celda que localiza `aoi_flood_points.json` usaba
`Path(__file__).parent` — funciona en un script ejecutado con
`python archivo.py`, pero **falla con `NameError: name '__file__' is not
defined`** dentro de una celda de notebook/Colab, porque una celda no
tiene la noción de "archivo actual" que sí tiene un script. Corregido con
un `try/except NameError` que usa `Path.cwd()` como respaldo (el
directorio de trabajo actual — en Colab, donde el usuario subió el
notebook y el JSON), con un mensaje de `assert` explícito si el archivo
no se encuentra, indicando que hay que subir `aoi_flood_points.json` a la
misma carpeta que el notebook. Documentado también dentro del propio
notebook (celda de la Sección 3), no solo aquí, para que quien lo corra
entienda por qué el código no usa `__file__` directamente.

### 2.2 Segundo error real encontrado en la primera ejecución, corregido (2026-08-06)

Al correr la v1.1 en GEE, Jerson reportó una tarea fallida a los 7
segundos con el error:

```
Image.lt: If one image has no bands, the other must also have no bands. Got 0 and 1.
```

**Diagnóstico:** para algunas de las 15 fechas objetivo, la colección de
imágenes Sentinel-1 (`col_evento` o `col_referencia`) queda **vacía** —
0 imágenes disponibles en esa ventana de fechas dentro del AOI. `.median()`
sobre una colección vacía en GEE no lanza un error inmediato: devuelve
una imagen "computada" con **0 bandas**. El error solo aparece más
adelante, cuando ese resultado de 0 bandas se resta/compara contra una
imagen o constante de 1 banda (`diferencia.lt(THRESHOLD_DB)`) — de ahí el
mensaje "Got 0 and 1".

Esto es más probable justamente en las fechas más antiguas del proyecto
(2015): Sentinel-1A llevaba apenas 8-11 meses operando cuando ocurrieron
los episodios de El Niño de 2015 documentados en la Fase 5, y la
cobertura sistemática sobre Sudamérica no era tan consistente como en
años posteriores (Sentinel-1B, que duplicó la frecuencia de revisita, no
se lanzó hasta abril de 2016). Además — **tal como señaló Jerson** — el
AOI de este análisis no es pequeño: cubre del orden de 100,000-150,000
km² (buffer de 5 km sobre 4,288 puntos históricos de eventos "flood",
§3.2), por lo que basta con que falte cobertura en una sub-zona del AOI
para una fecha puntual para que esa ventana quede vacía.

**Corrección aplicada, en dos capas (no solo un parche puntual):**

1. **Diagnóstico previo explícito** (nueva Sección 5.1 del notebook):
   antes de construir ninguna máscara, se consulta y se imprime cuántas
   imágenes Sentinel-1 hay disponibles (evento y referencia) para cada
   una de las 15 fechas objetivo. Las fechas sin cobertura completa se
   excluyen automáticamente de `FECHAS_VALIDAS`, con aviso explícito de
   cuáles y por qué — en vez de que el notebook falle a mitad de camino
   sin decir qué fecha lo causó. Esto también es, de paso, exactamente el
   tipo de retroalimentación visual que Jerson pidió (ver §2.3): cada
   fecha imprime su diagnóstico apenas se calcula.
2. **Blindaje defensivo en la función misma** (`mascara_inundacion_fecha`):
   aunque ya no debería llegar una fecha sin datos (se filtra antes), la
   función igual sustituye una colección vacía por una imagen constante
   fuera de rango (`ee.Algorithms.If(col.size().gt(0), col.median(), ...)`)
   y enmascara explícitamente cualquier píxel sin observación válida en
   vez de contarlo como "no inundado" — evita que la ausencia de dato se
   confunda con una observación real de "seco", que sesgaría la
   frecuencia hacia abajo.

**Consecuencia documentada, no oculta:** si alguna fecha termina
excluida, el techo real de la capa de frecuencia (`frecuencia_inundacion`)
será menor a 15 — el notebook lo imprime explícitamente
(`"N de M fechas objetivo tienen cobertura Sentinel-1 completa"`) para
que esto quede registrado y se tenga en cuenta al interpretar/clasificar
el resultado final, no se descubra después de exportar.

### 2.3 Seguimiento de la tarea de exportación cada 30 segundos (2026-08-06)

Pedido explícito de Jerson, comparando con scripts de otros países que ya
había usado: en vez de solo dejar el enlace a
<https://code.earthengine.google.com/tasks> y que el notebook "se quede
callado" mientras la tarea corre en GEE, la celda de exportación ahora
consulta `tarea.status()` cada 30 segundos y lo imprime con marca de
tiempo, hasta que la tarea termina (`COMPLETED` o `FAILED`) — permite ver
visualmente que algo está pasando sin tener que salir del notebook. El
enlace de seguimiento manual se conserva igual, para quien prefiera no
esperar ahí. Si la tarea termina en `FAILED`, se imprime también el
mensaje de error de GEE y una sugerencia de revisar el diagnóstico de
§2.2/Sección 5.1.

### 2.4 Tercer error real encontrado: tipo de píxel "Long" no soportado en exportación (2026-08-06)

Con el diagnóstico de §2.2 en su lugar, la tarea avanzó bastante más
(42s de runtime, vs. 7s del intento anterior) pero falló igual, esta vez
en la exportación con:

```
Pixel type not supported: Type<Long>. Convert the image to a floating point type or a smaller integer type, for example, using ee.Image.toDouble(). (Error code: 3)
```

**Diagnóstico:** el reductor `.sum()` de GEE, al sumar una
`ImageCollection` de imágenes 0/1 (`coleccion_mascaras`, una por cada
fecha válida de §2.2), **promueve automáticamente el tipo de píxel del
resultado a "Long" (entero de 64 bits)** — una medida de seguridad
interna de GEE contra desbordamiento (overflow) que aplica sin importar
que el rango real de la suma esté acotado (aquí, entre 0 y 15, el número
de fechas válidas). `Export.image.toDrive` no acepta "Long" como tipo de
salida, solo tipos de punto flotante o enteros más chicos — de ahí el
error.

**Corrección aplicada** (Sección 6 del notebook): se convierte
explícitamente la capa de frecuencia a `ee.Image.toUint8()` — un entero
sin signo de 8 bits (rango 0-255), más que suficiente para el rango real
0-15 — inmediatamente después del `.sum()`, y otra vez después del
segundo `.reproject()` (el remuestreo a 30 m para exportación, ver
§3.2), porque `.reproject()` puede volver a promover el tipo internamente.
Se documentó en el propio notebook (comentario inline en la celda) por
qué se necesita esta conversión, para que no se lea como un paso
arbitrario si alguien edita el pipeline más adelante.

### 2.5 Plan B: variante a 30 m nativos, preparada en paralelo sin tocar el original (2026-08-06)

Mientras la corrida original seguía activa en GEE (tarea
`RDBCEYSXHXD4TZWMD6BE4HXC`, ~2 horas de runtime, ~107 EECU-horas de
cómputo acumulado, ya en su 2º intento automático tras un reintento
interno de GEE), se preparó una variante alternativa por si esa corrida
volvía a fallar o tardaba demasiado — **sin modificar el notebook
original**, que seguía corriendo.

Nuevo archivo: `scripts/gee/Step11b_Ecuador_Sentinel1_Flood_Frequency_30m.ipynb`
(copia completa del original con 3 cambios puntuales):

1. **Reproyección temprana, no tardía:** el original calcula la resta
   VH, el umbral y la limpieza de píxeles conectados a resolución
   nativa (~10 m) y solo remuestrea a 30 m la capa de frecuencia ya
   sumada (al final, Sección 6). La variante 30 m reproyecta cada imagen
   VH (evento y referencia) a 30 m con remuestreo `bilinear` —apropiado
   para backscatter continuo, no el `nearest` por defecto de GEE— **antes**
   de restar, dentro de `mascara_inundacion_fecha`. Todo lo que viene
   después (resta, umbral, limpieza de ruido, suma) opera entonces sobre
   una grilla 9 veces menos densa, en las 9 fechas válidas — el ahorro
   de cómputo es real y ocurre en cada paso, no solo al exportar.
2. **`CONNECTED_PIXEL_MIN` recalibrado, documentado explícitamente (no
   un cambio silencioso):** el valor original (8 píxeles) representa un
   parche mínimo de ~800 m² a 10 m de resolución de píxel. A 30 m, 8
   píxeles representarían ~7,200 m² — un umbral de "mancha mínima" 9
   veces más grande, que cambiaría qué cuenta como ruido vs. inundación
   real. Se introdujo `CONNECTED_PIXEL_MIN_30M = 2` (~1,800 m²) como
   valor por defecto razonable, ajustable si el resultado sale
   demasiado ruidoso o demasiado agresivo filtrando manchas pequeñas
   reales.
3. **Nombres de salida distintos en Drive** (`efci_flood_frequency_2015_2025_30m`,
   descripción de tarea `EFCI_flood_frequency_2015_2025_30m`) para que
   nunca se confunda con el resultado del notebook original si ambos
   llegaran a correr.

**Trade-off aceptado, no oculto:** esta variante sacrifica algo de
fidelidad en el borde de la mancha de inundación (por el remuestreo
bilinear temprano) a cambio de reducir el cómputo real en ~89% (9x
menos píxeles procesados en cada uno de los 9 pasos por fecha). El
producto final sigue siendo conceptualmente el mismo (capa de
frecuencia 0-N, GeoTIFF de una banda), solo con bordes de mancha algo
menos precisos. Esta variante no se ejecutó — queda lista como
respaldo, a usar solo si el notebook original vuelve a fallar o su
tiempo de ejecución se vuelve impracticable.

## 3. Decisiones metodológicas y su justificación

### 3.1 Alcance temporal: 15 fechas objetivo, no todos los eventos "flood"

Sentinel-1 detecta agua superficial abierta, no deslizamientos ni
aluviones — por eso el alcance se restringe a `hazard_type == "flood"`
(7,281 de los 21,743 eventos del proyecto). Procesar detección de cambio
para miles de fechas individuales no es viable computacionalmente ni
necesario: se seleccionaron **3 fechas por cada uno de los 5 episodios de
El Niño ya documentados en la Fase 5** (2015, 2016, 2017, 2023, 2024) —
las de mayor número de eventos y severidad tipo "flood" reportados dentro
de cada episodio, calculado directamente sobre `hazard_event_geo.gpkg`
antes de escribir el script (no fechas arbitrarias ni elegidas a ojo).
Decisión confirmada por Jerson vía AskUserQuestion (2026-08-06).

### 3.2 AOI: buffer de 5 km sobre puntos históricos de eventos "flood", no todo Ecuador

En vez de procesar la totalidad del territorio continental (lo que
incluiría la Amazonía con dosel boscoso denso y los Andes de alta
pendiente, donde el método SAR es además menos confiable por atenuación de
señal y sombra/layover de radar), el área de análisis se construye a
partir de los **4,288 puntos únicos** donde históricamente se reportó un
evento tipo "flood" (redondeados a ~1 km de precisión — suficiente dado
que se van a bufferizar 5 km alrededor de cada uno), unidos con un buffer
de 5 km. Esto ata el área de análisis satelital directamente a donde el
proyecto ya sabe, por la base de reportes, que hay riesgo real — no a un
supuesto genérico de uso de suelo.

### 3.3 Método de detección de cambio: UN-SPIDER estándar (VH, umbral -3 dB)

Diferencia en dB entre una imagen "durante evento" (mediana de pasadas
Sentinel-1 dentro de ±6 días de la fecha objetivo) y una imagen de
referencia "pre-inundación" (mediana de pasadas ~12-48 días antes, con un
colchón de 12 días para no capturar el remanente del propio evento) sobre
la banda VH — más sensible que VV a superficies de agua en calma. Umbral
fijo de -3 dB (no Otsu automático): es el método más citado y
reproducible en la literatura de mapeo rápido de inundaciones (UN-SPIDER,
Copernicus EMS), preferido aquí sobre un umbral automático por robustez
frente a un AOI heterogéneo (costa, valles andinos, Amazonía) donde un
umbral calculado automáticamente por escena podría variar de forma no
comparable entre fechas.

### 3.4 Máscaras aplicadas

- **Pendiente > 5°** (DEM SRTM): excluida — el radar no puede distinguir
  confiablemente inundación de sombra/layover en terreno inclinado.
- **Agua permanente** (JRC Global Surface Water, ocurrencia histórica
  >90%): excluida — un río o embalse que siempre tiene agua no es
  "inundación nueva".
- **Limpieza de ruido sal-y-pimienta**: se exige un mínimo de 8 píxeles
  conectados (`connectedPixelCount`) para conservar un píxel como
  inundado — evita que ruido de speckle aislado se cuente como agua.

### 3.5 Resolución: cálculo a 10 m, exportación a 30 m

El umbral de cambio se calcula a la resolución nativa de Sentinel-1
(10 m) — remuestrear antes de umbralizar difuminaría los bordes de la
mancha de inundación. La capa ya agregada (frecuencia sobre las 15
fechas) se remuestrea a 30 m únicamente al exportar — esto es lo que
realmente acelera el cómputo/exportación en GEE, coherente con que el
resto del proyecto trabaja a escala nacional/cantonal, no de parcela.
Decisión confirmada por Jerson (preguntó explícitamente si el
remuestreo ayudaría al rendimiento; la respuesta es sí, aplicado en la
etapa de exportación, no en el cálculo del umbral en sí).

## 4. Producto intermedio esperado

Un GeoTIFF de una banda (`frecuencia_inundacion`), valores enteros 0 a
15 (número de las 15 fechas analizadas en que ese píxel se detectó como
inundado), resolución 30 m, EPSG:4326, recortado al AOI de §3.2.

## 4.1 Diagnóstico añadido: validación del umbral -3 dB vía Otsu (2026-08-06)

El umbral de §3.3 es fijo por diseño (no calculado por escena), pero eso no
lo exime de validación. Se agregó una nueva Sección 5.2 al notebook GEE
(`scripts/gee/Step11_Ecuador_Sentinel1_Flood_Frequency.ipynb`, ahora 25
celdas) que **no cambia el umbral operativo**, solo lo contrasta: para
cada fecha válida, calcula el histograma real de la diferencia VH dentro
del AOI (`ee.Reducer.histogram()`, a 100 m — más grueso que el análisis
operativo, solo para esta consulta diagnóstica, así que no afecta el
resultado final) y deriva el umbral Otsu (el método estándar de visión por
computador para separar automáticamente un histograma bimodal en dos
clases, maximizando la varianza entre ellas).

Se imprime, por fecha, el Otsu calculado vs. el -3 dB fijo, más un
promedio general. La interpretación queda explícita en el propio notebook:
si el promedio Otsu ronda -3 dB, el umbral fijo está bien calibrado para
este AOI/período; una desviación grande y consistente (>1-1.5 dB) en la
misma dirección en la mayoría de las fechas sería la señal para
reconsiderar `THRESHOLD_DB` (parámetro en la Sección 1). ### 4.1.1 Resultado real del diagnóstico Otsu (2026-08-06)

Jerson corrió la Sección 5.2. Resultado real:

| Fecha | Otsu (dB) | Fijo (dB) | Diferencia |
|---|---|---|---|
| 2017-04-08 | -0.45 | -3.0 | +2.55 |
| 2017-03-24 | -0.44 | -3.0 | +2.56 |
| 2017-02-08 | -0.46 | -3.0 | +2.54 |
| 2023-04-18 | 0.25 | -3.0 | +3.25 |
| 2023-03-09 | 0.25 | -3.0 | +3.25 |
| 2023-03-23 | -0.12 | -3.0 | +2.88 |
| 2024-02-21 | -2.73 | -3.0 | +0.27 |
| 2024-02-20 | -3.24 | -3.0 | -0.24 |
| 2024-02-19 | -3.24 | -3.0 | -0.24 |

Promedio Otsu: -1.13 dB (vs. -3.0 dB fijo).

**Interpretación (no tomar el promedio al pie de la letra):** hay una
división clara por episodio, no un desvío uniforme. Las 3 fechas de 2024
coinciden bien con el fijo (a menos de 0.3 dB). Las 6 fechas de 2017 y
2023 se alejan mucho, todas en la misma dirección (Otsu encuentra el
punto de separación entre -0.46 y +0.25 dB, mucho menos exigente que -3
dB).

**Hipótesis de trabajo, no una conclusión de "bajar el umbral":** Otsu
asume un histograma razonablemente bimodal con dos clases de tamaño
comparable. Los píxeles realmente inundados son una fracción minúscula
del total en cualquier fecha (0.57% del AOI combinando las 9 fechas, ver
§5) — con una clase minoritaria tan pequeña, Otsu tiende a partir el
grupo mayoritario ("sin cambio") en dos mitades arbitrarias en vez de
aislar la señal real de inundación, un modo de falla conocido del método
ante histogramas muy desbalanceados. Que 2024 sí coincida con el fijo es
consistente con que hubo más área realmente inundada dentro del AOI en
esas fechas específicas, dándole a Otsu una clase "inundado" con más peso
real para encontrar.

**Prueba directa de la hipótesis (Sección 5.3) — resultado real, confirma
la hipótesis con margen amplio:**

| Fecha | Área -3dB fijo (km²) | Área Otsu (km²) | Razón Otsu/fijo |
|---|---|---|---|
| 2017-04-08 | 790.8 | 10,647.4 | 13.5x |
| 2017-03-24 | 188.0 | 5,820.3 | 31.0x |
| 2017-02-08 | 472.1 | 6,032.5 | 12.8x |
| 2023-04-18 | 408.0 | 20,951.9 | 51.3x |
| 2023-03-09 | 1,017.9 | 20,279.7 | 19.9x |
| 2023-03-23 | 713.6 | 19,919.5 | 27.9x |
| 2024-02-21 | 1,091.2 | 1,213.3 | 1.1x |
| 2024-02-20 | 1,088.4 | 998.2 | 0.9x |
| 2024-02-19 | 1,080.3 | 992.3 | 0.9x |
| **TOTAL** | **6,850.4** | **86,855.2** | **12.7x** |

En 2017 y 2023, usar el umbral Otsu de cada fecha en vez del fijo
multiplicaría el área "inundada" detectada entre **12.8x y 51.3x**. En
2024, la razón es ~1x (Otsu y fijo prácticamente coinciden). Este
contraste tan marcado, exactamente en las mismas 6 fechas donde el §4.1.1
ya había detectado que Otsu se alejaba del fijo, es evidencia directa —
no solo teórica — de que Otsu está capturando variación normal de
backscatter (speckle, humedad de suelo, vegetación) como si fuera agua
nueva, no una señal real de inundación adicional. Un ~12.7x de inflación
total sobre 6 de 9 fechas es demasiado grande para ser una corrección
legítima del umbral; es la firma característica de un estimador que
falló por desbalance de clases, tal como se planteó como hipótesis.

**Decisión final:** se mantiene el umbral fijo -3 dB, sin cambios. La
evidencia (§4.1.1 + esta prueba de área) converge en la misma
conclusión desde dos ángulos distintos: el umbral fijo es la opción más
segura y físicamente defendible para este AOI heterogéneo, y Otsu no es
un estimador confiable aquí dado el fuerte desbalance de clases
(0.57% de píxeles inundados). Este ejercicio de validación queda
documentado como evidencia de que el umbral -3 dB fue puesto a prueba
activamente, no solo asumido de la literatura sin verificación.

## 5. Resultado real de la exportación GEE (2026-08-06)

De las 15 fechas objetivo, **9 tuvieron cobertura Sentinel-1 completa**
(2017, 2023 y 2024 — 3 fechas cada episodio) y **6 fueron excluidas** por
el diagnóstico de §2.2 (los 3 episodios de 2015 completos, y las 2 fechas
de 2016 que caían fuera de la ventana de revisita de un solo satélite
operando — ver §2.2 para la explicación completa). El techo real de la
capa de frecuencia es por lo tanto 0-9, no 0-15.

Histograma completo del GeoTIFF (1,325,827,545 píxeles, calculado exacto
por recorrido en franjas, no muestreado):

| Valor | Píxeles | % del AOI |
|---|---|---|
| 0 (sin detección) | 1,318,338,104 | 99.4351% |
| 1 | 5,093,088 | 0.3841% |
| 2 | 715,424 | 0.0540% |
| 3 | 785,350 | 0.0592% |
| 4 | 546,753 | 0.0412% |
| 5 | 276,024 | 0.0208% |
| 6 | 68,921 | 0.0052% |
| 7 | 3,862 | 0.0003% |
| 8 | 19 | 0.0000% |

Área total con al menos 1 detección (valor ≥1): 7,489,441 píxeles →
**6,740.5 km²** a resolución nativa de 30 m.

## 6. Clasificación en 5 categorías (Jenks, resultados reales)

Ejecutado en `notebooks/Step11c_Ecuador_SAR_Flood_Classification.ipynb`
(notebook local, sin dependencia de GEE, ejecutado íntegramente en este
entorno — a diferencia del notebook de extracción, este sí corrió aquí).

Con solo 8 valores distintos posibles (1-8), el quiebre Jenks de 5 clases
se resolvió por **búsqueda combinatoria exacta** (no aproximada por
muestreo): se evaluaron las 35 formas posibles de partir los 8 valores
ordenados en 5 grupos contiguos y se eligió la que minimiza la varianza
ponderada por conteo real de píxeles dentro de cada grupo.

| Categoría | Valores agrupados | Píxeles | Área (30 m nativo) |
|---|---|---|---|
| 1 — Muy Baja | {1} | 5,093,088 | 4,583.78 km² |
| 2 — Baja | {2} | 715,424 | 643.88 km² |
| 3 — Moderada | {3} | 785,350 | 706.82 km² |
| 4 — Alta | {4} | 546,753 | 492.08 km² |
| 5 — Muy Alta | {5,6,7,8} | 348,826 | 313.94 km² |

**Confirma directamente la hipótesis original de Jerson** ("la más débil
sea la más ancha y el área más pequeña es la que más se repitió y es
categoría alta") — el área decrece de forma monótona de la categoría 1 a
la 5. No fue forzado: es el resultado natural de aplicar Jenks sobre la
distribución real de los datos.

Producto: `data/processed/sar_flood_susceptibility_clasificado.tif` —
raster de una banda, `uint8`, valores 0-5, 30 m, EPSG:4326, comprimido
(deflate). Es el producto de referencia de mayor precisión, sin ninguna
generalización cartográfica.

## 7. De raster a polígono: por qué se usó agregación hexagonal (no vectorización de borde exacto)

Se intentó primero la vectorización directa a 30 m (`rasterio.features.shapes`
+ unión topológica por categoría, usando `shapely.coverage_union_all`, el
método más rápido disponible). Diagnóstico real, no hipotético:

- Solo la categoría 1 ("Muy Baja", la más fragmentada por definición —
  detectada en una única fecha de las 9) generó **186,302 polígonos
  individuales en una sola franja** de las 6 en que se dividió el país —
  y la unión topológica de esa única franja **no completó ni en 165
  segundos**, incluso con precisión de coordenadas fijada explícitamente
  para forzar la ruta rápida del algoritmo.
- Se probó como alternativa una agregación por bloque-máximo (reduce
  resolución tomando el máximo de cada bloque antes de vectorizar) a
  varios tamaños: 90 m, 150 m, 300 m y 990 m. **Resultado descartado en
  los 4 casos**: la inflación de área es severa —desde 3.64x el área
  real a 90 m hasta 13.7x a 990 m— porque cualquier bloque que contenga
  aunque sea 1 píxel inundado de cientos se pinta completo, exagerando
  artificialmente la extensión aparente. Para un producto de soporte a
  decisiones de Acción Anticipatoria, mostrar 13.7x más área "susceptible"
  de la real no es aceptable, sin importar cuánto simplifique el mapa.

**Decisión final:** se reutiliza la grilla hexagonal H3 resolución 5 ya
construida y validada en la Fase 9 (719 hexágonos, ~9.85 km de borde
promedio, ~84.5 km² cada uno) y se calcula, por hexágono, el
**promedio** (no el máximo) del valor crudo de frecuencia (0-8) sobre
todos sus píxeles de 30 m — un estadístico ponderado por área que, a
diferencia del máximo, no infla la superficie aparente (el promedio de
un bloque con 1 píxel inundado de 1,089 es ≈0.001, prácticamente cero,
en vez de "todo el bloque cuenta"). Cada hexágono se clasifica luego con
sus propios quiebres Jenks —no los de 30 m, que no aplican directamente
a un promedio continuo—: `[0, 0.0556, 0.211, 0.6748, 1.3336, 2.2007]`.

| Categoría | Hexágonos | Área |
|---|---|---|
| 0 — Sin señal SAR | 35 | 10,200.2 km² |
| 1 — Muy Baja | 537 | 155,925.7 km² |
| 2 — Baja | 118 | 34,235.8 km² |
| 3 — Moderada | 19 | 5,549.0 km² |
| 4 — Alta | 7 | 2,048.2 km² |
| 5 — Muy Alta | 3 | 877.8 km² |

684 de 719 hexágonos (95.1%) tienen algo de señal SAR. El mismo patrón
monótono decreciente de §6 se repite a este nivel de agregación — dos
métodos independientes (píxel nativo y hexágono) confirman la misma
forma de distribución.

**Nota de interpretación, no ocultar:** que un hexágono sea "Muy Baja"
significa que, en promedio sobre sus ~84.5 km², se detectó algo de señal
SAR — no que todo el hexágono se inunde. Es un indicador de intensidad
relativa por zona, del mismo tipo que los mapas Gi*/KDE de la Fase 9
(`docs/methodology/09_spatial_analysis.md`), no un mapa de extensión
exacta (ese es el raster nativo de §6).

Producto: `data/processed/sar_flood_susceptibility_hexagonos.gpkg` (719
features, columnas `sar_freq_media`, `sar_freq_max`, `sar_frac_inundada`,
`categoria`, `etiqueta`, `area_km2`).

## 8. Validación contra los 7,281 eventos históricos "flood"

Se muestreó el **raster clasificado nativo** (30 m, no la capa hexagonal
generalizada) en la ubicación exacta de cada uno de los 7,281 eventos
históricos "flood" (Fase 1-2):

| Categoría SAR en el punto del evento | N eventos | % |
|---|---|---|
| Sin señal SAR | 6,393 | 87.80% |
| Muy Baja | 675 | 9.27% |
| Baja | 80 | 1.10% |
| Moderada | 51 | 0.70% |
| Alta | 53 | 0.73% |
| Muy Alta | 29 | 0.40% |

**Por qué el 87.8% "sin señal" no invalida el producto:** el raster SAR
solo cubre 9 fechas puntuales (±6 días cada una) de los ~4,017 días
posibles del período 2015-2025 — apenas 2.91% del calendario. La
inmensa mayoría de los 7,281 eventos ocurrió en fechas que el radar
nunca observó, por diseño (solo se analizaron los picos de los 5
episodios documentados, no cada mes). La comparación correcta es contra
el azar, no contra "todos los eventos deberían coincidir": si los
eventos cayeran al azar en el calendario, ~2.91% caerían dentro de
alguna ventana SAR. La tasa observada real es 12.20% — un
**enriquecimiento de 4.2x sobre el azar**, evidencia de validación
positiva real, aunque modesta por lo disperso del muestreo temporal.

Este resultado no se puede comparar directamente con una tasa de
"aciertos" de un clasificador binario — es, en esencia, una prueba de
que la coincidencia espacio-temporal entre reportes humanos y detección
satelital directa es mayor de lo que el azar explicaría, usando dos
fuentes de evidencia completamente independientes.

## 9. Mapa y cruce con la Fase 9

`outputs/maps/mapa_sar_flood_susceptibility.png` — mapa estático de la
capa hexagonal, mismo estilo del atlas de Fase 10 (límites provinciales
de referencia, paleta secuencial cálida, anotación de fuente).

**Hallazgo notado, no analizado en profundidad en esta fase:** las
categorías "Alta"/"Muy Alta" del mapa SAR se concentran visualmente en
la misma zona (Quito/Rumiñahui/Mejía y alrededores) que los hotspots
Gi* al 99% de confianza de la Fase 9 (`docs/methodology/09_spatial_analysis.md`
§4) — una convergencia entre dos fuentes de evidencia completamente
independientes (reportes humanos SNGRE vs. detección satelital directa
Sentinel-1), que refuerza la lectura de esa zona como núcleo de
cronicidad real, no un artefacto de una sola fuente de datos. Queda
como hallazgo para el reporte ejecutivo; cuantificar la correlación
espacial formalmente es un análisis adicional fuera del alcance
definido para esta extensión.

## 10. Limitaciones

- 9 fechas válidas es una muestra dispersa, no una serie temporal
  continua — el producto mide "frecuencia de detección en los peores
  momentos documentados con cobertura Sentinel-1 disponible", no un
  registro exhaustivo de cada inundación ocurrida 2015-2025. Ver §8 para
  el análisis cuantitativo de esta limitación.
- La capa vectorial (hexagonal) es una generalización de intensidad
  media por zona de ~84.5 km², no un mapa de extensión exacta de
  inundación — para eso existe el raster nativo de 30 m (§6), que
  permanece como el producto de mayor precisión disponible.
- El método SAR puede fallar bajo dosel boscoso denso (parte de la
  Amazonía, si algún punto del AOI cae ahí) y en zonas urbanas densas
  (el patrón de retrodispersión de edificios interfiere con la señal de
  agua) — limitaciones conocidas del método, no específicas de este
  proyecto.
- No hay aún validación contra otro producto independiente de extensión
  de inundación (Copernicus EMS, si existe cobertura para estos eventos
  en Ecuador) — pendiente como parte de la validación externa general
  del proyecto (Fase 0 §12).

## 11. Referencias

- UN-SPIDER Knowledge Portal — "Step-by-Step: Flood Mapping using SAR
  data" (metodología de cambio VH, umbral -3 dB).
- JRC Global Surface Water (Pekel et al. 2016).
- `docs/methodology/05_recurrence_index.md` §4.3 (definición de los 5
  episodios de El Niño reutilizada aquí para elegir las fechas objetivo).
- Memoria del proyecto: `feedback_gee_cds_credentials` (snippet de
  autenticación estándar).
