from aiogram import Router

from .lottery import router as lottery
from .market import router as market
from .titles import router as titles
from .donate import router as donate
from .exchange import router as exchange
from .items import router as items
from .leaderboard import router as leaderboard

router = Router()

router.include_router(lottery)
router.include_router(market)
router.include_router(titles)
router.include_router(donate)
router.include_router(exchange)
router.include_router(items)
router.include_router(leaderboard)
