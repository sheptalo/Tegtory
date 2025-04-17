from enum import EnumType


class EventType(EnumType):
    StartFactory = "start_factory"
    EndFactoryWork = "end_factory_work"
    UpgradeFactory = "start_upgrade_factory"
    SubtractMoney = "subtract_money"
