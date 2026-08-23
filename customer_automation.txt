from datetime import datetime, timezone
from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# =================================================================
# 1. DATABASE SETUP
# =================================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./customer_automation.db"
# Note: For production, use PostgreSQL or MySQL.
# "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# =================================================================
# 2. SQLALCHEMY ORM MODELS
# =================================================================
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    reminder_type = Column(String(50)) # e.g., "cart_abandonment", "subscription_renewal"
    message_body = Column(Text)
    status = Column(Enum("pending", "sent", "failed", "cancelled", name="reminder_status"), default="pending")
    due_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# Create all tables
Base.metadata.create_all(bind=engine)

# =================================================================
# 3. PYDANTIC SCHEMAS (Data Validation)
# =================================================================
class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class CustomerResponse(CustomerCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ReminderCreate(BaseModel):
    customer_id: int
    reminder_type: str
    message_body: str
    due_at: datetime

class ReminderResponse(ReminderCreate):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# =================================================================
# 4. FASTAPI APP & DEPENDENCIES
# =================================================================
app = FastAPI(title="Customer Automation API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock function simulating sending an email or SMS
def trigger_communication_api(reminder_id: int, message_body: str):
    # In a real app, this would use Celery/Redis to call Twilio/SendGrid
    print(f"[MOCK BACKGROUND JOB] Sending reminder {reminder_id}: {message_body}")


# =================================================================
# 5. ROUTES
# =================================================================

@app.post("/customers/", response_model=CustomerResponse, tags=["Customers"])
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_customer = Customer(**customer.model_dump())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@app.get("/customers/", response_model=List[CustomerResponse], tags=["Customers"])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Customer).offset(skip).limit(limit).all()


@app.post("/reminders/", response_model=ReminderResponse, tags=["Automation"])
def create_reminder(
    reminder: ReminderCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Verify customer exists
    customer = db.query(Customer).filter(Customer.id == reminder.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    new_reminder = Reminder(**reminder.model_dump())
    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)

    # If the reminder is due now (or in the past), trigger immediately
    if new_reminder.due_at <= datetime.now(timezone.utc):
        background_tasks.add_task(
            trigger_communication_api, 
            new_reminder.id, 
            new_reminder.message_body
        )
        new_reminder.status = "sent"
        db.commit()

    return new_reminder

@app.get("/reminders/pending", response_model=List[ReminderResponse], tags=["Automation"])
def get_pending_reminders(db: Session = Depends(get_db)):
    return db.query(Reminder).filter(Reminder.status == "pending").all()