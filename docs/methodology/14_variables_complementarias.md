# 14 — Variables complementarias no incorporadas: conectividad, bienes y validación cruzada con el COE Nacional

**Fase 14 del proyecto EFCI Ecuador — 18 de septiembre de 2026**
**Audiencia:** equipo técnico del proyecto

## 1. Objetivo

Tras el hallazgo de Educación y Salud (adición del 18 de septiembre de
2026, ver `docs/methodology/10_products.md` §11), Jerson pidió una
revisión sistemática: ¿qué otras variables existen en las fuentes de
datos del proyecto pero nunca se incorporaron a ningún producto? Esta
fase responde esa pregunta con una auditoría completa del archivo de
origen (`Indices ENSO (1).xlsx`, 20 hojas) contra el pipeline actual, y
ejecuta las 3 líneas de trabajo que Jerson priorizó de los hallazgos:

1. Conectividad vial (vías y puentes afectados).
2. Validación cruzada del EFCI contra 2 fuentes oficiales externas
   (Resolución 193 del COE Nacional y su modelo de Escenarios de
   Respuesta) encontradas en el mismo archivo.
3. Categorías humanitarias y de bienes adicionales (familias afectadas,
   personas/familias damnificadas, bienes públicos/privados).

## 2. Metodología de la auditoría

Se abrieron las 20 hojas de `Indices ENSO (1).xlsx` (más allá de
`BD_2015_2025`, ya usada desde la Fase 1) y se catalogó cada una. Para
las columnas de `BD_2015_2025` no mapeadas a `hazard_event.csv`
(comparando sus 63 columnas originales contra las 40 columnas del
esquema harmonizado de Fase 1), se calculó su tasa de llenado dentro
del alcance real del proyecto — los 21,743 eventos de los 4 peligros
(`EVENTO` en {Inundación, Deslizamiento, Socavamiento, Aluvión
(Flujos)}), no los 69,718 registros totales de la base cruda (que
incluye incendios forestales, sismos y otros peligros fuera de
alcance).

## 3. Hallazgo A — columnas de `BD_2015_2025` nunca incorporadas

| Variable | Eventos con dato > 0 (de 21,743) | % | Cantones con máximo histórico > 0 (de 221) |
|---|---|---|---|
| Metros lineales de vías afectadas | 12,832 | 59.0% | 213 |
| Familias afectadas | 5,890 | 27.1% | 217 |
| Personas damnificadas | 997 | 4.6% | 180 |
| Familias damnificadas | 883 | 4.1% | 174 |
| Bienes públicos afectados/destruidos | 880 / 196 | 4.0% / 0.9% | 178 |
| Bienes privados afectados/destruidos | 721 / 118 | 3.3% / 0.5% | 146 |
| Personas en familias acogientes | 455 | 2.1% | 143 |
| Puentes afectados/destruidos | 382 / 118 | 1.8% / 0.5% | 140 |
| Personas que resisten la evacuación | 16 | 0.07% | — (no mapeado, demasiado disperso) |

Se descartaron por baja relevancia dentro del alcance del proyecto:
"Ha. de cobertura vegetal quemada" (27,377 eventos en la base
completa, pero solo 2 dentro del alcance de las 4 amenazas — es una
variable de incendios forestales) y "Categoría de vía" (0 registros,
columna vacía en el origen).

Dos columnas del origen resultaron ser el mismo dato en dos unidades
("METROS LINEALES DE VÍAS AFECTADAS" y "Km lineales de vías
afecatdas" = metros/1000, verificado con la razón entre ambas =
0.001 exacto) — se usó solo la de metros.

**Por qué importa "vías":** es, con amplio margen, la variable no
incorporada más significativa del proyecto — presente en 59% de los
eventos dentro de alcance y en 213 de los 221 cantones, más amplia
incluso que Vivienda o Agricultura. Para un sistema pensado para
Acción Anticipatoria, la accesibilidad vial es un insumo operativo
directo (determina si la ayuda puede llegar), no solo descriptivo.

## 4. Implementación — extracción y agregación

`vías`, `puentes`, `bienes` y las categorías humanitarias no viven en
`hazard_event.csv`/`hazard_event_geo.gpkg` (se descartaron en la
harmonización de Fase 1, como todas las columnas no usadas del
esquema `Flood_Event`). Se extrajeron directamente de `BD_2015_2025`
uniendo por `event_id = ID` (verificado 1:1, sin duplicados, 21,743/
21,743 IDs de `hazard_event.csv` presentes en el origen) — no fue
necesario re-geocodificar, se reutiliza el `canton_code` ya validado
en Fase 2.

