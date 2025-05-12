from typing import TYPE_CHECKING

from aiogram import F, Router, types

from domain.queries.shop import ListShopQuery
from domain.results import Failure, Success
from infrastructure import QueryExecutor
from presenters.aiogram.kb import CityCB
from presenters.aiogram.kb import shop as kb
from presenters.aiogram.messages import shop as msg

if TYPE_CHECKING:
    from domain.entities import Shop

router = Router()


@router.callback_query(F.data == CityCB.shop)
async def shop_list(
    call: types.CallbackQuery, query_executor: QueryExecutor
) -> None:
    shops: Success[list[Shop]] | Failure = await query_executor.ask(
        ListShopQuery()
    )
    if isinstance(shops, Success):
        markup = kb.get_shop_list_markup(shops.data)
        await call.message.edit_caption(
            caption=msg.shop_list, reply_markup=markup
        )
