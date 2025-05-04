from aiogram import Router

from .city import router as city
from .factory import router as factory
from .start import router as start

router = Router()
router.include_routers(city, factory, start)

__all__ = ["router"]
