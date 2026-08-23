from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query
from sqlalchemy import func

# Import these from your main application
from customer_automation import (
    SessionLocal,
    Customer,
    Message,
    Reminder,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports & Analytics"]
)


# ============================================================
# DATE HELPERS
# ============================================================

def get_date_range(days: int):

    end = datetime.now(timezone.utc)

    start = end - timedelta(days=days)

    return start, end


# ============================================================
# TASK REPORT
# ============================================================

@router.get("/tasks")
def task_report(
    days: int = Query(
        30,
        ge=1,
        le=365
    )
):

    db = SessionLocal()

    try:

        start, end = get_date_range(days)

        total = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= start,
                Reminder.created_at <= end
            )
            .scalar()
            or 0
        )

        completed = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= start,
                Reminder.created_at <= end,
                Reminder.status == "sent"
            )
            .scalar()
            or 0
        )

        pending = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.status == "pending"
            )
            .scalar()
            or 0
        )

        failed = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= start,
                Reminder.created_at <= end,
                Reminder.status == "failed"
            )
            .scalar()
            or 0
        )

        cancelled = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= start,
                Reminder.created_at <= end,
                Reminder.status == "cancelled"
            )
            .scalar()
            or 0
        )

        overdue = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.status == "pending",
                Reminder.due_at < datetime.now(timezone.utc)
            )
            .scalar()
            or 0
        )

        completion_rate = (
            (completed / total) * 100
            if total > 0
            else 0
        )

        return {
            "report": "Task Report",

            "period_days": days,

            "total_tasks": total,

            "completed": completed,

            "pending": pending,

            "overdue": overdue,

            "failed": failed,

            "cancelled": cancelled,

            "completion_rate": round(
                completion_rate,
                2
            )
        }

    finally:

        db.close()


# ============================================================
# COMPLETION STATISTICS
# ============================================================

@router.get("/completion")
def completion_statistics(
    days: int = Query(
        30,
        ge=1,
        le=365
    )
):

    db = SessionLocal()

    try:

        start, end = get_date_range(days)

        statuses = [
            "pending",
            "sent",
            "failed",
            "cancelled"
        ]

        result = {}

        for status in statuses:

            count = (
                db.query(func.count(Reminder.id))
                .filter(
                    Reminder.created_at >= start,
                    Reminder.created_at <= end,
                    Reminder.status == status
                )
                .scalar()
                or 0
            )

            result[status] = count

        total = sum(result.values())

        result["total"] = total

        result["completion_percentage"] = round(
            (
                result["sent"] / total * 100
            )
            if total
            else 0,
            2
        )

        return result

    finally:

        db.close()


# ============================================================
# PRODUCTIVITY REPORT
# ============================================================

@router.get("/productivity")
def productivity_report(
    days: int = Query(
        30,
        ge=1,
        le=365
    )
):

    db = SessionLocal()

    try:

        start, end = get_date_range(days)

        completed_tasks = (
            db.query(Reminder)
            .filter(
                Reminder.status == "sent",
                Reminder.created_at >= start,
                Reminder.created_at <= end
            )
            .all()
        )

        total_completed = len(
            completed_tasks
        )

        total_tasks = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= start,
                Reminder.created_at <= end
            )
            .scalar()
            or 0
        )

        completion_rate = (
            total_completed / total_tasks * 100
            if total_tasks
            else 0
        )

        # Average retries

        total_attempts = sum(
            task.attempts or 0
            for task in completed_tasks
        )

        average_attempts = (
            total_attempts / total_completed
            if total_completed
            else 0
        )

        # Group tasks by type

        task_types = {}

        for task in completed_tasks:

            task_type = task.reminder_type

            if task_type not in task_types:
                task_types[task_type] = 0

            task_types[task_type] += 1

        return {

            "report": "Productivity Report",

            "period_days": days,

            "total_tasks": total_tasks,

            "completed_tasks": total_completed,

            "completion_rate": round(
                completion_rate,
                2
            ),

            "average_attempts": round(
                average_attempts,
                2
            ),

            "completed_by_type": task_types
        }

    finally:

        db.close()


# ============================================================
# DAILY PRODUCTIVITY
# ============================================================

@router.get("/daily")
def daily_productivity(
    days: int = Query(
        7,
        ge=1,
        le=365
    )
):

    db = SessionLocal()

    try:

        start, end = get_date_range(days)

        reminders = (
            db.query(Reminder)
            .filter(
                Reminder.created_at >= start,
                Reminder.created_at <= end
            )
            .all()
        )

        daily = {}

        for reminder in reminders:

            date = reminder.created_at.date().isoformat()

            if date not in daily:

                daily[date] = {
                    "total": 0,
                    "completed": 0,
                    "pending": 0,
                    "failed": 0,
                    "cancelled": 0
                }

            daily[date]["total"] += 1

            if reminder.status == "sent":
                daily[date]["completed"] += 1

            elif reminder.status == "pending":
                daily[date]["pending"] += 1

            elif reminder.status == "failed":
                daily[date]["failed"] += 1

            elif reminder.status == "cancelled":
                daily[date]["cancelled"] += 1

        return {
            "report": "Daily Productivity",
            "period_days": days,
            "data": daily
        }

    finally:

        db.close()


# ============================================================
# CHANNEL REPORT
# ============================================================

