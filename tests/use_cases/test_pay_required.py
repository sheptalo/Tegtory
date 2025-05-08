import pytest

from common.exceptions import AppException
from domain.use_cases.commands.pay_required import pay_required


def test_pay_required_failure_exec() -> None:
    cls = type("", (), {})
    with pytest.raises(AppException):
        pay_required(cls)
