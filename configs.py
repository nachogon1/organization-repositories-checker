import os
import sys
import logging

from starlette.config import Config


env_file = os.getenv("ENV_FILE", "develop.env")

config = Config(env_file=env_file)

MONGO_HOST: str = config("MONGO_HOST", default="yara_db")
MONGO_PORT: str = config("MONGO_PORT", default="27017")
MONGO_URL: str = config("MONGO_URL", default=f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
DB_NAME: str = config("DB_NAME", default="yara_db")
GITHUB_ORGANIZATION: str = config("GITHUB_ORGANIZATION", default="")
GITHUB_TOKEN: str = config("GITHUB_TOKEN", default="")
APP_HOST: str = config("APP_HOST", default="0.0.0.0")
APP_PORT: str = config("APP_PORT", default="8000")
APP_URL: str = config("APP_URL", default=f"http://{APP_HOST}:{APP_PORT}")