from typing import Optional
from domain.base.singleton import Singleton


class Registry(metaclass=Singleton):
    def __init__(self):
        from domain.model.member.repository import MemberRepository, MemberAddressRepository
        self.member: Optional[MemberRepository] = None
        self.member_adress: Optional[MemberAddressRepository] = None
