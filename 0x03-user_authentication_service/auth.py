#!/usr/bin/env python3
"""
Auth module
"""
from bcrypt import checkpw
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Generates a hash for a user's password.

    Args:
        password (str): The user's password.

    Returns:
        str: The hashed password.
    """
    encoded_password = password.encode("utf")

    salt = bcrypt.gensalt()

    hashedpw = bcrypt.hashpw(encoded_password, salt)

    return hashedpw

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            User: The registered user.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login credentials are valid.

        Args:
            email (str): The email address of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode('utf-8'), user.hashed_password)




if __name__ == '__main__':
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'

    auth = Auth()

    auth.register_user(email, password)

    print(auth.valid_login(email, password))

    print(auth.valid_login(email, "WrongPwd"))

    print(auth.valid_login("unknown@email", password))
