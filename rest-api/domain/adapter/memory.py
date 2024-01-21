from typing import Dict, List
from bson.objectid import ObjectId

from domain.model.member import Member, MemberAddress
from domain.port import (
    MemberRepository,
    MemberAddressRepository,
    MemberNotFound,
    MemberAddressNotFound
)

class MemberRepositoryInMemory(MemberRepository):
    def __init__(self, data: Dict[str, Member] = None):
        self.data: Dict[str, Member] = data or {}

    async def next_identity(self) -> str:
        return 'Member-'+str(ObjectId())

    async def from_id(self, id: str) -> Member:
        member = self.data.get(id, None)
        if member is None:
            raise MemberNotFound(f'User id: {id} not found')
        return member
    
    async def get_list(self) -> List[Member]:
        return list(self.data.values())

    async def save(self, entity: Member) -> str:
        self.data[entity.id] = entity
        return entity.id

class MemberAddressRepositoryInMemory(MemberAddressRepository):
    def __init__(self, data: Dict[str, MemberAddress] = None):
        self.data: Dict[str, MemberAddress] = data or {}
    
    async def next_identity(self) -> str:
        return 'Member-Addr-'+str(ObjectId())

    async def from_id(self, id:str) -> MemberAddress:
        member_address = self.data.get(id, None)
        if (member_address is None):
            raise MemberAddressNotFound(f'Address id: {id} not found')
        return member_address
    
    async def from_member_id(self, member_id: str) -> MemberAddress:
        member_address = None
        for key, value in self.data.items():
            if (value.member_id == member_id):
                member_address = value

        if (member_address is None):
            raise MemberAddressNotFound(f'Address of user: {member_id} not found')
        return member_address

    async def save(self, entity: MemberAddress) -> str:
        self.data[entity.id] = entity
        return entity.id
