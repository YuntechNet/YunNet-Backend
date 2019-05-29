import time

def jwt_payload(session_limit: int, username: str):
    """
    Return JWT payload base

    Attributes:
        session_limit -- The survive time of this session
        username -- Username field
    """
    payload = {
        'exp': time.time() + session_limit,
        'username': username,
    }
    return payload
