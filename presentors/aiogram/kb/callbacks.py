from enum import EnumType


class CityCB(EnumType):
    back = "city"
    shop = "city__shop"
    choose_amount = "city_shop__choose_amount"
    sign_contract = "city_shop__sign_contract"
    leaderboard = "city__leaderboard"
    trading_companies = "city__trading_companies"


class FactoryCB(EnumType):
    back = "factory"
    create = "factory__create"
    choose_time = "factory__choose_time"
    work_yourself = "factory__work_yourself"
    start = "factory__start"
    upgrade = "factory__upgrade"
    upgrade_conf = "factory__upgrade:pay"
    tax = "factory__tax"
    pay_tax = "factory__tax:pay"
    storage = "factory__storage"
    upgrade_storage = "factory__storage:pay"
    workers = "factory__workers"
    hire = "factory__workers:pay"


class OtherCB(EnumType):
    working_on = "other__working_on"
    subscribe = "other__subscribe"
