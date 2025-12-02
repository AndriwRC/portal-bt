from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str | bytes, hashed_password: str | bytes):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str | bytes):
    return password_hash.hash(password)
