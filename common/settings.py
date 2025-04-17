import os
from pathlib import Path

from domain.entity.factory import Product

TAX_LIMIT: int = int(os.environ.get("TAX_LIMIT", 50000))
DEBUG: bool = os.environ.get("DEBUG") != "False"
FACTORY_NAME_LENGTH_LIMIT: int = os.environ.get(
    "FACTORY_NAME_LENGTH_LIMIT", 20
)
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "static"

DEFAULT_AVAILABLE_PRODUCTS: list[Product] = [
    Product(
        name="Доски",
        price_multiply=0.8,
        time_to_create=100,
        amount_multiply=0.8,
    ),
    Product(
        name="Кирпичи",
        price_multiply=0.9,
        time_to_create=160,
        amount_multiply=0.6,
    ),
    Product(
        name="Уголь",
        price_multiply=0.6,
        time_to_create=30,
        amount_multiply=1.2,
    ),
]
