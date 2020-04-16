from app import mongo
from app.file import File
from flask_restful import Resource
from flask_restful_swagger import swagger


class Update(Resource):
    @swagger.operation(
        notes="This endpoint updates the database "
        "with data from John Hopkins CSSE"
    )
    def get(self):
        file = File()
        virus_data = file.get_virus_data()
        mongo.update_virus_db(virus_data)

        return {"message": "Virus database update completed successfully"}


class Test(Resource):
    @swagger.operation(notes="This is a test endpoint for debugging")
    def get(self):
        return {"message": "This is a test endpoint for debugging"}