@router.get("/channels")
def channel_report(
    days: int = Query(
        30,
        ge=1,
        le=365
    )
):

    db = SessionLocal()

    try:

        start, end = get_date_range(days)

        whatsapp = (
            db.query(func.count(Message.id))
            .filter(
                Message.channel == "WhatsApp",
                Message.created_at >= start,
                Message.created_at <= end
            )
            .scalar()
            or 0
        )

        email = (
            db.query(func.count(Message.id))
            .filter(
                Message.channel == "Email",
                Message.created_at >= start,
                Message.created_at <= end
            )
            .scalar()
            or 0
        )

        incoming = (
            db.query(func.count(Message.id))
            .filter(
                Message.direction == "incoming",
                Message.created_at >= start,
                Message.created_at <= end
            )
            .scalar()
            or 0
        )

        outgoing = (
            db.query(func.count(Message.id))
            .filter(
                Message.direction == "outgoing",
                Message.created_at >= start,
                Message.created_at <= end
            )
            .scalar()
            or 0
        )

        return {

            "report": "Communication Report",

            "period_days": days,

            "whatsapp_messages": whatsapp,

            "email_messages": email,

            "incoming_messages": incoming,

            "outgoing_messages": outgoing,

            "total_messages": (
                incoming + outgoing
            )
        }

    finally:

        db.close()


# ============================================================
# REMINDER REPORT
# ============================================================

@router.get("/reminders")
def reminder_report(
    days: int = Query(
        30,
        ge=1,
        le=365
    )
):

    db = SessionLocal()

    try:

        start, end = get_date_range(days)

        reminders = (
            db.query(Reminder)
            .filter(
                Reminder.created_at >= start,
                Reminder.created_at <= end
            )
            .all()
        )

        by_type = {}

        for reminder in reminders:

            reminder_type = (
                reminder.reminder_type
            )

            if reminder_type not in by_type:

                by_type[reminder_type] = {
                    "total": 0,
                    "sent": 0,
                    "pending": 0,
                    "failed": 0,
                    "cancelled": 0
                }

            by_type[reminder_type]["total"] += 1

            if reminder.status == "sent":
                by_type[reminder_type]["sent"] += 1

            elif reminder.status == "pending":
                by_type[reminder_type]["pending"] += 1

            elif reminder.status == "failed":
                by_type[reminder_type]["failed"] += 1

            elif reminder.status == "cancelled":
                by_type[reminder_type]["cancelled"] += 1

        return {
            "report": "Reminder Report",
            "period_days": days,
            "by_type": by_type
        }

    finally:

        db.close()


# ============================================================
# CUSTOMER REPORT
# ============================================================

@router.get("/customers")
def customer_report():

    db = SessionLocal()

    try:

        total_customers = (
            db.query(func.count(Customer.id))
            .scalar()
            or 0
        )

        customers_with_email = (
            db.query(func.count(Customer.id))
            .filter(
                Customer.email.isnot(None)
            )
            .scalar()
            or 0
        )

        customers_with_whatsapp = (
            db.query(func.count(Customer.id))
            .filter(
                Customer.whatsapp.isnot(None)
            )
            .scalar()
            or 0
        )

        return {

            "report": "Customer Report",

            "total_customers": total_customers,

            "customers_with_email":
                customers_with_email,

            "customers_with_whatsapp":
                customers_with_whatsapp
        }

    finally:

        db.close()


# ============================================================
# COMPLETE DASHBOARD REPORT
# ============================================================

@router.get("/dashboard")
def dashboard_report():

    db = SessionLocal()

    try:

        now = datetime.now(timezone.utc)

        today = now - timedelta(days=1)

        week = now - timedelta(days=7)

        month = now - timedelta(days=30)

        # ----------------------------------------------------
        # TODAY
        # ----------------------------------------------------

        today_total = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= today
            )
            .scalar()
            or 0
        )

        today_completed = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= today,
                Reminder.status == "sent"
            )
            .scalar()
            or 0
        )

        # ----------------------------------------------------
        # WEEK
        # ----------------------------------------------------

        week_total = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= week
            )
            .scalar()
            or 0
        )

        week_completed = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= week,
                Reminder.status == "sent"
            )
            .scalar()
            or 0
        )

        # ----------------------------------------------------
        # MONTH
        # ----------------------------------------------------

        month_total = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= month
            )
            .scalar()
            or 0
        )

        month_completed = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.created_at >= month,
                Reminder.status == "sent"
            )
            .scalar()
            or 0
        )

        # ----------------------------------------------------
        # PENDING
        # ----------------------------------------------------

        pending = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.status == "pending"
            )
            .scalar()
            or 0
        )

        # ----------------------------------------------------
        # OVERDUE
        # ----------------------------------------------------

        overdue = (
            db.query(func.count(Reminder.id))
            .filter(
                Reminder.status == "pending",
                Reminder.due_at < now
            )
            .scalar()
            or 0
        )

        def rate(completed, total):

            if total == 0:
                return 0

            return round(
                completed / total * 100,
                2
            )

        return {

            "dashboard": "Reports & Analytics",

            "today": {
                "tasks": today_total,
                "completed": today_completed,
                "completion_rate":
                    rate(
                        today_completed,
                        today_total
                    )
            },

            "last_7_days": {
                "tasks": week_total,
                "completed": week_completed,
                "completion_rate":
                    rate(
                        week_completed,
                        week_total
                    )
            },

            "last_30_days": {
                "tasks": month_total,
                "completed": month_completed,
                "completion_rate":
                    rate(
                        month_completed,
                        month_total
                    )
            },

            "current_status": {
                "pending": pending,
                "overdue": overdue
            }
        }

    finally:

        db.close()