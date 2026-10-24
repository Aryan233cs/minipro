from calendar import c
from itertools import count
import os

from matplotlib.pylab import f
import numpy as np
import pandas as pd
from pandas import col
from traitlets import default

class Student:

    def __init__(self,roll_no,name,marks):
        for subject, mark in marks.items():
            if mark<0 or mark>100:
                raise ValueError(f"invalid marks for {subject}:{mark}")
        self.roll_no=roll_no
        self.name=name
        self.marks=marks

    def __repr__(self):
        return f"Students({self.roll_no},{self.name!r},{self.marks})"

class Gradebook:

    def __init__(self,filename="student.csv"):
        self.filename=filename
        self.students=[]

    def add_student(self,roll_no,name,marks):
        student=Student(roll_no,name,marks)
        self.students.append(student)

    def to_dataframe(self):
        rows=[]
        for s in self.students:
            row={"roll_no":s.roll_no,"name":s.name,**s.marks}
            rows.append(row)
        return pd.DataFrame(rows)

    def save(self):
        df=self.to_dataframe()
        df.to_csv(self.filename,index=False)

    def load(self):
        if not os.path.exists(self.filename):
            return "File not exist"
        df=pd.read_csv(self.filename,keep_default_na=False)
        self.students=[]
        for _, row in df.iterrows():
            marks={col: int(row[col]) for col in df.columns if col not in ("roll_no","name")}
            self.add_student(int(row["roll_no"]),row["name"], marks)

    def generate_sample_data(self,n=30,subjects=("Maths","Physcis","Chemistry","English","CS")):
        np.random.seed(42)
        self.students=[]
        marks_array=np.random.randint(20,101,size=(n,len(subjects )))

        for i,row in enumerate(marks_array,start=1):
            marks={subject:int(mark) for subject,mark in zip(subjects,row)}
            self.add_student(i,f"Student {i}",marks)

    def subject_stats(self):
        df=self.to_dataframe()
        marks_df=df.drop(columns=["name","roll_no"])

        rows=[]
        for subject in marks_df.columns:
            values=marks_df[subject]
            rows.append({
                "subject":subject,
                "average":np.mean(values),
                "max":np.max(values),
                "mean":np.min(values),
                "std_":np.std(values),
            })
        return pd.DataFrame(rows).round(2)

    def student_report(self):
        df=self.to_dataframe()
        marks_df=df.drop(columns=["name","roll_no"]) 
        total=marks_df.sum(axis=1)

        percetage=total/(100*len(marks_df.columns)) *100
        grade=np.select(
            [percetage>=75,percetage>=60,percetage>=40],
            ['A','B','C'],
            default="Fail"
        )

        report=pd.DataFrame({
            "roll_no":df["roll_no"],
            "name":df["name"],
            "total":total,
            "percentage":percetage,
            "grade":grade
        }
        )
        return report

    def rank_list(self):
        report=self.student_report()
        ranked=report.sort_values("percentage",ascending=False)
        ranked=ranked.reset_index(drop=True)
        ranked["rank"]=ranked.index +1
        return ranked

    def top_students(self,n=5):
        return self.rank_list().head(n)

    def pass_fail_counts(self):
        df=self.to_dataframe()
        mark_df=df.drop(columns=["name","roll_no"])

        rows=[]
        for subject in mark_df.columns:
            values=mark_df[subject]
            rows.append({
                "subject":subject,
                "passed":int(np.sum(values >=40)),
                "failed":int(np.sum(values<=40))
            })

        return pd.DataFrame(rows)



    def __len__(self):
        return len(self.students)


def main():
    book=Gradebook()
    book.load()

    while True:
        print("\n1. Add student")
        print("2. Show all students")
        print("3. Generate sample data")
        print("4. Subject stats")
        print("5. Top 5 students")
        print("6. Full rank list")
        print("7. Pass/fail count per subject")
        print("8. Quit")
        choice = input("Choose: ")

        if choice in ("2","4","5","6","7") and book.__len__()==0:
            print("There are no students")
            continue

        if choice=="1":
            roll_no=input("Roll no: ")
            name=input("NAME: ")
            marks={}
            count=int(input("How may sub: "))
            for _ in range(count):
                subject=input("Enter subject: ")
                marks[subject]= float(input(f"Enter marks in {subject}:"))
            try:
                book.add_student(roll_no,name,marks)
                book.save()
                print("Student added!")
            except ValueError as e:
                print("error",e)

        elif choice == "2":
            print(book.to_dataframe())

        elif choice == "3":
            confirm = input("This replaces all data. Continue? (y/n): ")
            if confirm.lower() == "y":
                book.generate_sample_data()
                book.save()
                print("Sample data generated!")

        elif choice == "4":
            print(book.subject_stats())

        elif choice == "5":
            print(book.top_students())

        elif choice == "6":
            print(book.rank_list())

        elif choice == "7":
            print(book.pass_fail_counts())

        elif choice == "8":
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

        

    
    