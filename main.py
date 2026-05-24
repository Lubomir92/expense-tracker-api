from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
from database import engine, Base, SessionLocal

app = FastAPI()

# vytvorenie tabuliek v DB
Base.metadata.create_all(bind=engine)


# dependency — databázová session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model (čo prichádza z requestu)
class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str


@app.get("/")
def home():
    return {"message": "API funguje"}


# CREATE
@app.post("/expenses")
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if not expense:
        return {"error": "Expense not found"}

    db.delete(expense)
    db.commit()

    return {"message": "Deleted"}
@app.put("/expenses/{expense_id}")
def update_expense(expense_id: int, updated: ExpenseCreate, db: Session = Depends(get_db)):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()

    if not expense:
        return {"error": "Expense not found"}

    expense.title = updated.title
    expense.amount = updated.amount
    expense.category = updated.category

    db.commit()
    db.refresh(expense)

    return expense

@app.get("/expenses/category/{category}")
def get_by_category(category: str, db: Session = Depends(get_db)):
    return db.query(models.Expense).filter(models.Expense.category == category).all()

