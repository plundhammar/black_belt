from pathlib import Path
import geopandas as gpd
import pandas as pd


def read_counties(path: str | Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    return gdf


def read_elections(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    return df


def read_paleomap(path: str | Path) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    return gdf


def inspect_gdf(name: str, gdf: gpd.GeoDataFrame, n: int = 5) -> None:
    print(f"\n=== {name} ===")
    print("CRS:", gdf.crs)
    print("Shape:", gdf.shape)
    print("Columns:")
    print(list(gdf.columns))
    print("\nHead:")
    print(gdf.head(n))


def inspect_df(name: str, df: pd.DataFrame, n: int = 5) -> None:
    print(f"\n=== {name} ===")
    print("Shape:", df.shape)
    print("Columns:")
    print(list(df.columns))
    print("\nHead:")
    print(df.head(n))

def inspect_geometry_types(name: str, gdf: gpd.GeoDataFrame) -> None:
    print(f"\n=== geometry types: {name} ===")
    print(gdf.geom_type.value_counts(dropna=False))