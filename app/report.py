from datetime import timedelta

import pandas as pd
from app import mongo


class Report:
    """
    Report is wrapper for the virus class
    which takes virus data and processes it (mainly
    using pandas) to a format for the user to consume
    """

    def __init__(self, country):
        self.country = country

    @classmethod
    def get_global_status(cls):
        """
        returns a current global total for deaths, recovered
        and confirmed for Covid_19
        :return: dict of global totals
        """
        results = mongo.get_global_by_date()
        results_df = (
            pd.DataFrame(results)
            .drop(columns=["region", "date", "country"])
            .sum()
        )
        results_dict = results_df.to_dict()

        return results_dict

    def get_infection_status(self) -> dict:
        """
        returns a dict containing the deaths, confirmed
        and recovered stats for the instantiated country
        :return: dict of stats
        """
        date = mongo.get_latest_date
        results = mongo.find_by_date_range(self.country, old_date=date)
        results_df = (
            pd.DataFrame(results)
            .drop(columns=["region", "date", "country"])
            .sum()
        )
        results_dict = results_df.to_dict()

        return results_dict

    @staticmethod
    def get_infection_status_all_countries() -> dict:
        """
        returns dict for each country in db
        with virus stats
        :return: dict of stats
        """
        results = mongo.get_global_by_date()
        results_df = pd.DataFrame(results)
        results_df.index = results_df["country"]
        results_df = results_df.drop(columns=["region", "date", "country"])
        results_df_grouped = results_df.groupby(results_df.index).sum()
        results_dict = results_df_grouped.to_dict("index")

        return results_dict

    def get_infection_history(self, days: int) -> dict:
        """
        returns a dict of country infection statistics
        for a given number of days
        :param days: number of days as int
        :return: dict of stats
        """
        day_n = mongo.get_latest_date - timedelta(1)
        five_days_before_n = day_n - timedelta(days - 1)
        results = mongo.find_by_date_range(
            self.country, old_date=five_days_before_n, young_date=day_n
        )
        results_df = pd.DataFrame(results).drop(columns=["region"])
        results_df.index = results_df["date"].dt.strftime("%d/%m/%Y")
        results_df_grouped = (
            results_df.groupby(results_df.index)
            .sum()
            .sort_values("date", ascending=True)
        )
        results_dict = results_df_grouped.to_dict("index")

        return results_dict
