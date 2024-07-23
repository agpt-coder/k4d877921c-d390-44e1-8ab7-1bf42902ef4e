from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class ContentDetails(BaseModel):
    """
    Detailed information about a single content item including its title, type, and scheduled time.
    """

    title: str
    contentBody: str
    contentType: prisma.enums.ContentType
    scheduledTime: datetime
    isActive: bool


class GetContentResponse(BaseModel):
    """
    Response model for scheduled content retrieval. Contains details about the content scheduled for the specified kiosk.
    """

    contentList: List[ContentDetails]


async def get_content(kioskId: str) -> GetContentResponse:
    """
    Retrieves scheduled content for a specific kiosk.

    This function queries the database to find all active content related to
    the specified kiosk, scheduled before the current time.

    Args:
        kioskId (str): Unique identifier for the kiosk whose content is being requested.

    Returns:
        GetContentResponse: Response model for scheduled content retrieval. Contains details about the content scheduled for the specified kiosk.
    """
    contents = await prisma.models.Content.prisma().find_many(
        where={"isActive": True, "scheduledTime": {"lte": datetime.utcnow()}}
    )
    content_details_list = [
        ContentDetails(
            title=content.title,
            contentBody=content.contentBody,
            contentType=content.contentType,
            scheduledTime=content.scheduledTime,
            isActive=content.isActive,
        )
        for content in contents
    ]
    return GetContentResponse(contentList=content_details_list)
