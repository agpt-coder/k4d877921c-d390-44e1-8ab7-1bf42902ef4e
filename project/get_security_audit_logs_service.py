from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class SecurityAuditLog(BaseModel):
    """
    Represents a single security audit log entry.
    """

    timestamp: datetime
    user_id: str
    action: str
    details: str


class GetSecurityAuditLogsResponse(BaseModel):
    """
    Provides a list of all security-related activities logged in the system.
    """

    logs: List[SecurityAuditLog]


async def get_security_audit_logs() -> GetSecurityAuditLogsResponse:
    """
    Retrieves a log of all security-related activities.

    This function queries the DeviceInteraction and User tables to construct a detailed log
    of security-related activities, focusing on device and authentication actions.

    Returns:
        GetSecurityAuditLogsResponse: An object containing a list of all recorded security-related activities.
    """
    device_interactions = await prisma.models.DeviceInteraction.prisma().find_many(
        include={"User": True}
    )
    logs = [
        SecurityAuditLog(
            timestamp=interaction.createdAt,
            user_id=interaction.userId if interaction.userId else "Unknown",
            action=interaction.action,
            details=interaction.description or "No details provided.",
        )
        for interaction in device_interactions
    ]
    return GetSecurityAuditLogsResponse(logs=logs)
