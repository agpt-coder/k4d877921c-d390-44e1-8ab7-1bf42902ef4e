import prisma
import prisma.models
from pydantic import BaseModel


class GetUISettingsResponse(BaseModel):
    """
    Model representing the user's UI settings, including theme, layout options, and language.
    """

    theme: str
    layout: str
    language: str
    accessibility_compliance: bool


async def get_ui_settings(userId: str) -> GetUISettingsResponse:
    """
    Fetches the current UI settings for a specified user.

    Args:
        userId (str): The unique identifier of the user whose UI settings are being fetched.

    Returns:
        GetUISettingsResponse: Model representing the user's UI settings, including theme, layout options, and language.
    """
    user_profile = await prisma.models.UserProfile.prisma().find_unique(
        where={"userId": userId}
    )
    if user_profile:
        theme = "default"
        layout = "default"
        accessibility_compliance = True
        return GetUISettingsResponse(
            theme=theme,
            layout=layout,
            language=user_profile.language,
            accessibility_compliance=accessibility_compliance,
        )
    else:
        raise Exception(f"User with ID {userId} does not have a profile.")
