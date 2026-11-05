# 10b — Mapas de inundación, por separado (resumen ejecutivo)

**Primera de 4 versiones independientes por tipo de amenaza — completada el 17 de agosto de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Ya tienes el análisis de agrupamiento geográfico específico de inundación (ver el resumen ejecutivo de la Fase 9b). Esta etapa convierte ese análisis en los mismos 8 mapas y el atlas PDF que ya conocías del proyecto — pero esta vez mostrando solo inundación, no la mezcla de los 4 tipos de amenaza.

## Un problema que se encontró y se corrigió antes de entregarte el resultado

El primer mapa de cronicidad salió casi en blanco — casi todo el país en la categoría más baja, sin distinguir nada. La causa: el sistema intentó reutilizar una clasificación (de "muy baja" a "muy alta" cronicidad) que en realidad **nunca se había calculado específicamente para inundación** — solo existía para la vista combinada de los 4 peligros juntos. Se corrigió recalculando esa clasificación directamente sobre los datos reales de inundación, con el mismo método ya usado en todo el proyecto (quiebres naturales/Jenks). El mapa corregido sí muestra la variación real, y coincide con lo que ya viste en el análisis de puntos calientes (Fase 9b): la costa concentra la cronicidad alta, el oriente amazónico la baja.

Se documenta este ajuste explícitamente porque el mismo error se repetiría si se copia el mismo proceso para deslizamiento, socavamiento y aluvión sin corregirlo primero — ya queda anotado para no volver a cometerlo.

## ¿Qué se entrega?

Los mismos 8 mapas de siempre (frecuencia de inundaciones, severidad, frecuencia en meses El Niño, población afectada, pérdidas agrícolas, pérdidas de vivienda, cronicidad EFCI, y puntos calientes/fríos), ahora específicos de inundación, más un atlas PDF de 9 páginas (`Atlas_EFCI_Ecuador_Flood.pdf`).

**El cantón con mayor cronicidad de inundación del país es Chone (Manabí)**, seguido de Quito, Guayaquil, Babahoyo y Santo Domingo — un ranking centrado en la costa y las cuencas bajas, distinto del ranking combinado que ya conocías (donde Quito lideraba por una mezcla de deslizamientos y otros factores).

## ¿Qué falta?

Por ahora solo se construyeron los mapas estáticos y el atlas — los productos interactivos (mapas HTML, tablero, hoja de cálculo, perfiles por cantón, reporte Word) se harán después, para los 4 tipos de amenaza a la vez, una vez que confirmes que este primer resultado de inundación va en la dirección correcta. Y, según lo acordado, el siguiente paso pendiente de tu confirmación es replicar todo este trabajo (Fase 9 + Fase 10) para deslizamiento, socavamiento y aluvión.
