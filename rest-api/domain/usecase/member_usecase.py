import hashlib
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, EmailStr
from domain.model.member import Member, MemberAddress, GenderEnum
from domain.model.member.repository import MemberAddressNotFound
from domain.registry import Registry 
from .exception import PasswordMismatch, IncorrectPassword, AgeValidationError

class RegisterMemberAddress(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class RegisterMember(BaseModel):
    email: EmailStr
    name: str
    date_of_birth: date
    gender: GenderEnum
    is_subscribe_to_news_sletter: bool
    password: str
    confirm_password: str
    address: RegisterMemberAddress

class UpdateMemberInfo(BaseModel):
    date_of_birth: date
    gender: GenderEnum
    is_subscribe_to_news_sletter: bool

class UpdateAddressInfo(RegisterMemberAddress):
    pass

class MemberProfile(BaseModel):
    id: str
    email: str
    name: str
    age: int
    gender: GenderEnum
    is_subscribe_to_news_sletter: bool
    address: Optional[MemberAddress]

class MemberMetaInfo(BaseModel):
    id: str
    email: str
    name: str
    age: int
    gender: GenderEnum

def hash_password(password: str):
    check_password = password[::-1]
    return hashlib.sha256(check_password.encode()).hexdigest()

def calculate_age_from_date_of_birth(date_of_birth: date):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

def validate_age_policy(date_of_birth: date):
    age = calculate_age_from_date_of_birth(date_of_birth)
    return age < 6

async def register_member(register_member_info: RegisterMember) -> MemberProfile:
    if (register_member_info.password != register_member_info.confirm_password):
        raise PasswordMismatch('Password and confirm password does not match')

    member_repo = Registry().member
    member_address_repo = Registry().member_adress
    member_id: str = await member_repo.next_identity()
    address_id: str = await member_address_repo.next_identity()

    if validate_age_policy(register_member_info.date_of_birth):
        raise AgeValidationError('Not allow member which age less than 6')

    member_address = MemberAddress(
        id=address_id,
        member_id=member_id,
        city=register_member_info.address.city,
        street=register_member_info.address.street,
        state=register_member_info.address.state,
        postal_code=register_member_info.address.postal_code,
        country=register_member_info.address.country,
    )
    member = Member(
        id=member_id,
        address=address_id,
        name=register_member_info.name,
        email=register_member_info.email,
        gender=register_member_info.gender,
        date_of_birth=register_member_info.date_of_birth,
        password=hash_password(register_member_info.password),
        is_subscribe_to_news_sletter=register_member_info.is_subscribe_to_news_sletter
    )
    await member_repo.save(member)
    await member_address_repo.save(member_address)
    return MemberProfile(
        **member.model_dump(),
        age=calculate_age_from_date_of_birth(member.date_of_birth),
        address=member_address
    )

async def update_member_info(
    member_id: str,
    member_info: UpdateMemberInfo,
    address_info: UpdateAddressInfo
) -> MemberProfile:
    member_repo = Registry().member
    member_address_repo = Registry().member_adress

    if validate_age_policy(member_info.date_of_birth):
        raise AgeValidationError('Not allow member which age less than 6')

    member = await member_repo.from_id(member_id)
    member.date_of_birth = member_info.date_of_birth
    member.gender = member_info.gender
    member.is_subscribe_to_news_sletter = member_info.is_subscribe_to_news_sletter
    await member_repo.save(member)

    try:
        member_address = await member_address_repo.from_member_id(member_id)
    except MemberAddressNotFound:
        member_address = MemberAddress(id=member_address_repo.next_identity())
    member_address.city = address_info.city
    member_address.street = address_info.street
    member_address.state = address_info.state
    member_address.postal_code = address_info.postal_code
    member_address.country = address_info.country
    await member_address_repo.save(member_address)
    
    return MemberProfile(
        **member.model_dump(),
        age=calculate_age_from_date_of_birth(member.date_of_birth),
        address=member_address
    )

async def change_member_password(
    member_id: str,
    old_password: str,
    new_password: str,
    new_confirm_password: str
) -> bool:
    member_repo = Registry().member
    member = await member_repo.from_id(member_id)
    
    if (member.password != hash_password(old_password)):
        raise IncorrectPassword('Password is not correct')

    if (new_password != new_confirm_password):
        raise PasswordMismatch('Password and confirm password does not match')
    
    member.password = hash_password(new_password)
    await member_repo.save(member)
    return True

async def get_member_list() -> List[MemberMetaInfo]:
    member_repo = Registry().member
    member_list = await member_repo.get_list()
    member_info_list = [
        MemberMetaInfo(
            **us.model_dump(),
            age=calculate_age_from_date_of_birth(us.date_of_birth)
        ) for us in member_list]
    return member_info_list

async def get_member_profile(
    member_id: str
) -> MemberProfile:
    member_repo = Registry().member
    member_address_repo = Registry().member_adress
    member = await member_repo.from_id(member_id)

    try:
        member_address = await member_address_repo.from_member_id(member_id)
    except MemberAddressNotFound:
        member_address=None

    return MemberProfile(
        **member.model_dump(),
        age=calculate_age_from_date_of_birth(member.date_of_birth),
        address=member_address
    )
