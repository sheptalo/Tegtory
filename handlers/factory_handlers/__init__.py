from aiogram import Router
from .tax import router as tax
from .upgrade import router as upgrade
from .work_yourself import router as yourself
from .workers import router as workers
from .ecology import router as ecology
from .create_factory import router as create
from .rename_factory import router as rename
from .reset_factory import router as reset

router = Router()

router.include_router(tax)
router.include_router(upgrade)
router.include_router(workers)
router.include_router(ecology)
router.include_router(create)
router.include_router(rename)
router.include_router(reset)
router.include_router(yourself)

__all__ = [
    router,
]
