from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.dirname(__file__))


app = FastAPI()

class Expense(BaseModel):
    amount:int
    category:str
    notes:str

class DateRange(BaseModel):
    start_date:date
    end_date:date



@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date:date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)

    if expenses is None:
        raise HTTPException(status_code=500, detail="Faield to retrieve expense summary from database")

    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date:date, expenses:List[Expense]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message":"Expanses updated successfully"}


@app.post("/analytics_by_category/")
def get_analytics_category(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)

    if date is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from database")


    total = sum([row['total'] for row in data])
    breakdown = {}
    for row in data:
        percentage= (row['total']/total)*100 if total!=0 else 0
        breakdown[row['category']] = {
            "total":row["total"],
            "percentage": percentage
        }
    return breakdown

@app.get("/analytics_by_month/")
def get_analytics_by_month():
    data =db_helper.fetch_expense_by_month()

    if date is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from database")

    return data
