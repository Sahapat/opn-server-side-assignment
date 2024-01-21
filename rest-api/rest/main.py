from functools import partial
from pydantic import ValidationError
from fastapi import FastAPI, HTTPException, Depends

from domain.usecase.member_usecase import (
    get_member_list,
    get_member_profile,
    register_member,
    update_member_info,
    change_member_password
)
from domain.usecase.exception import PasswordMismatch, AgeValidationError, IncorrectPassword
from domain.model.member.repository import MemberNotFound 
from .authorization import authentication_guard
from .event_handler import on_startup, on_shutdown
from .schema import (
    RegisterMemberRequest,
    MemberListResponse,
    MemberProfileResponse,
    UpdateMemberRequest,
    ChangePasswordRequest
)

def create_app():
    fast_app = FastAPI(title='Member Service')
    fast_app.add_event_handler('startup', func=partial(on_startup, app=fast_app))
    fast_app.add_event_handler('shutdown', func=partial(on_shutdown, app=fast_app))
    return fast_app


app = create_app()

@app.get('/members', response_model=MemberListResponse, dependencies=[Depends(authentication_guard)])
async def do_get_members():
    member_list = await get_member_list()
    return MemberListResponse(member_list=member_list)

@app.get('/members/profile/{member_id}', response_model=MemberProfileResponse, dependencies=[Depends(authentication_guard)])
async def do_get_member_profile(member_id: str):
    try:
        member = await get_member_profile(member_id)
    except MemberNotFound as err:
        raise HTTPException(404, str(err))
    return MemberProfileResponse(
        **member.model_dump()
    )

@app.post('/members', response_model=MemberProfileResponse, dependencies=[Depends(authentication_guard)])
async def do_register_member(regiser_data: RegisterMemberRequest):
    try:
        member_profile = await register_member(regiser_data)
    except (PasswordMismatch, ValidationError, AgeValidationError) as err:
        raise HTTPException(400, f'{err.__class__.__name__}: {str(err)}')
    return MemberProfileResponse(
        **member_profile.model_dump()
    )

@app.put('/members/{member_id}', response_model=MemberProfileResponse, dependencies=[Depends(authentication_guard)])
async def do_update_member(member_id: str, update_member_data: UpdateMemberRequest):
    try:
        member = await update_member_info(
            member_id=member_id,
            member_info=update_member_data.member_info,
            address_info=update_member_data.address_info
        )
    except (ValidationError, AgeValidationError) as err:
        raise HTTPException(400, f'{err.__class__.__name__}: {str(err)}')    
    except MemberNotFound:
        raise HTTPException(404, f'Member with id {member_id} not found')
    return MemberProfileResponse(
        **member.model_dump()
    )

@app.post('/members/{member_id}/change-pasword', response_model=bool, dependencies=[Depends(authentication_guard)])
async def do_change_password(member_id: str, change_password_data: ChangePasswordRequest):
    try:
        result = await change_member_password(
            member_id=member_id,
            old_password=change_password_data.old_password,
            new_password=change_password_data.new_password,
            new_confirm_password=change_password_data.new_confirm_pasword
        )
    except (PasswordMismatch, IncorrectPassword) as err:
        raise HTTPException(400, f'{err.__class__.__name__}: {str(err)}')    
    except MemberNotFound:
        raise HTTPException(404, f'Member with id {member_id} not found')
    return result
