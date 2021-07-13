import os
import sys
import logging

from loguru import logger
from starlette.config import Config


env_file = os.getenv("ENV_FILE", "live.env")

config = Config(env_file=env_file)

MONGO_HOST: str = config("MONGO_HOST", default="yara_db")
MONGO_PORT: str = config("MONGO_PORT", default="27017")
MONGO_URL: str = config("MONGO_URL", default=f"mongodb://{MONGO_HOST}:{MONGO_PORT}")
DB_NAME: str = config("DB_NAME", default="yara_db")

