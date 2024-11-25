from aiogram.fsm.state import StatesGroup, State


class CreateFactory(StatesGroup):
    new_factory_name = State()


class FactoryName(StatesGroup):
    new_factory_name = State()
    confirm = State()


class DeleteFactory(StatesGroup):
    user_id = State()


class DeleteFactoryGroup(StatesGroup):
    user_id = State()


class SellStolar(StatesGroup):
    stolar_on_sell = State()
    money_buy = State()
    confirm = State()


class FindFactory(StatesGroup):
    name = State()


class SellStock(StatesGroup):
    stock = State()


class ChangeNick(StatesGroup):
    new_nickname = State()
