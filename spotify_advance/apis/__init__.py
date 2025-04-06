import os
from logging import getLogger

from yaml import safe_load

logger = getLogger("spotify_advance.api")
logger.setLevel("INFO")


def get_client_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "conf.yaml")
    with open(config_path, "r") as f:
        return safe_load(f)["spotify"]


def get_mongodb_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "conf.yaml")
    with open(config_path, "r") as f:
        return safe_load(f)["mongodb"]


client_data: dict[str, str] = get_client_data()
mongodb_data: dict[str, str] = get_mongodb_data()
