from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from domain.usecase.exception import InvalidToken
from domain.usecase import verify_auth_token

httpBearer = HTTPBearer()

async def authentication_guard(bearer: HTTPAuthorizationCredentials = Depends(httpBearer)) -> bool:
    try:
        result = await verify_auth_token(bearer.credentials)
    except InvalidToken as err:
        raise HTTPException(403, f'{err.__class__.__name__}: {str(err)}')
    return result
