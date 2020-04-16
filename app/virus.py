from datetime import datetime

import pandas as pd
from flask_pymongo import PyMongo


class VirusMongo(PyMongo):
    """
    Additional functionality to database management
    tools. VirusMongo inherits from parent class
    PyMongo.
    """

    def update_virus_db(self, virus_data: pd.DataFrame) -> None:
        """
        Updates database with values from a given DataFrame.
        Will exclude dates that are already writen to database
        :param virus_data: DataFrame of new values
        """
        search_results = self.db.location.find()
        dates_in_db = [
            search_result["date"] for search_result in search_results
        ]
        for i, row in virus_data.iterrows():
            date = datetime.strptime(row["date"], "%m/%d/%y")
            if date not in dates_in_db:
                data_entry = {
                    "date": date,
                    "country": row["Country/Region"],
                    "region": row["Province/State"],
                    "deaths": row["deaths"],
                    "recovered": row["recovered"],
                    "confirmed": row["confirmed"],
                }
                self.db.location.insert_one(data_entry)

    def find_by_country(self, country: str = None) -> list:
        """
        returns a list of stats in dict by a given
        country. If no country given then all will
        be returned
        :param country: country as str
        :return: list of dicts
        """
        if country:
            country = {"country": country}
        search_results = self.db.location.find(country)
        results_refactored = [
            self.__to_dict(result) for result in search_results
        ]

        return results_refactored

    @property
    def get_latest_date(self) -> datetime:
        """
        returns the most recently synced date
        from database
        :return: datetime
        """
        results = self.db.location.find()
        saved_dates = {result["date"] for result in results}

        return max(saved_dates)

    def find_by_date_range(
        self,
        country: str,
        young_date: datetime = None,
        old_date: datetime = None,
    ) -> list:
        """
        returns a filtered list of dicts by country filtered
        by a given date range.
        :param young_date: datetime
        :param old_date: datetime
        :param country: str
        :return: list of dicts
        """
        young_date = young_date or self.get_latest_date
        old_date = old_date or datetime(1970, 1, 1)
        search_results = self.db.location.find(
            {
                "date": {"$gte": old_date, "$lte": young_date},
                "country": country,
            }
        )
        results_refactored = [
            self.__to_dict(result) for result in search_results
        ]

        return results_refactored

    @staticmethod
    def __to_dict(item: iter) -> dict:
        """
        converts an iterable from search results
        to a dictionary
        :param item: iterable
        :return: dict
        """
        _dict = {
            "country": item["country"],
            "date": item["date"],
            "region": item["region"],
            "deaths": item["deaths"],
            "recovered": item["recovered"],
            "confirmed": item["confirmed"],
        }
        return _dict

    def get_global_by_date(self, date: datetime = None) -> list:
        """
        returns the death, confirmed, and recovered
        total for all countries on a given date
        :param date: datetime
        :return: dict of stats
        """
        date = date or self.get_latest_date
        search_results = self.db.location.find({"date": {"$gte": date}})
        results_refactored = [
            self.__to_dict(result) for result in search_results
        ]

        return results_refactored
