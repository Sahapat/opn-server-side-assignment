from typing import List
from datetime import date
from pydantic import Field, BaseModel

from domain.model.member import GenderEnum
from domain.usecase.member_usecase import (
    RegisterMemberAddress,
    RegisterMember,
    MemberMetaInfo,
    MemberProfile,
    UpdateMemberInfo,
    UpdateAddressInfo
)

class RegisterMemberAddressRequest(RegisterMemberAddress):
    postal_code: str = Field(..., alias="postalCode")

class RegisterMemberRequest(RegisterMember):
    gender: GenderEnum = Field(..., description="'male' or 'female' or 'none'")
    date_of_birth: date = Field(..., description="2022-01-01", alias='dateOfBirth')
    is_subscribe_to_news_sletter: bool = Field(..., alias='isSubscribeToNewsSletter')
    confirm_password: str = Field(..., alias='confirmPassword')
    address: RegisterMemberAddressRequest

class MemberListResponse(BaseModel):
    member_list: List[MemberMetaInfo] = Field(..., serialization_alias ='members')

class MemberAddressResponse(UpdateAddressInfo):
    postal_code: str = Field(..., serialization_alias="postalCode")

class MemberProfileResponse(MemberProfile):
    is_subscribe_to_news_sletter: bool = Field(..., serialization_alias="isSubscribeToNewsSletter")
    address: MemberAddressResponse

class UpdateMemberInfoRequest(UpdateMemberInfo):
    date_of_birth: date = Field(..., description="2022-01-01", alias='dateOfBirth')
    is_subscribe_to_news_sletter: bool = Field(..., serialization_alias="isSubscribeToNewsSletter")

class UpdateAddressInfoRequest(UpdateAddressInfo):
    postal_code: str = Field(..., serialization_alias="postalCode")

class UpdateMemberRequest(BaseModel):
    member_info: UpdateMemberInfoRequest
    address_info: UpdateAddressInfoRequest

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword")
    new_password: str = Field(..., alias="newPassword")
    new_confirm_pasword: str = Field(..., alias="newConfirmPassword")
    