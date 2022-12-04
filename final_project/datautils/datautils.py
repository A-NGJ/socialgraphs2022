from collections import defaultdict
import json
import logging
from pathlib import Path
import typing as t

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class Loader:
    def __init__(self):
        self.data = []

    def _check_data(self):
        if len(self.data) == 0:
            raise ReferenceError("data is empty, did you run load()?")

    def load(self, path: str):
        """Loads characters from json files"""

        files = sorted(Path(path).glob("*.json"))
        if len(files) == 0:
            raise EnvironmentError(f"no files were found in {path}")

        for file_ in files:
            try:
                with open(file_, "r", encoding="utf=8") as rfile:
                    self.data.append(json.load(rfile))
            except EnvironmentError:
                logging.warning("%s could not be opened", file_)

    def get_sidebar_summary(self) -> t.Tuple[dict]:
        """
        Get summary of all atrributes in sidebar

        Returns
        -------
        tuple :
            summary, count_categories, count_attr
        """

        self._check_data()

        summary = defaultdict(set)
        count_side_bars = defaultdict(int)
        count_attr = defaultdict(int)

        for character in self.data:
            for side_bar in character["side_bars"]:
                count_side_bars[side_bar["name"]] += 1
                for attr in side_bar["attributes"]:
                    summary[side_bar["name"]].add(attr["name"])
                    count_attr[attr["name"]] += 1

        return summary, count_side_bars, count_attr

    def drop(self):
        """Drops data from loader"""
        self.data = []

    def to_dataframe(self) -> pd.DataFrame:
        """Returns dataframe with characters data"""

        data_dict = {
            "Name": [],
            "DisplayName": [],
            "Content": [],
            "Crosslinks": [],
            "Species": [],
            "Gender": [],
            "Affiliation(s)": [],
            "Homeworld": [],
            "Died": [],
        }

        self._check_data()

        for character in self.data:
            data_dict["Name"].append(character.get("name"))
            data_dict["DisplayName"].append(character.get("display_name"))
            data_dict["Content"].append(character.get("content"))
            data_dict["Crosslinks"].append(
                [link.replace("/wiki/", "") for link in character["crosslinks"]]
            )

            attributes = {"Species", "Gender", "Affiliation(s)", "Homeworld", "Died"}

            for side_bar in character["side_bars"]:
                for attr in side_bar["attributes"]:
                    if attr["name"] in attributes:
                        if attr["name"] in ["Affiliation(s)", "Died"]:
                            data_dict[attr["name"]].append(attr.get("values", np.nan))
                        else:
                            values = attr.get("values")
                            if values:
                                data_dict[attr["name"]].append(values[0])
                            else:
                                data_dict[attr["name"]].append(np.nan)
                        attributes.remove(attr["name"])

            for attr in attributes:
                data_dict[attr].append(np.nan)

        return pd.DataFrame(data_dict)


<<<<<<< HEAD
def find_rows_with(
    name: str, df: pd.DataFrame, *, lookup_column: str, match_column: str
) -> t.List[str]:

    matching_rows = []

    for _, row in df.iterrows():
        # iterate over records
        for element in row[lookup_column]:
            if element == name:
                # append only characters which have crosslink to one of the episodes
                matching_rows.append(row[match_column])
                break
    return matching_rows
=======


def plot_distribution(
    data: t.Iterable[float], *, fig: plt.Figure, ax: plt.Axes, **kwargs
):
    """
    Plots distribution of given data and marks its average, 10th and 90th percentile,

    Parameters
    ----------
    data :
        Data for the distribution plot
    ax :
        matplotlib axes to plot data on
    title : Optional[str]
    xlabel : Optional[str]
    ylabel : Optional[str]
    tag : Optional[str]
        Tag to be displayed in the legend
    mean_color : Optional[str]
        Color of mean line
    percentile10_color : Optional[str]
        Color of 10th percentile line
    percentile90_color : Optional[str]
        Color of 90th percentile line
    """
    percentile10 = np.percentile(data, 10)
    percentile90 = np.percentile(data, 90)
    mean = np.mean(data)

    ax = sns.histplot(data, ax=ax, label=kwargs.get("tag", "distribution"))
    ax.axvline(
        mean,
        linewidth=2,
        color=kwargs.get("mean_color", "navy"),
        label=f"Average sentiment {kwargs.get('tag', '')}: {mean:.2f}",
    )
    ax.set_xlabel(kwargs.get("xlabel", ""), fontsize=14)
    ax.set_ylabel(kwargs.get("ylabel", ""), fontsize=14)
    ax.set_title(kwargs.get("title", ""), fontsize=16)

    ax.axvline(
        percentile10,
        ymax=0.55,
        linestyle=":",
        linewidth=3,
        color=kwargs.get("percentile10_color", "red"),
        label=f"$10^{{th}}$ percentile {kwargs.get('tag', '')}: {percentile10:.2f}",
    )
    ax.axvline(
        percentile90,
        ymax=0.55,
        linestyle=":",
        linewidth=3,
        color=kwargs.get("percentile90_color", "darkorange"),
        label=f"$90^{{th}}$ percentile {kwargs.get('tag', '')}: {percentile90:.2f}",
    )

    handles, labels = ax.get_legend_handles_labels()
    # remove duplicates while preserving the order
    seen = set()
    seen_add = seen.add
    new_labels = []
    new_handles = []
    for i, label in enumerate(labels):
        if label not in seen:
            new_labels.append(label)
            new_handles.append(handles[i])
            seen_add(label)

    ax.legend(new_handles, new_labels)

    ax.grid()
    fig.tight_layout()

    return fig, ax


def remove_duplicates(seq: t.Iterable):
    seen = set()
    seen_add = set.add
    return [item for item in seq if not (item in seen or seen_add(item))]
>>>>>>> 2f98d5113a7e5ef75e2a4fd5aff95aad7cd949a4
