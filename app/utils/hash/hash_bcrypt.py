import bcrypt
from passlib.context import CryptContext


async def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


async def check_password(stored_hash: str, password: str) -> bool:
    result = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    return result
