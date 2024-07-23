from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateContentResponse(BaseModel):
    """
    Response model confirming the content has been updated or added to the schedule, including the identifier of the updated or new content item.
    """

    contentId: str
    message: str


async def update_content(
    kioskId: str,
    title: str,
    contentBody: str,
    contentType: str,
    scheduledTime: str,
    isActive: bool,
) -> UpdateContentResponse:
    """
    Updates or adds new content to the schedule.

    Args:
        kioskId (str): The unique identifier of the kiosk where the content is to be scheduled.
        title (str): The title of the content to be added or updated.
        contentBody (str): The body of the content, may include text, URLs to images or videos, etc.
        contentType (str): The type of content being scheduled (e.g., Image, Video, NewsTicker).
        scheduledTime (str): The specific datetime when the content is scheduled to be displayed. It is expected in ISO 8601 format.
        isActive (bool): Flag indicating whether the content is active and should be displayed according to the schedule.

    Returns:
        UpdateContentResponse: Response model confirming the content has been updated or added to the schedule, including the identifier of the updated or new content item.
    """
    scheduledTime_datetime = datetime.fromisoformat(scheduledTime)
    existing_content: Optional[
        prisma.models.Content
    ] = await prisma.models.Content.prisma().find_unique(
        where={"title": title, "kioskId": kioskId}
    )
    if existing_content:
        updated_content = await prisma.models.Content.prisma().update(
            where={"id": existing_content.id},
            data={
                "contentBody": contentBody,
                "contentType": contentType,
                "scheduledTime": scheduledTime_datetime,
                "isActive": isActive,
            },
        )
        content_id = existing_content.id
        message = "Content updated successfully."
    else:
        new_content = await prisma.models.Content.prisma().create(
            data={
                "title": title,
                "contentBody": contentBody,
                "contentType": contentType,
                "scheduledTime": scheduledTime_datetime,
                "isActive": isActive,
                "kioskId": kioskId,
            }
        )
        content_id = new_content.id
        message = "New content added successfully."
    return UpdateContentResponse(contentId=content_id, message=message)
