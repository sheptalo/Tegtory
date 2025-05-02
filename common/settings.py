import os
from pathlib import Path

TAX_LIMIT: int = int(os.environ.get("TAX_LIMIT", 50000))
DEBUG: bool = os.environ.get("DEBUG") != "False"
FACTORY_NAME_LENGTH_LIMIT: int = int(os.environ.get("FACTORY_NAME_LIMIT", 20))
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "static"

HIRE_PRICE = 370
