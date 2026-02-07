"""Processing helpers for the biodiversity notebook."""
from typing import Tuple

import pandas as pd


def count_observations_by_species(observations: pd.DataFrame) -> pd.DataFrame:
    """Return total observations per scientific_name."""
    if "scientific_name" not in observations.columns or "observations" not in observations.columns:
        raise ValueError("observations must contain 'scientific_name' and 'observations'")
    counts = observations.groupby("scientific_name")["observations"].sum().reset_index()
    counts = counts.sort_values("observations", ascending=False).reset_index(drop=True)
    return counts


def observations_by_park(observations: pd.DataFrame) -> pd.DataFrame:
    if "park_name" not in observations.columns or "observations" not in observations.columns:
        raise ValueError("observations must contain 'park_name' and 'observations'")
    park_counts = observations.groupby("park_name")["observations"].sum().reset_index()
    park_counts = park_counts.sort_values("observations", ascending=False).reset_index(drop=True)
    return park_counts


def preprocess(species: pd.DataFrame, observations: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Clean species and observations and populate species['observations']."""
    obs = observations.copy()
    sp = species.copy()

    # drop duplicate rows in observations
    obs = obs.drop_duplicates()

    # normalize park names
    if "park_name" in obs.columns:
        obs["park_name"] = obs["park_name"].str.replace(" National Park", "", regex=True)

    # fill conservation_status
    if "conservation_status" in sp.columns:
        sp["conservation_status"] = sp["conservation_status"].fillna("Unknown")

    # deduplicate species by category+scientific_name
    if {"category", "scientific_name"}.issubset(sp.columns):
        sp = sp.drop_duplicates(subset=["category", "scientific_name"], keep="last")

    # compute observations per species and map back
    if "scientific_name" in obs.columns and "observations" in obs.columns and "scientific_name" in sp.columns:
            counts = count_observations_by_species(obs)
            # convert counts to a plain mapping to satisfy type checkers and ensure stable mapping
            obs_map = counts.set_index("scientific_name")["observations"].to_dict()
            sp["observations"] = sp["scientific_name"].map(obs_map).fillna(0).astype(int)

    return sp, obs

