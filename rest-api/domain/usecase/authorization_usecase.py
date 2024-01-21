from .exception import InvalidToken

async def verify_auth_token(token: str) -> bool:
    if token != 'faketoken_user1':
        raise InvalidToken("Unauthorized. Invalid token")
    return True
