"""Notifications / email settings router."""

from fastapi import APIRouter, status
from pydantic import BaseModel, Field

from services.email_service import send_email

router = APIRouter()

# In-memory settings store (in production, persist to DB or a settings table)
_notification_settings: dict = {
    "smtp_host": "",
    "smtp_port": 587,
    "smtp_user": "",
    "smtp_password": "",
    "notify_task_reminder": True,
    "notify_daily_summary": True,
    "notify_weekly_report": True,
    "recipient_email": "",
}


class NotificationSettings(BaseModel):
    smtp_host: str = ""
    smtp_port: int = Field(default=587, ge=1, le=65535)
    smtp_user: str = ""
    smtp_password: str = ""
    notify_task_reminder: bool = True
    notify_daily_summary: bool = True
    notify_weekly_report: bool = True
    recipient_email: str = ""


class TestEmailRequest(BaseModel):
    recipient: str = Field(..., description="Email address to send the test to")


@router.get("/notifications/settings", response_model=NotificationSettings)
async def get_settings() -> NotificationSettings:
    """Return current notification settings (password masked)."""
    masked = dict(_notification_settings)
    masked["smtp_password"] = "***" if masked.get("smtp_password") else ""
    return NotificationSettings(**masked)


@router.post("/notifications/settings", response_model=NotificationSettings)
async def update_settings(payload: NotificationSettings) -> NotificationSettings:
    """Persist notification settings."""
    _notification_settings.update(payload.model_dump())
    return await get_settings()


@router.post("/notifications/test-email", status_code=status.HTTP_202_ACCEPTED)
async def test_email(payload: TestEmailRequest) -> dict:
    """Send a test email to verify SMTP configuration."""
    await send_email(
        to=payload.recipient,
        subject="Productivity App — Test Email",
        html_body="<h2>Test email</h2><p>SMTP configuration is working correctly.</p>",
    )
    return {"detail": "Test email dispatched"}


@router.post("/notifications/send-daily-summary", status_code=status.HTTP_202_ACCEPTED)
async def trigger_daily_summary() -> dict:
    """Manually trigger the daily summary email job."""
    from services.scheduler import send_daily_summary_job

    await send_daily_summary_job()
    return {"detail": "Daily summary dispatched"}
