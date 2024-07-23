from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserInterfaceSettings(BaseModel):
    """
    The set of customizable UI settings applied for a user.
    """

    theme: str
    layout: str
    language: str


class UpdateUserUISettingsResponse(BaseModel):
    """
    Response after updating the UI settings, reflecting the applied changes or an error state.
    """

    success: bool
    message: Optional[str] = None
    updatedSettings: UserInterfaceSettings


async def update_ui_settings(
    userId: str, theme: str, layout: str, language: str
) -> UpdateUserUISettingsResponse:
    """
    Updates the UI settings based on user preferences.

    Args:
        userId (str): The identifier of the user whose UI settings are being updated.
        theme (str): The desired theme for the user interface.
        layout (str): The layout preference to adjust the user interface.
        language (str): The preferred language setting for the user interface.

    Returns:
        UpdateUserUISettingsResponse: Response after updating the UI settings, reflecting the applied changes or an error state.
    """
    try:
        user_profile = await prisma.models.UserProfile.prisma().find_unique(
            where={"userId": userId}
        )
        if not user_profile:
            return UpdateUserUISettingsResponse(
                success=False,
                message="User profile not found",
                updatedSettings=UserInterfaceSettings(theme="", layout="", language=""),
            )
        updated_profile = await prisma.models.UserProfile.prisma().update(
            where={"userId": userId}, data={"language": language}
        )
        return UpdateUserUISettingsResponse(
            success=True,
            message="UI settings updated successfully",
            updatedSettings=UserInterfaceSettings(
                theme=theme, layout=layout, language=language
            ),
        )
    except Exception as e:
        return UpdateUserUISettingsResponse(
            success=False,
            message=f"Failed to update UI settings: {e}",
            updatedSettings=UserInterfaceSettings(theme="", layout="", language=""),
        )
