"""Visualization helpers for the biodiversity project."""
from typing import Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns


def seaborn_barplot(
    df: pd.DataFrame,
    x: str,
    y: str,
    hue: str | None = None,
    order: list | None = None,
    figsize: tuple = (10, 5),
) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=df, x=x, y=y, hue=hue, order=order, ax=ax)
    plt.tight_layout()
    return fig, ax


def plot_at_risk_summary(summary_df: pd.DataFrame, figsize: tuple = (8, 6)) -> Tuple[Figure, Axes]:
    """Plot at-risk species summary DataFrame (must contain 'conservation_status','count','pct')."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=summary_df, x="conservation_status", y="count", order=summary_df["conservation_status"], ax=ax)
    for bar, pct in zip(ax.containers[0], summary_df["pct"]):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()
        ax.text(x, y, f"{pct:.1f}%", ha="center", va="bottom", fontsize=10)
    ax.set_title("At-Risk Species by Conservation Status")
    ax.set_ylabel("Count")
    ax.set_xlabel("Conservation Status")
    plt.tight_layout()
    return fig, ax


def plot_unknown_status_by_category(df: pd.DataFrame, figsize: tuple = (8, 6)) -> Tuple[Figure, Axes]:
    """Plot species with Unknown status by category (expects columns: category, conservation_status, count)."""
    fig, ax = plt.subplots(figsize=figsize)
    sns.barplot(data=df, x="category", y="count", hue="conservation_status", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_title("Species with Unknown Conservation Status by Category")
    ax.set_ylabel("Number of Species")
    ax.set_xlabel("Biological Category")
    plt.tight_layout()
    return fig, ax



def plot_stacked_bar_from_pivot(pivot_df: pd.DataFrame, palette: str = "Set2", figsize: tuple = (8, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    # ensure Unknown is not shown in stacked charts (defensive in case pivot includes it)
    if "Unknown" in pivot_df.columns:
        plot_df = pivot_df.drop(columns=["Unknown"])
    else:
        plot_df = pivot_df
    plot_df.plot(kind="bar", stacked=True, color=sns.color_palette(palette, n_colors=len(plot_df.columns)), ax=ax)
    ax.set_ylabel("Number of Species")
    ax.set_xlabel("Biological Category")
    ax.set_title("Conservation Status by Category (Sorted by Total)")
    ax.legend(title="Conservation Status", bbox_to_anchor=(1.05, 1), loc="upper left")
    sns.despine()
    plt.tight_layout()
    return fig, ax

