from abc import abstractmethod
from typing import List
from domain.base.repository import RepositoryAbstract
from domain.model.member import Member

class MemberRepository(RepositoryAbstract[str, Member]):
    @abstractmethod
    async def next_identity(self) -> str:
        pass

    @abstractmethod
    async def from_id(self, id: str) -> Member:
        pass

    @abstractmethod
    async def get_list(self) -> List[Member]:
        pass

    @abstractmethod
    async def save(self, entity: Member) -> str:
        pass
