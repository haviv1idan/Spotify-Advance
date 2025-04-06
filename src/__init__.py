import logging
from typing import Final

from yaml import safe_load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.info("Logging is set up.")


def read_client_data() -> dict[str, str]:
    with open('conf.yaml', 'r') as f:
        data = safe_load(f)
        return data


client_data: dict[str, str] = read_client_data()
CLIENT_ID: Final[str] = client_data.get('client_id')
CLIENT_SECRET: Final[str] = client_data.get('client_secret')
REDIRECT_URI: Final[str] = client_data.get('redirect_uri')