Se calculó el máximo histórico por cantón con la misma filosofía
"peor escenario esperable" ya usada para `poblacion_total` /
`vivienda_total` / `agricultura_total` / `educacion_total` /
`salud_total` (Fase 4 §4.1, extendida en la adición de Educación/
Salud): `puentes_total = max(afectados + destruidos)`,
`bienes_publicos_total` y `bienes_privados_total` de igual forma;
`vias_metros_afectados`, `familias_afectadas`, `familias_damnificadas`
y `personas_acogientes` toman directamente el máximo de un solo
evento (no son pares afectado+destruido).

Igual que con Educación/Salud, **estas variables son descriptivas —
no se incorporaron a la fórmula del Índice de Severidad ni del EFCI**.
Cambiar los pesos del índice es una decisión metodológica separada,
mayor, que requeriría repetir el análisis de sensibilidad de la Fase
13 — no se hizo sin una decisión explícita del equipo.

Columnas nuevas en `mapa_master_canton.csv`/`.gpkg` (221 cantones, 0
nulos): `vias_metros_afectados`, `puentes_total`,
`bienes_publicos_total`, `bienes_privados_total`, `familias_afectadas`,
`familias_damnificadas`, `damnificados_total`, `personas_acogientes`.

## 5. Productos generados

- 2 mapas nuevos en el atlas estático (`Step10a_Ecuador_Static_Maps.ipynb`):
  `11_vias_afectadas.png` y `12_puentes_afectados.png`. El atlas
  (`Atlas_EFCI_Ecuador.pdf`) pasa de 11 a 13 páginas (portada + 12
  mapas). Los demás componentes (públicos/privados, humanitarias) no
  se mapearon en esta ronda — se priorizó vías y puentes por volumen
  de datos; quedan disponibles en `mapa_master_canton.csv` para quien
  quiera mapearlos.
- 2 hojas nuevas en `EFCI_Ecuador_Estadisticas.xlsx`:
  `Variables_Complementarias` (ranking de 221 cantones por las 8
  variables nuevas) y `Validacion_COE` (ver sección 7).
- 12 variables nuevas en el filtro del tablero interactivo
  (`EFCI_Ecuador_Dashboard.html`), re-agregadas con las mismas 7
  llaves de agrupación (año/mes/provincia/cantón/categoría ENSO/
  amenaza) que las 13 variables ya existentes. Fila a fila: 9,604 =
  9,604 (coincide exacto con el dashboard antes del cambio). La suma
  nacional de vías afectadas en el tablero (1,140,770 m) tiene un
  desfase de 0.07% contra el dato fuente (1,141,532 m) — es el mismo
  gap preexistente de 35 eventos sin `province_name_official`
  documentado en la adición de Educación/Salud, no un error nuevo.

## 6. Hallazgo B — 2 fuentes de validación externa sin usar

Además de `BD_2015_2025`, el archivo de origen contiene un marco
paralelo construido aparentemente por o para el COE Nacional, nunca
cruzado con el EFCI:

- **Hoja "Resolución 193"**: lista oficial de 143 cantones designados
  prioritarios por Resolución 193 del COE Nacional.
- **Hoja "Opción 2"** (y su base "Escenarios y nivel de respuesta"):
  para 141-143 cantones, población expuesta bajo 1500msnm, máximo
  impacto histórico de un solo evento, un "Peso de Vulnerabilidad
  Real" (= máximo impacto / población expuesta), y 3 escenarios de
  impacto proyectado (Débil-Moderado = 50% del máximo histórico,
  Fuerte = 100%, Extraordinario = 150%) con su nivel de respuesta
  operativa asociado (30%/60%/100% de esos escenarios, mapeados a
  72 horas / GADs locales saturados / techo de Flash Appeal — según
  la hoja "Notas Metodológicas" del propio archivo).
- **Hoja "Hoja9"**: clasifica cada cantón en un "Nivel COE Proyectado"
  (Urgencia a Catástrofe Internacional) según umbrales fijos de
  población afectada proyectada.

Este marco es exactamente la clase de fuente de validación externa
que la sección de Validación del diseño original del proyecto pide
(gobierno, además de UNOSAT/EM-DAT/DesInventar/Copernicus EMS) y
nunca se había cruzado con el EFCI.

## 7. Validación cruzada — metodología y resultados

**Homologación de nombres:** se normalizó texto (mayúsculas, sin
tildes) y se unió por la llave compuesta `provincia|cantón` (no
`cantón` solo — hay 2 pares de cantones homónimos en provincias
distintas: Bolívar y Olmedo). Se aplicó el alias documentado en la
propia hoja "Notas Metodológicas" (Puerto Ayora → Santa Cruz, mismo
cantón). Resultado: 143/143 cantones de Resolución 193 encontraron
match exacto en el maestro de 221 cantones; 143/143 en Opción 2;
140/141 en Hoja9 (el no-match es "Puerto Villamil", que no es un
cantón sino la cabecera de Isabela — señalado como tal en la propia
hoja "Notas Metodológicas" del origen, no es un error de esta
homologación).

