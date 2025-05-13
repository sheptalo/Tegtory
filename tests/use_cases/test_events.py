from typing import Any

import pytest

from domain.events import EventType
from domain.events.subscribe import on_event
from domain.use_cases.base import EventBased


class TestEventBased(EventBased):
    @on_event(EventType.SubtractMoney)
    def sub_money(self, event: Any) -> None:
        pass


@pytest.mark.asyncio
async def test_on_event() -> None:
    decorator = on_event(EventType.SubtractMoney)
    func = decorator(lambda: None)

    assert hasattr(func, "__event__")


@pytest.mark.asyncio
async def test_event_based_get_children() -> None:
    assert TestEventBased in EventBased.__subclasses__()
    assert len(TestEventBased.get_subscribers()) == 1
