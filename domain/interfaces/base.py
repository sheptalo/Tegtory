from typing import Protocol, TypeVar

T = TypeVar("T")


class ICrudRepository(Protocol[T]):
    def all(self) -> list[T]:
        pass

    def get(self, item_id: int) -> T | None:
        pass

    def create(self, item: T) -> T:
        pass

    def update(self, item: T) -> T:
        pass

    def delete(self, item_id: int) -> None:
        pass