**a) Traslape EFCI vs Resolución 193.** De los 32 cantones que el
EFCI clasifica Alta o Muy Alta, 17 (53.1%) están también en la lista
oficial de 143 cantones del COE. Mirado al revés: de los 143 cantones
de Resolución 193, solo 17 (11.9%) tienen clase EFCI Alta o Muy Alta
— la mayoría de la lista oficial (110 de 143) tiene clase EFCI
Moderada o Baja.

15 cantones con clase EFCI Alta o Muy Alta **no están** en la lista
oficial de 143 — el caso más notable es **Ambato** (Tungurahua),
2º lugar nacional en EFCI (Muy Alta, 0.537), completamente ausente de
Resolución 193. El resto del grupo se concentra en la región
amazónica (Morona, Zamora, Pastaza, El Chaco, Archidona, Mera, Limón
Indanza, Santiago, Palanda, Quijos) y en las tierras altas de
Tungurahua/Chimborazo (Baños de Agua Santa, San Pedro de Pelileo,
Guano, Riobamba).

**b) Correlación EFCI vs "Peso de Vulnerabilidad Real".** Spearman
ρ=0.169 (p=0.044, n=143) — una correlación débil, apenas
estadísticamente significativa.

**c) Cruce clase EFCI × Nivel COE Proyectado (Escenario Fuerte).**
Coherente en los extremos (los 2 cantones EFCI Muy Alta caen en Nivel
4 - Desastre Nacional), pero con dispersión considerable en el medio
(las clases Moderada y Baja del EFCI se reparten entre los 5 niveles
COE sin un patrón claro). Tabla completa en
`data/processed/validacion_coe_canton.csv`.

## 8. Interpretación — por qué la correlación es débil, y qué significa

Esto **no es evidencia de que uno de los dos índices esté mal**. Miden
cosas distintas por diseño:

- El EFCI mide **cronicidad histórica multi-amenaza** (recurrencia +
  severidad + persistencia + magnitud ENSO, 2015-2025, las 4 amenazas
  del proyecto: inundación, deslizamiento, socavamiento, aluvión).
- El "Peso de Vulnerabilidad Real" del COE mide **la intensidad de un
  solo evento histórico máximo relativo a la población expuesta**
  bajo 1500msnm — no acumula recurrencia ni incluye deslizamientos/
  socavamientos.
- Resolución 193 es una designación administrativa — no está
  documentado en el origen qué criterio técnico exacto usó el COE
  para incluir o excluir un cantón, más allá de la nota de que 3
  cantones se agregaron después con población estimada por ratio
  provincial (Colimes, Coronel Marcelino Maridueña, Jama).

El hallazgo más accionable no es "el EFCI está mal" ni "Resolución
193 está mal" — es que **el EFCI identifica cantones de alta
cronicidad (Ambato el más claro, seguido de un clúster amazónico) que
la designación oficial actual no cubre**. Eso es información nueva y
concreta para la conversación de gobierno/validación (Sección 12 del
diseño original del proyecto), no una falla de ninguna de las dos
fuentes.

## 9. Riesgos y supuestos

- La homologación de nombres cantón/provincia se hizo por coincidencia
  exacta tras normalizar texto — funcionó al 100% en este caso (no
  hizo falta fuzzy matching), pero un cambio futuro de nomenclatura
  en cualquiera de las fuentes rompería el cruce silenciosamente si no
  se revalida.
- Las variables de conectividad/bienes/humanitarias son descriptivas,
  no ponderadas — no se debe asumir que un cantón con alto
  `vias_metros_afectados` pero EFCI bajo es "menos prioritario"; son
  lentes distintos.
- El desfase de 0.07% en vías en el dashboard (mismo origen que el
  gap de Educación/Salud: 35 eventos sin provincia geocodificada) no
  se resolvió aquí — sigue pendiente como se documentó en la adición
  anterior.

## 10. Próximos pasos

- Decidir si el hallazgo de Ambato/clúster amazónico amerita
  compartirse formalmente con el COE Nacional como insumo para una
  eventual actualización de Resolución 193.
- Evaluar si "vías y puentes" debe convertirse en un pilar propio del
  Índice de Severidad (hoy 5 pilares: población/vivienda/agricultura/
  ganadería/infraestructura) — requeriría repetir el análisis de
  sensibilidad de la Fase 13 antes de tocar los pesos.
- Bienes públicos/privados, familias afectadas y damnificados quedan
  en el maestro de datos y el Excel, pendientes de mapa propio si el
  equipo lo prioriza.
- Seguir con la comparación externa pendiente desde fases anteriores:
  EM-DAT, DesInventar, UNOSAT.
