import bcrypt

def encrypt_password(password: str) -> str:
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt).decode('utf-8')

def check_password(input_password: str, hashed_password: str) -> bool:
    is_valid = bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))
    return is_valid
