import os


class Config(object):
    SECRET_KEY = "XXXXXXXTYUIO"
    REDIS_URL = "redis://localhost:6379/0"


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    MONGO_URI = f"mongodb://localhost:27017/virus"


class DevCloudConfig(Config):
    DEBUG = True
    MONGODB_PASS = os.environ.get("MONGODB_PASS")
    MONGODB_USER = os.environ.get("MONGODB_USER")
    MONGO_URI = (
        f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}"
        f"@cluster0-f11fa.mongodb.net/virus?retryWrites=true&w=majority"
    )


class DevDockerConfig(Config):
    DEBUG = True
    MONGODB_HOST = os.environ.get("MONGODB_HOST")
    MONGO_URI = f"mongodb://{MONGODB_HOST}:27017/virus"


class TestConfig(Config):
    DEBUG = True
    MONGO_URI = f"mongodb://localhost:27017/test"
