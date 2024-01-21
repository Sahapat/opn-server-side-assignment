from typing import TypeVar, Generic
from abc import abstractmethod

IdType = TypeVar('IdType')
EntityType = TypeVar('EntityType')


class EntityNotFound(Exception):
    pass


class RepositoryAbstract(Generic[IdType, EntityType]):
    @abstractmethod
    async def next_identity(self) -> IdType:
        pass

    @abstractmethod
    async def from_id(self, id: IdType) -> EntityType:
        pass

    @abstractmethod
    async def save(self, entity: EntityType):
        pass

