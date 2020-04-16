from pathlib import Path

import pytest
from app.file import File


class TestFile:
    def setup_method(self):
        self.test_file = File()

    def test_map_url(self):
        test_url = self.test_file.map_url("deaths")

        assert (
            test_url == "https://raw.githubusercontent.com/"
            "CSSEGISandData/COVID-19/master/"
            "csse_covid_19_data/"
            "csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
        )

    def test_parse_csv_by_category(self, monkeypatch):
        monkeypatch.setattr(
            self.test_file,
            "map_url",
            lambda x: f"{Path(__file__).parent.parent}/test_data.csv",
        )
        parsed_file = self.test_file.parse_csv_by_category("deaths")

        assert len(parsed_file) > 1

    def test_get_virus_data(self, monkeypatch):
        monkeypatch.setattr(
            self.test_file,
            "map_url",
            lambda x: f"{Path(__file__).parent.parent}/test_data.csv",
        )
        virus_data = self.test_file.get_virus_data()

        assert virus_data.shape[1] == 6


if __name__ == "__main__":
    pytest.main()
