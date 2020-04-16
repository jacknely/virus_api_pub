import pytest
from app import create_app, mongo
from app.report import Report
from tests.sample_data import generate_sample_data


@pytest.fixture(scope="session")
def client():
    app = create_app("config.TestConfig")
    test_client = app.test_client()
    yield test_client


class TestApp:
    def setup_method(self, client):
        sample_data = generate_sample_data()
        mongo.db.location.insert_many(sample_data)

    def teardown_method(self, client):
        mongo.db.drop_collection("location")

    def test_get_infection_status(self, client):
        test_report = Report("country")
        status = test_report.get_infection_status()

        assert status["confirmed"] == 14

    def test_get_infection_history(self, client):
        test_report = Report("country")
        history = test_report.get_infection_history(3)

        assert len(history) == 3

    def test_get_global_status(self, client):
        global_report = Report.get_global_status()

        assert global_report["deaths"] == 14

    def test_ge(self, client):
        test_report = Report("country")
        all_countries = test_report.get_infection_status_all_countries()

        assert all_countries["country"]["deaths"] == 14


if __name__ == "__main__":
    pytest.main()
