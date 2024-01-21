from domain.registry import Registry
from domain.adapter.memory import MemberRepositoryInMemory, MemberAddressRepositoryInMemory

def inject():
    Registry().member = MemberRepositoryInMemory()
    Registry().member_adress = MemberAddressRepositoryInMemory()
