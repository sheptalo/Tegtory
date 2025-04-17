import pytest


@pytest.mark.asyncio
async def test_create_factory(factory_repository, mock_factory, uc_factory):
    await uc_factory.create(mock_factory)

    factory_repository.create.assert_called_with(mock_factory)


@pytest.mark.asyncio
async def test_upgrade_factory(
    factory_repository, mock_factory, uc_factory, mock_user
):
    await uc_factory.upgrade(mock_factory, mock_user)
    mock_factory.level += 1
    factory_repository.update.assert_called_with(mock_factory)


@pytest.mark.asyncio
async def test_pay_tax(
    factory_repository, mock_factory, mock_user, uc_factory
):
    result = await uc_factory.pay_tax(mock_factory, mock_user)
    mock_factory.tax = 0
    factory_repository.update.assert_called_with(mock_factory)
    assert result == mock_factory


@pytest.mark.asyncio
async def test_hire(factory_repository, mock_factory, uc_factory, mock_user):
    mock_user.money = 10000
    result = await uc_factory.hire(mock_factory, mock_user)
    mock_factory.workers += 1
    factory_repository.update.assert_called_with(mock_factory)
    assert result == mock_factory
