from aiogram import Router

from .contract import router as contract
from .main import router as main

router = Router()


router.include_routers(main, contract)

__all__ = ["router"]
