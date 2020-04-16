from app import api, create_app
from resources.file import Test, Update
from resources.report import CountryStatus, Status, StatusCountries

api.add_resource(Update, "/update")
api.add_resource(Test, "/test")

api.add_resource(CountryStatus, "/status/<string:country>")
api.add_resource(Status, "/status")
api.add_resource(StatusCountries, "/status/countries")


if __name__ == "__main__":
    app = create_app("config.DevConfig")
    app.run(debug=True)
