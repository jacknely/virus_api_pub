from app import mongo
from app.report import Report
from flask import jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger


class CountryStatus(Resource):
    @swagger.operation(
        notes="This endpoint returns the status for a requested country"
    )
    def get(self, country):
        report = Report(country)
        status = {
            "Date": mongo.get_latest_date.strftime("%d %b %Y"),
            "Country": country,
            "Today": report.get_infection_status(),
            "History": report.get_infection_history(5),
        }

        return jsonify(status)


class Status(Resource):
    @swagger.operation(
        notes="This endpoint returns the global death, "
        "recovered and confirmed totals"
    )
    def get(self):
        results = Report.get_global_status()

        return results


class StatusCountries(Resource):
    @swagger.operation(
        notes="This endpoint returns the current death, "
        "recovered and confirmed total for each country"
    )
    def get(self):
        results = Report.get_infection_status_all_countries()

        return results
