import bcrypt

def encrypt_password(password: str) -> str:
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)