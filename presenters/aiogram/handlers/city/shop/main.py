from typing import TYPE_CHECKING

from aiogram import F, Router, types

from domain.queries.shop import ListShopQuery, ShopQuery
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


@router.callback_query(F.data.startswith(f"{CityCB.shop}:"))
async def shop_page(
    call: types.CallbackQuery, query_executor: QueryExecutor
) -> None:
    shop_data = await query_executor.ask(
        ShopQuery(title=call.data.split(":")[1])
    )
    if isinstance(shop_data, Success):
        shop: Shop = shop_data.data
        markup = kb.get_shop_markup(shop)
        await call.message.edit_caption(
            caption=msg.specific_shop.format(
                shop.title, shop.description, shop.delivery_required
            ),
            reply_markup=markup,
        )
