from collections import defaultdict
import json
import logging
from pathlib import Path
import typing as t

import numpy as np
import pandas as pd


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
                [link.split("/")[-1] for link in character["crosslinks"]]
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
