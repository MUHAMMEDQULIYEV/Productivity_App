"""Email sending service using SMTP."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import settings


async def send_email(to: str, subject: str, html_body: str) -> None:
    """Send an HTML email via SMTP.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        html_body: HTML content of the email body.

    Raises:
        RuntimeError: If SMTP configuration is missing or sending fails.
    """
    if not settings.SMTP_USER or not settings.SMTP_HOST:
        raise RuntimeError("SMTP is not configured. Set SMTP_HOST and SMTP_USER in .env.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
    msg["To"] = to
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(msg["From"], [to], msg.as_string())


def task_reminder_html(task_title: str, deadline: str) -> str:
    """Return HTML body for a task deadline reminder."""
    return (
        f"<h2>Task Reminder</h2>"
        f"<p>Your task <strong>{task_title}</strong> is due at <strong>{deadline}</strong>.</p>"
        f"<p>Log in to your Productivity App to update its status.</p>"
    )


def daily_summary_html(completed: int, total: int, due_today: int) -> str:
    """Return HTML body for the daily summary email."""
    return (
        f"<h2>Daily Productivity Summary</h2>"
        f"<ul>"
        f"<li>Tasks completed today: <strong>{completed}</strong></li>"
        f"<li>Total tasks: <strong>{total}</strong></li>"
        f"<li>Tasks due today: <strong>{due_today}</strong></li>"
        f"</ul>"
        f"<p>Keep it up! 🚀</p>"
    )


def weekly_report_html(completed_week: int, words_learned: int) -> str:
    """Return HTML body for the weekly progress report."""
    return (
        f"<h2>Weekly Progress Report</h2>"
        f"<ul>"
        f"<li>Tasks completed this week: <strong>{completed_week}</strong></li>"
        f"<li>New vocabulary words learned: <strong>{words_learned}</strong></li>"
        f"</ul>"
        f"<p>Great work this week! 🎉</p>"
    )
