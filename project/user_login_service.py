from datetime import datetime, timedelta
from typing import Optional

import prisma
import prisma.models
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Model for the response after a user login attempt. Contains the result of the authentication process.
    """

    success: bool
    message: str
    token: Optional[str] = None
    userId: Optional[str] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "MY_SUPER_SECRET_KEY"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies password against the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_msgs (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT token that is used as the access token.

    Args:
        data (dict): A dictionary of claims. For example, a sub claim to identify the user.
        expires_delta (Optional[timedelta]): The amount of time till the token expires.

    Returns:
        str: The JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def user_login(username: str, password: str) -> UserLoginResponse:
    """
    Authenticates a user and initiates a session.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password for the user.

    Returns:
        UserLoginResponse: Model for the response after a user login attempt.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user is None or not verify_password(password, user.password):
        return UserLoginResponse(success=False, message="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return UserLoginResponse(
        success=True, message="Login successful", token=access_token, userId=user.id
    )
