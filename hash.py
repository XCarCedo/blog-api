from passlib.context import CryptContext

_ctx = CryptContext("argon2")

def hash(password: str) -> str:
    return _ctx.hash(password)

def verify(plain_password: str, hashed_password: str) -> str:
    return _ctx.verify(plain_password, hashed_password)
