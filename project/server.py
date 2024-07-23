import logging
from contextlib import asynccontextmanager
from typing import List

import project.get_content_service
import project.get_security_audit_logs_service
import project.get_ui_settings_service
import project.update_content_service
import project.update_ui_settings_service
import project.update_user_permissions_service
import project.user_login_service
import project.user_logout_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="k4",
    lifespan=lifespan,
    description="The development of the kiosk management application will be approached with meticulous attention to detail, ensuring that the final product meets all specified requirements and enhancements to cater to a broad user base while maintaining a strong security posture. The application will be built on the tech stack comprising Python for the backend programming, leveraging the FastAPI framework for its asynchronous support and ease in building APIs, PostgreSQL for the database to ensure robust data management, and Prisma as the ORM for efficient database interactions. The system design will incorporate the following key functionalities and features:\n\n- UI Customization: In line with the requirements, the UI will be fully customizable, offering theme support, layout flexibility, multi-language capability, accessibility compliance, interactive elements, real-time content updates, user authentication options, and feedback mechanisms. This approach will ensure that the UI aligns with the municipal brand identity and is universally accessible.\n\n- Local CMS: To manage and schedule a variety of content types including promotional media, informational content, and customer feedback surveys, the CMS will feature scheduling capabilities for specific times or dates, and support for offline functionality. This ensures that content remains relevant and engaging for the target audience.\n\n- Security Features: The application will incorporate user authentication, secure communication through SSL/TLS, data encryption, role-based access control (RBAC), regular security audits, and anti-tampering measures to protect the software and data from unauthorized access or modifications.\n\n- Hardware and Peripherals Support: The system will support durable, industrial-grade touchscreens and robust peripheral devices like barcode scanners and printers, prioritizing easy maintenance and updates. The hardware selection will reflect the need for high reliability in public spaces.\n\n- Analytics and Reporting: Comprehensive analytics and reporting capabilities will include real-time tracking, inventory management, customer interaction data, system performance metrics, customizable reports, predictive analytics, and a mobile-accessible dashboard.\n\n- Multilingual Support and Automated Diagnostics: The application will feature multilingual support and automated diagnostics to enhance usability for a global audience and ensure efficient operation.\n\n- Compatibility and Software Dependencies: The development process will consider compatibility with various operating systems, the need for specific runtime versions, library dependencies, and third-party tools or services interactions. Containerization technologies like Docker may also be incorporated for efficient distribution or deployment.\n\n- Recursive Programming and Human-in-the-Loop: By leveraging recursive programming, the system will manage complexity efficiently. A human-in-the-loop approach will facilitate continuous iteration and refinement of the application, ensuring that development aligns with user feedback and evolving requirements.\n\n- Integrations: Real-time device monitoring, remote management capabilities within the local network, and firewall integration will be incorporated to ensure that the system is comprehensive and secure against potential threats.\n\nThis strategic plan outlines our approach to deploying a robust, secure, and user-friendly kiosk management system on a private municipal server, incorporating advanced functionalities and ensuring that the system is adaptable, scalable, and resilient.",
)


@app.post("/auth/logout", response_model=project.user_logout_service.UserLogoutResponse)
async def api_post_user_logout(
    token: str,
) -> project.user_logout_service.UserLogoutResponse | Response:
    """
    Terminates an existing user session.
    """
    try:
        res = await project.user_logout_service.user_logout(token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/content/{kioskId}/update",
    response_model=project.update_content_service.UpdateContentResponse,
)
async def api_post_update_content(
    kioskId: str,
    title: str,
    contentBody: str,
    contentType: str,
    scheduledTime: str,
    isActive: bool,
) -> project.update_content_service.UpdateContentResponse | Response:
    """
    Updates or adds new content to the schedule.
    """
    try:
        res = await project.update_content_service.update_content(
            kioskId, title, contentBody, contentType, scheduledTime, isActive
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}/permissions",
    response_model=project.update_user_permissions_service.UpdateUserPermissionsResponse,
)
async def api_put_update_user_permissions(
    userId: str, newPermissions: List[str]
) -> project.update_user_permissions_service.UpdateUserPermissionsResponse | Response:
    """
    Updates user roles and permissions.
    """
    try:
        res = await project.update_user_permissions_service.update_user_permissions(
            userId, newPermissions
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/ui-settings/{userId}/update",
    response_model=project.update_ui_settings_service.UpdateUserUISettingsResponse,
)
async def api_put_update_ui_settings(
    userId: str, theme: str, layout: str, language: str
) -> project.update_ui_settings_service.UpdateUserUISettingsResponse | Response:
    """
    Updates the UI settings based on user preferences.
    """
    try:
        res = await project.update_ui_settings_service.update_ui_settings(
            userId, theme, layout, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/auth/login", response_model=project.user_login_service.UserLoginResponse)
async def api_post_user_login(
    username: str, password: str
) -> project.user_login_service.UserLoginResponse | Response:
    """
    Authenticates a user and initiates a session.
    """
    try:
        res = await project.user_login_service.user_login(username, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/ui-settings/{userId}",
    response_model=project.get_ui_settings_service.GetUISettingsResponse,
)
async def api_get_get_ui_settings(
    userId: str,
) -> project.get_ui_settings_service.GetUISettingsResponse | Response:
    """
    Fetches the current UI settings for a specified user.
    """
    try:
        res = await project.get_ui_settings_service.get_ui_settings(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/security/audit-logs",
    response_model=project.get_security_audit_logs_service.GetSecurityAuditLogsResponse,
)
async def api_get_get_security_audit_logs() -> project.get_security_audit_logs_service.GetSecurityAuditLogsResponse | Response:
    """
    Retrieves a log of all security-related activities.
    """
    try:
        res = await project.get_security_audit_logs_service.get_security_audit_logs()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/content/{kioskId}", response_model=project.get_content_service.GetContentResponse
)
async def api_get_get_content(
    kioskId: str,
) -> project.get_content_service.GetContentResponse | Response:
    """
    Retrieves scheduled content for a specific kiosk.
    """
    try:
        res = await project.get_content_service.get_content(kioskId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
