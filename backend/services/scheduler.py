"""APScheduler background job scheduler."""

import logging
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="UTC")


async def check_task_reminders() -> None:
    """Send reminder emails for tasks due within the next hour."""
    try:
        from database import AsyncSessionLocal
        from models.task import Task
        from services.email_service import send_email, task_reminder_html
        from sqlalchemy import select

        async with AsyncSessionLocal() as db:
            now = datetime.now(timezone.utc)
            cutoff = now + timedelta(hours=1)
            result = await db.execute(
                select(Task)
                .where(Task.deadline >= now, Task.deadline <= cutoff)
                .where(Task.status.notin_(["completed", "archived"]))
            )
            tasks = result.scalars().all()
            if tasks and settings.SMTP_USER:
                for task in tasks:
                    deadline_str = task.deadline.strftime("%Y-%m-%d %H:%M UTC") if task.deadline else "N/A"
                    await send_email(
                        to=settings.SMTP_USER,
                        subject=f"Task Reminder: {task.title}",
                        html_body=task_reminder_html(task.title, deadline_str),
                    )
    except Exception:
        logger.exception("Error in check_task_reminders job")


async def send_daily_summary_job() -> None:
    """Send a daily productivity summary email."""
    try:
        from database import AsyncSessionLocal
        from models.task import Task
        from services.email_service import daily_summary_html, send_email
        from sqlalchemy import select
        import datetime as dt

        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Task))
            tasks = result.scalars().all()
            today = dt.date.today()
            completed = sum(
                1
                for t in tasks
                if t.status == "completed"
                and t.updated_at
                and t.updated_at.date() == today
            )
            due_today = sum(
                1
                for t in tasks
                if t.deadline
                and t.deadline.date() == today
                and t.status not in ("completed", "archived")
            )
            if settings.SMTP_USER:
                await send_email(
                    to=settings.SMTP_USER,
                    subject="Your Daily Productivity Summary",
                    html_body=daily_summary_html(completed, len(tasks), due_today),
                )
    except Exception:
        logger.exception("Error in send_daily_summary_job")


async def send_weekly_report_job() -> None:
    """Send a weekly progress report email."""
    try:
        from database import AsyncSessionLocal
        from models.task import Task
        from models.vocabulary import LanguageVocabulary
        from services.email_service import send_email, weekly_report_html
        from sqlalchemy import select
        import datetime as dt

        async with AsyncSessionLocal() as db:
            today = dt.date.today()
            week_start = today - dt.timedelta(days=today.weekday())

            task_result = await db.execute(select(Task))
            tasks = task_result.scalars().all()
            completed_week = sum(
                1
                for t in tasks
                if t.status == "completed"
                and t.updated_at
                and t.updated_at.date() >= week_start
            )

            vocab_result = await db.execute(select(LanguageVocabulary))
            vocab = vocab_result.scalars().all()
            words_learned = sum(
                1
                for v in vocab
                if v.learned and v.date_learned and v.date_learned >= week_start
            )

            if settings.SMTP_USER:
                await send_email(
                    to=settings.SMTP_USER,
                    subject="Your Weekly Progress Report",
                    html_body=weekly_report_html(completed_week, words_learned),
                )
    except Exception:
        logger.exception("Error in send_weekly_report_job")


# Register jobs
scheduler.add_job(check_task_reminders, "interval", hours=1, id="task_reminders")
scheduler.add_job(
    send_daily_summary_job,
    CronTrigger(hour=8, minute=0),
    id="daily_summary",
)
scheduler.add_job(
    send_weekly_report_job,
    CronTrigger(day_of_week="mon", hour=8, minute=0),
    id="weekly_report",
)
