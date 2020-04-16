from pathlib import Path
from unittest.mock import patch

import pytest
from app import create_app, mongo
from run import api
from tests.sample_data import generate_sample_data


@pytest.fixture(scope="session")
def client():
    app = create_app("config.TestConfig")
    test_client = app.test_client()
    yield test_client


class TestEndpoints:
    def setup_method(self):
        sample_data = generate_sample_data()
        mongo.db.location.insert_many(sample_data)

    def teardown_method(self):
        mongo.db.drop_collection("location")

    def test_get_test(self, client):
        response = client.get("/test")

        assert response.status_code == 200
        assert b"This is a test endpoint for debugging" in response.data

    def test_update(self, client):
        with patch(
            "app.file.File.map_url",
            return_value=f"{Path(__file__).parent.parent}/test_data.csv",
        ):
            response = client.get("/update")

            assert response.status_code == 200
            assert b"successfully" in response.data

    def test_get_country_status(self, client):
        response = client.get("/status/country")

        assert response.status_code == 200
        assert b"country" in response.data

    def test_get_status(self, client):
        response = client.get("/status")

        assert response.status_code == 200
        assert b"14" in response.data

    def test_get_status_countries(self, client):
        response = client.get("/status/countries")

        assert response.status_code == 200
        assert b"14" in response.data


if __name__ == "__main__":
    pytest.main()
