from datetime import datetime

import pandas as pd
import pytest
from app import create_app, mongo
from tests.sample_data import generate_sample_data


@pytest.fixture(scope="module")
def client():
    app = create_app("config.TestConfig")
    test_client = app.test_client()
    yield test_client


@pytest.fixture
def test_entry():
    test_entry = {
        "date": datetime(1990, 4, 4),
        "country": "country",
        "region": "region",
        "deaths": "deaths",
        "recovered": "recovered",
        "confirmed": "confirmed",
    }
    return test_entry


class TestApp:
    def teardown_method(self, client):
        mongo.db.drop_collection("location")

    def test_db(self, test_entry, client):
        mongo.db.location.insert_one(test_entry)

        assert mongo.db.name == "test"
        assert mongo.db.location.count_documents({}) == 1

        test_results = mongo.db.location.find_one(
            {"date": datetime(1990, 4, 4)}
        )
        mongo.db.location.delete_one(test_results)

        assert mongo.db.location.count_documents({}) == 0

    def test_find_by_country(self, test_entry, client):
        mongo.db.location.insert_one(test_entry)
        test_result = mongo.find_by_country("country")

        assert len(test_result) == 1

    def test_update_virus_db(self, client):
        assert mongo.db.location.count_documents({}) == 0
        test_import = {
            "date": "04/04/90",
            "Country/Region": "country",
            "Province/State": "region",
            "deaths": "deaths",
            "recovered": "recovered",
            "confirmed": "confirmed",
        }
        test_data = pd.DataFrame([test_import], columns=test_import.keys())
        mongo.update_virus_db(test_data)

        assert mongo.db.location.count_documents({}) == 1

    def test_get_latest_date(self, test_entry, client):
        mongo.db.location.insert_one(test_entry)
        test_date = mongo.get_latest_date

        assert test_date == datetime(1990, 4, 4)

    def test_find_by_date_range(self, client):
        sample_data = generate_sample_data()
        mongo.db.location.insert_many(sample_data)
        test_query = mongo.find_by_date_range("country")

        assert len(test_query) == 9

    def test_get_global_by_date(self, client):
        sample_data = generate_sample_data()
        mongo.db.location.insert_many(sample_data)
        test_query = mongo.get_global_by_date()

        assert len(test_query) == 1


if __name__ == "__main__":
    pytest.main()
