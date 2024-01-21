from abc import abstractmethod
from domain.base.repository import RepositoryAbstract
from domain.model.member import MemberAddress

class MemberAddressRepository(RepositoryAbstract[str, MemberAddress]):
    @abstractmethod
    async def next_identity(self) -> str:
        pass

    @abstractmethod
    async def from_id(self, id: str) -> MemberAddress:
        pass

    @abstractmethod
    async def from_member_id(self, member_id: str) -> MemberAddress:
        pass

    @abstractmethod
    async def save(self, entity: MemberAddress):
        pass
