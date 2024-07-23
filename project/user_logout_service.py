from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class UserLogoutResponse(BaseModel):
    """
    Confirms that the user session has been successfully terminated, without exposing any sensitive information.
    """

    status: str
    message: str


async def user_logout(token: str) -> UserLogoutResponse:
    """
    Terminates an existing user session.

    This function first looks up the provided session token in the `AuthToken` table. If found,
    it deletes the token from the table, effectively ending the user session. If the token does
    not exist or has already expired, it returns a response indicating failure to log out.

    Args:
        token (str): The session token or ID used for authenticating the request, to ensure that the session is rightfully terminated by its owner or a valid authority.

    Returns:
        UserLogoutResponse: Confirms that the user session has been successfully terminated, with details.

    Example:
        response = user_logout("example-session-token")
        > UserLogoutResponse(status="success", message="Session terminated successfully.")
    """
    auth_token = await prisma.models.AuthToken.prisma().find_unique(
        where={"token": token}
    )
    if auth_token and auth_token.expiresAt > datetime.now():
        await prisma.models.AuthToken.prisma().delete(where={"token": token})
        return UserLogoutResponse(
            status="success", message="Session terminated successfully."
        )
    else:
        return UserLogoutResponse(
            status="error", message="Invalid session token or token already expired."
        )
