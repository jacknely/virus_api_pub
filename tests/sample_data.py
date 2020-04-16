from datetime import datetime


def generate_sample_data():
    data = []
    for num in range(6, 15):
        entry = {
            "date": datetime(1990, 4, num),
            "country": "country",
            "region": "region",
            "deaths": num,
            "recovered": num,
            "confirmed": num,
        }
        data.append(entry)
    return data
