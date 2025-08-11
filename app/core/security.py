import bcrypt

def hash_password(password: str) -> str:
    """
    Hash the password using bcrypt.
    Returns a UTF-8 string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Store as string in DB


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))