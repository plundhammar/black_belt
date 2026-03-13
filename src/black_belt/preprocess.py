import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union
from shapely.geometry import box
from .config import SOUTH_STATE_FIPS, MAP_CRS


def filter_south_counties(counties: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    counties = counties.copy()
    counties["STATEFP"] = counties["STATEFP"].astype(str).str.zfill(2)
    return counties[counties["STATEFP"].isin(SOUTH_STATE_FIPS)].copy()


def make_county_vote_table(
    elections: pd.DataFrame,
    year: int = 2020,
    dem_label: str = "DEMOCRAT",
    rep_label: str = "REPUBLICAN",
) -> pd.DataFrame:
    df = elections.copy()

    # Clean county FIPS robustly
    if "county_fips" not in df.columns:
        raise ValueError("Election file must contain county_fips.")

    df = df[df["county_fips"].notna()].copy()
    df["county_fips"] = df["county_fips"].astype(float).astype(int).astype(str).str.zfill(5)
    df["GEOID"] = df["county_fips"]

    # Keep only presidential total rows for the selected year
    if "office" in df.columns:
        df = df[df["office"] == "US PRESIDENT"].copy()

    if "mode" in df.columns:
        df = df[df["mode"] == "TOTAL"].copy()

    required = {"year", "party", "candidatevotes", "GEOID"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Election file is missing columns: {missing}")

    tmp = df.loc[
        (df["year"] == year) &
        (df["party"].isin([dem_label, rep_label])),
        ["GEOID", "party", "candidatevotes"]
    ].copy()

    wide = (
        tmp.pivot_table(
            index="GEOID",
            columns="party",
            values="candidatevotes",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )

    if dem_label not in wide.columns:
        wide[dem_label] = 0
    if rep_label not in wide.columns:
        wide[rep_label] = 0

    total_2party = wide[dem_label] + wide[rep_label]
    wide["dem_share_2party"] = wide[dem_label] / total_2party.where(total_2party > 0)
    wide["dem_margin_2party"] = (
        (wide[dem_label] - wide[rep_label]) / total_2party.where(total_2party > 0)
    )

    return wide[["GEOID", "dem_share_2party", "dem_margin_2party"]]


def merge_counties_votes(
    counties: gpd.GeoDataFrame,
    votes: pd.DataFrame,
) -> gpd.GeoDataFrame:
    gdf = counties.copy()
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)
    return gdf.merge(votes, on="GEOID", how="left")


def prepare_geometries_for_distance(
    counties: gpd.GeoDataFrame,
    coast: gpd.GeoDataFrame,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    counties = counties.to_crs(MAP_CRS)
    coast = coast.to_crs(MAP_CRS)
    return counties, coast


def clip_to_county_extent(
    counties: gpd.GeoDataFrame,
    gdf_other: gpd.GeoDataFrame,
    pad_km: float = 300.0,
) -> gpd.GeoDataFrame:
    xmin, ymin, xmax, ymax = counties.total_bounds
    pad = pad_km * 1000.0

    bbox_geom = box(xmin - pad, ymin - pad, xmax + pad, ymax + pad)
    bbox = gpd.GeoDataFrame(geometry=[bbox_geom], crs=counties.crs)

    return gpd.overlay(gdf_other, bbox, how="intersection")

def polygon_boundaries_as_lines(polygons: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    lines = polygons.copy()
    lines["geometry"] = lines.geometry.boundary
    lines = lines[~lines.geometry.is_empty & lines.geometry.notna()].copy()
    return lines


def compute_centroid_distance_km(
    counties: gpd.GeoDataFrame,
    coast_lines: gpd.GeoDataFrame,
    out_col: str = "dist_km",
) -> gpd.GeoDataFrame:
    gdf = counties.copy()
    coast_union = unary_union(coast_lines.geometry)
    gdf[out_col] = gdf.geometry.centroid.distance(coast_union) / 1000.0
    return gdf