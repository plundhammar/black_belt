from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "raw"
CENSUS_DIR = DATA_DIR / "census"
ELECTIONS_DIR = DATA_DIR / "elections"
PALEOMAP_DIR = DATA_DIR / "paleomap"

COUNTIES_SHP = CENSUS_DIR / "cb_2018_us_county_20m.shp"
ELECTIONS_CSV = ELECTIONS_DIR / "countypres_2000-2024.csv"

PALEOMAP_CM_DIR = PALEOMAP_DIR / "CM"
PALEOMAP_CS_DIR = PALEOMAP_DIR / "CS"