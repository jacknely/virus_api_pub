import pandas as pd


class File:
    """
    File operations for importing
    data into application
    """

    @staticmethod
    def map_url(category: str) -> str:
        """
        returns a url for virus data based on a given
        category
        :param category: str (deaths, recovered, confirmed)
        :return: url of virus data as str
        """
        source = {
            "deaths": "https://raw.githubusercontent.com"
            "/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
            "csse_covid_19_time_series/"
            "time_series_covid19_deaths_global.csv",
            "confirmed": "https://raw.githubusercontent.com"
            "/CSSEGISandData/COVID-19/master/csse_covid_19_data/"
            "csse_covid_19_time_series/"
            "time_series_covid19_confirmed_global.csv",
            "recovered": "https://raw.githubusercontent.com/"
            "CSSEGISandData/COVID-19/master/csse_covid_19_data/"
            "csse_covid_19_time_series/"
            "time_series_covid19_recovered_global.csv",
        }
        return source.get(category)

    def parse_csv_by_category(self, category: str) -> pd.DataFrame:
        """
        returns a flattened data-frame of virus data for
        a given category
        :param category: category as str (eg deaths)
        :return: flatten data-frame of category data
        """
        url = self.map_url(category)
        raw_data = pd.read_csv(url, header=0)
        raw_data_modified = raw_data.drop(["Lat", "Long"], axis=1)
        raw_data_indexed = raw_data_modified.set_index(
            ["Country/Region", "Province/State"]
        )
        flattened_data = (
            raw_data_indexed.stack().reset_index()
        )  # this flattens a multilevel DataFrame
        flattened_data.rename(
            columns={"level_2": "date", 0: category}, inplace=True
        )
        return flattened_data

    def get_virus_data(self) -> pd.DataFrame:
        """
        Returns a list of DataFrames containing
        imported data for each category
        :return: list of DataFrames
        """
        categories = ["confirmed", "deaths", "recovered"]
        data_sets = []
        for category in categories:
            data = self.parse_csv_by_category(category)
            data_sets.append(data)
        virus_data = self.__merge_category_data(data_sets)
        return virus_data

    @staticmethod
    def __merge_category_data(data_sets: list) -> pd.DataFrame:
        """
        merges the deaths, recovered and confirmed
        data into a single DataFrame
        :param data_sets: list of DataFrames
        :return: DataFrame of merged results
        """
        confirmed, deaths, recovered = tuple(data_sets)
        merge_settings = {
            "how": "inner",
            "on": ["Country/Region", "Province/State", "date"],
        }
        confirmed_deaths = confirmed.merge(deaths, **merge_settings)
        confirmed_deaths_recovered = confirmed_deaths.merge(
            recovered, **merge_settings
        )
        return confirmed_deaths_recovered
