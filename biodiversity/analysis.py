"""Higher-level analysis utilities extracted from the notebook."""
from typing import Dict, List, Tuple

import pandas as pd


def observation_stats(observations: pd.DataFrame) -> Dict[str, int]:
    """Compute simple overall statistics for the observations DataFrame."""
    return {
        "total_observations": int(observations.shape[0]),
        "unique_species": int(observations["scientific_name"].nunique()),
        "unique_parks": int(observations["park_name"].nunique()) if "park_name" in observations.columns else 0,
    }


def top_species_by_observations(observations: pd.DataFrame, n: int = 1) -> pd.DataFrame:
    """Return the top-n species by total observations."""
    if "scientific_name" not in observations.columns or "observations" not in observations.columns:
        raise ValueError("observations must contain 'scientific_name' and 'observations'")
    counts = observations.groupby("scientific_name")["observations"].sum().reset_index()
    counts = counts.sort_values("observations", ascending=False).reset_index(drop=True)
    return counts.head(n)


def species_stats(species: pd.DataFrame) -> Dict[str, object]:
    """Return basic statistics about the species DataFrame."""
    res: Dict[str, object] = {"num_species": int(species.shape[0])}
    if "category" in species.columns:
        res["num_categories"] = int(species["category"].nunique())
    if "conservation_status" in species.columns:
        res["conservation_status_values"] = list(species["conservation_status"].dropna().unique())
    return res


def at_risk_species_df(species: pd.DataFrame) -> pd.DataFrame:
    """Filter species DataFrame to 'at risk' rows (not Unknown)."""
    if "conservation_status" not in species.columns:
        raise ValueError("species must contain 'conservation_status'")
    return species[~species["conservation_status"].isin(["Unknown"])]


def at_risk_observations(observations: pd.DataFrame, species: pd.DataFrame) -> pd.DataFrame:
    """Return observations rows for species that are at risk."""
    at_risk = at_risk_species_df(species)
    return observations[observations["scientific_name"].isin(at_risk["scientific_name"])]


def filter_bats(species: pd.DataFrame) -> pd.DataFrame:
    """Return rows in species whose common_names mention 'Bat'."""
    if "common_names" not in species.columns:
        return species.iloc[0:0]
    return species[species["common_names"].str.contains("Bat", case=True, na=False)]


def get_at_risk_summary(species: pd.DataFrame) -> pd.DataFrame:
    """Return a summary (count, pct) of at-risk species by conservation_status."""
    ar = at_risk_species_df(species)[["scientific_name", "conservation_status"]]
    summary = (
        ar.groupby("conservation_status")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .reset_index(drop=True)
    )
    summary["pct"] = summary["count"] / summary["count"].sum() * 100
    return summary


def get_unknown_status_by_category(species: pd.DataFrame) -> pd.DataFrame:
    """Return counts of species with Unknown status by category and status."""
    not_at_risk = species[species["conservation_status"].isin(["Unknown"])][
        ["scientific_name", "category", "conservation_status"]
    ]
    return not_at_risk.groupby(["category", "conservation_status"]).size().reset_index(name="count")


def conservation_pivot_by_category(species: pd.DataFrame) -> pd.DataFrame:
    """Return a pivot table (category x conservation_status) of counts sorted by total descending."""
    df = species[["scientific_name", "category", "conservation_status"]].copy()
    df = df[~df["conservation_status"].isna()]
    cat_status_counts = df.groupby(["category", "conservation_status"]).size().reset_index(name="count")
    pivot_df = cat_status_counts.pivot(index="category", columns="conservation_status", values="count").fillna(0)
    # Exclude the 'Unknown' column from the pivot (we don't want Unknown shown in stacked charts)
    if "Unknown" in pivot_df.columns:
        pivot_df = pivot_df.drop(columns=["Unknown"])
    pivot_df["total"] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values("total", ascending=False).drop(columns=["total"])
    return pivot_df


def at_risk_by_park(observations: pd.DataFrame, species: pd.DataFrame) -> pd.DataFrame:
    """Return total observations per park for at-risk species."""
    aro = at_risk_observations(observations, species)
    if "park_name" not in aro.columns or "observations" not in aro.columns:
        raise ValueError("observations must contain 'park_name' and 'observations'")
    res = aro.groupby("park_name")["observations"].sum().reset_index()
    return res.sort_values("observations", ascending=False).reset_index(drop=True)

