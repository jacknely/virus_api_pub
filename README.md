![Docker Image CI](https://github.com/jacknely/virus_api/workflows/Docker%20Image%20CI/badge.svg)
![Python package](https://github.com/jacknely/virus_api/workflows/Python%20package/badge.svg)
![Python application](https://github.com/jacknely/virus_api/workflows/Python%20application/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# :face_with_thermometer: Virus API
An endpoint for Covid-19 statistics. Made with Flask and MongoDB.

## Requirements
- Python 3.6 to 3.8
- Docker
- Flask
- Flask-restful
- Pandas
- PyMongo
- Pytest

All requirements are installed from requirements.txt during docker container build.

## Build and Run
### Option 1: Docker Compose
Execute the following code in root directory of application
```
$ docker-compose build
$ docker-compose up
```


### Option 2: Docker Image
To build image:
```
$ docker build -t virus_api .
```

To run image in container:
```
$ docker run -v $(pwd):/opt -p 5001:5001 --rm virus_api
```
Ensure commands are executed in app root directory


## Usage
Make sure that the application is running before executing any of the below commands:

### Update
To update database with latest data from Johns Hopkins CSSE, navigate to:
```
localhost:5001/update
```
A message will be displayed on successful import of new data.

### Status
To get the current global death, confirmed and recovered statistic's, navigate to the below:
```
localhost:5001/status

```
### Country Status
To get status by country, enter the below to browser:
```
localhost:5001/status/<country>
```
The following is a response example:
```
{
  "Country": "US",
  "Date": "08 Apr 2020",
  "History": {
    "03/04/2020": {
      "confirmed": 275586,
      "deaths": 7087,
      "recovered": 9707
    },
    "04/04/2020": {
      "confirmed": 308850,
      "deaths": 8407,
      "recovered": 14652
    },
    "05/04/2020": {
      "confirmed": 337072,
      "deaths": 9619,
      "recovered": 17448
    },
    "06/04/2020": {
      "confirmed": 366667,
      "deaths": 10783,
      "recovered": 19581
    },
    "07/04/2020": {
      "confirmed": 396223,
      "deaths": 12722,
      "recovered": 21763
    }
  },
  "Today": {
    "confirmed": 429052,
    "deaths": 14695,
    "recovered": 23559
  }
}
```
### Countries
This endpoint returns a response with infection statistics from all countries.
```
localhost:5001/status/countries
```

## Swagger
For an overview of API endpoints, navigate to:
```
localhost:5001/api/spec.html
```


