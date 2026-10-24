from random import choice
import re
from unittest import result

import pandas as pd
import numpy as np
import os

class Expense:

    def __init__(self,date,category,amount,note=""):
        self.date=date
        self.category=category
        self.amount=amount
        self.note=note

    def __repr__(self):
        return f"Today's date={self.date}, category={self.category!r},Total amount={self.amount} "

    def to_dict(self):
        return {
          "date": self.date,
          "category": self.category,   # you fill these in
          "amount": self.amount,
          "note": self.note,
        }

class ExpenseTracker:

    def __init__(self,filename="expense.csv"):
        self.filename=filename
        self.expenses=[]

    def add_expense(self,date,category,amount,note=""):
        expense = Expense(date,category,amount,note)
        self.expenses.append(expense)

    def tocsv(self):
        df=pd.DataFrame([e.to_dict() for e in self.expenses])
        df.to_csv(self.filename,index=False)

    def __len__(self):
        return len(self.expenses)

    def average_spend(self):
        df=self.to_dataframe()
        return np.mean(df["amount"])

    def max_spend(self):
        df=self.to_dataframe()
        return np.max(df["amount"])

    
    def load(self):
        if not os.path.exists(self.filename):
            return
        df=pd.read_csv(self.filename,keep_default_na=False)
        self.expenses =[]
        for _, row in df.iterrows():
            self.add_expense(row["date"],row["category"],row["amount"],row["note"])

    def to_dataframe(self):
        return pd.DataFrame([e.to_dict() for e in self.expenses])

    def total_by_cat(self):
        df=self.to_dataframe()
        return df.groupby("category")["amount"].sum()

    def filter_by_month(self,month):
        df=self.to_dataframe()
        df["date"]=pd.to_datetime(df["date"])
        return df[df["date"].dt.month == 10]



def main():
    tracker=ExpenseTracker()
    tracker.load()

    while True:
        print("\n1 Add Expense")
        print("\n2. Show total by category")
        print("\n3. Show average and max spend")
        print("\n4. Show expenses for a month")
        print("5. Quit")
        choose= input("\nCHoose: ")

        if choose=="1":
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")
            amount = float(input("Amount: "))   
            note = input("Note: ")
            tracker.add_expense(date,category,amount,note)    # fill in: pass the four values
            tracker.tocsv()
            print("Expense added!")
        elif choose=="2":
            if len(tracker) == 0:
                print("No expenses yet.")
            else:
                 print(tracker.total_by_cat()) 
        elif choose=="3":
            if len(tracker)==0:
                print("No expense yet")
            else:
                print("Average:", tracker.average_spend())
                print("MAX: ",tracker.max_spend())
        elif choose=="4":
            month=int(input("enter the month(1-12): "))
            result=tracker.filter_by_month(month)
            if result.empty:
                print("NO expennses yet")
            else:
                print(result)
        elif choose=="5":
            break
        else:
            print("Invallid choice")
            print("hello")

if __name__ == "__main__":
    main()