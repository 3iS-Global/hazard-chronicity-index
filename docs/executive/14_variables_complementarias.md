# 14 — Qué más había en los datos y no se había usado (resumen ejecutivo)

**Fase 14 del proyecto HCI Ecuador — 18 de septiembre de 2026**
**Audiencia:** directores, tomadores de decisión, personal de FAO, especialistas no técnicos

## ¿Qué problema resuelve esta etapa?

Después de encontrar que Salud y Educación estaban en la base de
datos pero no tenían mapa propio, Jerson pidió revisar sistemáticamente
si había algo más así. La respuesta fue sí — y más grande de lo
esperado: el archivo de origen tiene 20 pestañas, y varias nunca se
habían abierto para el proyecto.

## ¿Qué se encontró?

**1. Vías y puentes — el hallazgo más grande de todos.** La base de
desastres registra "metros de vía afectada" en 6 de cada 10 eventos
dentro del alcance del proyecto, y en 213 de los 221 cantones del
país — una cobertura más amplia que Vivienda o Agricultura, que sí
están en el índice. Nunca tuvo mapa, tabla ni columna propia. Para un
sistema pensado para actuar antes de que ocurra el desastre, esto
importa de forma muy concreta: si una vía o un puente está dañado, la
ayuda no llega, sin importar qué tan bien calculada esté la prioridad.

**2. Un archivo oficial del gobierno, completo, nunca cruzado con el
HCI.** El mismo Excel de origen contiene la Resolución 193 del COE
Nacional — la lista oficial de 143 cantones que el gobierno ya
declaró prioritarios ante El Niño — más un modelo entero de
"escenarios de respuesta" (cuánta gente necesitaría ayuda en un
escenario débil, fuerte o extraordinario, y qué nivel de respuesta
activar). Nadie lo había comparado nunca con el HCI.

**3. Categorías humanitarias adicionales.** Familias afectadas (una
unidad distinta a "personas"), personas y familias "damnificadas"
(una categoría legal ecuatoriana más grave que "afectadas"), personas
acogidas por otras familias, y pérdidas de bienes públicos y privados
— ninguna se refleja hoy en el índice ni en ningún reporte.

## ¿Qué se hizo con esto?

- **2 mapas nuevos** en el atlas: Vías Afectadas y Puentes Afectados/
  Destruidos. El atlas pasa de 11 a 13 páginas.
- **2 hojas nuevas** en el Excel de estadísticas: una con las 8
  variables nuevas por cantón, y otra con la comparación contra el
  archivo del COE.
- **12 variables nuevas** en el filtro del tablero interactivo.
- **Un cruce completo del HCI contra la lista oficial del COE** — el
  hallazgo central de esta fase.

## El hallazgo del cruce con el COE — y qué significa

Al comparar el HCI con la lista oficial de 143 cantones prioritarios,
2 de cada 3 cantones que el HCI marca como "Alta" o "Muy Alta"
cronicidad SÍ están en esa lista oficial — pero el otro tercio no. El
caso más claro es **Ambato**: el segundo cantón con mayor cronicidad
de todo el país según el HCI, y no aparece en la lista oficial de 143
cantones prioritarios. Un grupo de cantones amazónicos (Morona,
Zamora, Pastaza, entre otros) tiene el mismo patrón.

Esto no quiere decir que el HCI esté mal, ni que la lista oficial
esté mal — miden cosas distintas. El HCI mira la historia completa
2015-2025 de 4 tipos de amenaza; el modelo del COE mira el peor
evento único de solo inundación relativo a la población expuesta.
Lo importante es que ahora hay evidencia concreta y cruzada para
llevar a una conversación con el COE Nacional: ¿debería Ambato (y el
grupo amazónico) estar en una futura actualización de la lista
oficial?

También se comparó qué tan parecidos son los 2 números (HCI del
proyecto vs. "peso de vulnerabilidad" del COE) para los mismos
cantones — el parecido es bajo (correlación débil, apenas
significativa). Es información honesta que hay que tener presente: no
son intercambiables, son 2 lentes distintas sobre el mismo problema.

## ¿Cómo contribuye esto al objetivo final?

El proyecto HCI necesita poder responder "¿por qué estos cantones y
no otros?" frente a un revisor externo — y ahora, por primera vez,
puede mostrar cómo se compara contra la propia designación oficial del
gobierno, con nombres y números concretos (Ambato, el clúster
amazónico), no solo en abstracto. Además, vías y puentes llenan un
vacío real: son el tipo de dato que una operación de Acción
Anticipatoria necesita para decidir cómo, y no solo dónde, actuar.

## ¿Qué falta?

- Decidir si compartir el hallazgo de Ambato/Amazonía con el COE
  Nacional como insumo para revisar la Resolución 193.
- Decidir si vías y puentes deberían convertirse en un componente
  propio del Índice de Severidad — es un cambio metodológico mayor,
  no se hizo automáticamente en esta fase.
- Bienes públicos/privados y las categorías humanitarias quedan
  disponibles en el Excel y el maestro de datos, pendientes de mapa
  propio si el equipo lo prioriza.
- Sigue pendiente la comparación contra EM-DAT, DesInventar y UNOSAT.
