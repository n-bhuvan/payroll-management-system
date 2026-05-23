from tkinter import messagebox

import pandas as pd

import os

from database.db import connect_db


def export_employee_csv():

    try:

        connection = connect_db()

        cursor = connection.cursor()

        query = """
        SELECT employee_id,
               name,
               department,
               position,
               salary,
               bonus,
               deductions
        FROM employees
        """

        cursor.execute(query)

        employees = cursor.fetchall()

        if not employees:

            messagebox.showwarning(
                "No Data",
                "No employee data available to export"
            )

            return

        columns = [
            "Employee ID",
            "Name",
            "Department",
            "Position",
            "Salary",
            "Bonus",
            "Deductions"
        ]

        df = pd.DataFrame(
            employees,
            columns=columns
        )

        os.makedirs(
            "reports",
            exist_ok=True
        )

        file_path = os.path.abspath(
            os.path.join(
                "reports",
                "employee_report.csv"
            )
        )

        df.to_csv(
            file_path,
            index=False
        )

        messagebox.showinfo(
            "Export Successful",
            f"CSV Report Exported Successfully!\n\nLocation:\n{file_path}"
        )

        cursor.close()

        connection.close()

    except Exception as e:

        messagebox.showerror(
            "Export Error",
            str(e)
        )