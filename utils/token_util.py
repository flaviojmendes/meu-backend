import os
from constants import AUTH0_NAMESPACE

def get_nickname_from_token(token: str) -> str:
    nickname = token[f"{AUTH0_NAMESPACE}nickname"]
    return nickname