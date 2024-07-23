from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserPermissionsResponse(BaseModel):
    """
    Response model confirming the updated permissions of the user.
    """

    userId: str
    updatedPermissions: List[str]
    status: str


async def update_user_permissions(
    userId: str, newPermissions: List[str]
) -> UpdateUserPermissionsResponse:
    """
    Updates user roles and permissions.

    Args:
    userId (str): The unique identifier of the user whose permissions are to be updated.
    newPermissions (List[str]): A list of new permissions to be applied to the user.

    Returns:
    UpdateUserPermissionsResponse: Response model confirming the updated permissions of the user.

    Example:
    update_user_permissions('123e4567-e89b-12d3-a456-426614174000', ['MunicipalAdmin'])
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return UpdateUserPermissionsResponse(
            userId=userId, updatedPermissions=[], status="User not found"
        )
    try:
        if newPermissions:
            await prisma.models.User.prisma().update(
                where={"id": userId}, data={"role": newPermissions[0]}
            )
        return UpdateUserPermissionsResponse(
            userId=userId, updatedPermissions=newPermissions, status="Success"
        )
    except Exception as e:
        return UpdateUserPermissionsResponse(
            userId=userId, updatedPermissions=[], status=f"Update failed: {str(e)}"
        )
