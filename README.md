# Hazard Chronicity Index (HCI)

**Chronicity of El Niño-associated hazards in Ecuador, 2015–2025 / Índice de cronicidad de amenazas asociadas a El Niño en Ecuador (2015–2025)**

Author: Jerson Achicanoy, Information Management and GIS Expert · Prepared by 3iS · © 2026

**Interactive dashboard / Tablero interactivo:** https://3is-global.github.io/hazard-chronicity-index/

## English

The HCI identifies in which Ecuadorian cantons floods, landslides, scour and debris flows recur chronically, how severe they are and how much they coincide with El Niño episodes. Its purpose is to support Anticipatory Action and territorial prioritisation.

### Repository layout

| Folder | Content |
|---|---|
| `index.html` | Interactive atlas (GitHub Pages home page) |
| `src/`, `tests/`, `config/` | Modular Python code, unit tests and configuration (`config/config.yaml`) |
| `notebooks/` | The full pipeline, one notebook per step (`Step1` … `Step15`), with Spanish comments followed by English comments |
| `scripts/` | Utilities: heavy-data download (`fetch_data.py`), Sentinel-1 / Google Earth Engine notebooks (`gee/`) and product generators (`products/`) |
| `data/processed/` | Aggregated results per canton and province (indices, hotspots, ENSO association) |
| `outputs/` | Maps (300 dpi), atlas PDF, tables, figures and dashboard |
| `docs/` | Methodology and executive notes per step, method infographic |
| `assets/branding/` | Logos used in the products |

### Method in brief

Each canton gets an index from 0 to 1 that combines four components and is classified into five levels (Very Low to Very High):

| Component | Weight | What it measures |
|---|---|---|
| Recurrence | 35 % | Event frequency, especially in El Niño months |
| Severity | 30 % | Worst historical impact on population, housing, agriculture, livestock and infrastructure |
| Persistence | 20 % | Length of consecutive affected months and number of affected months per year |
| El Niño magnitude | 15 % | Strength of the El Niño episodes faced (ICEN index, ENFEN) |

The weights were checked with AHP, alternative scenarios, Monte Carlo simulation, Sobol indices and PCA. The analysis is complemented by spatial statistics (Getis-Ord Gi*, Local Moran's I, kernel density, H3 hexagons), Sentinel-1 flood detection and a predictive impact model.

### How much is due to El Niño?

A negative binomial model adjusted for seasonality and trend compares El Niño and non-El Niño months: the signal is strong on the Coast (×3.5, and ×5 for floods), not detectable in the Highlands or the Amazon region, and inverse for debris flows. The index describes historical chronicity; **only on the Coast** can it be clearly attributed to El Niño.

### Scope and limitations

- It is not a rainfall or impact forecast.
- There are only 5 El Niño episodes in the period; results show association, not causation.
- It relies on SNGRE/ECU911 reports, whose coverage differs between regions and years.
- Regions (Coast, Highlands, Amazon) are assigned by province; some transition cantons may be misclassified.

### Data

The repository keeps only code, aggregated results and documentation. Source data are not redistributed: SNGRE/ECU911 reports are restricted and administrative boundaries come from INEC/HDX. Heavy data (models, parish-level boundaries) are declared in `config/data_sources.yaml` and fetched with:

```bash
python scripts/fetch_data.py
```

### Installation and tests

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
pytest
```

Python 3.12 is required. Notebooks expect to be run from the `notebooks/` folder. For the Earth Engine notebooks replace `YOUR_GEE_PROJECT_ID` with your own Google Cloud project; no credentials are stored in this repository.

### License and citation

Code is released under the MIT license (`LICENSE`). Documentation, results and the dashboard are released under CC BY 4.0 (`LICENSE-DOCS.md`). To cite this work use `CITATION.cff`. The United Nations and European Union logos in `assets/branding/` are not covered by these licenses and remain subject to their owners' terms of use.

## Español

El HCI identifica en qué cantones se repiten de forma crónica las inundaciones, deslizamientos, socavamientos y aluviones, qué tan graves son y cuánto coinciden con los episodios de El Niño. Su propósito es apoyar la Acción Anticipatoria y la priorización territorial.

La estructura de carpetas, el método (Recurrencia 35 %, Severidad 30 %, Persistencia 20 %, Magnitud de El Niño 15 %), los alcances y las limitaciones son los descritos arriba. En los notebooks y módulos, los comentarios en español se mantienen y la versión en inglés va justo debajo.

**Datos:** el repositorio guarda solo código, resultados agregados y documentación; los datos pesados se declaran en `config/data_sources.yaml` y se obtienen con `python scripts/fetch_data.py`.

**Instalación y pruebas:** `pip install -r requirements.txt` y `pytest` (Python 3.12).

Elaborado por 3iS · © 2026.
