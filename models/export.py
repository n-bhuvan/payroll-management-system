import pandas as pd

import os

from database.db import connect_db

from models.payroll import calculate_net_salary


def export_employee_csv():

    connection = connect_db()

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

    df = pd.read_sql(query, connection)

    connection.close()
    if df.empty:

        raise Exception(
            "No employee data available to export"
        )

    df["net_salary"] = df.apply(
        lambda row: calculate_net_salary(
            row["salary"],
            row["bonus"],
            row["deductions"]
        ),
        axis=1
    )

    os.makedirs("reports", exist_ok=True)

    file_path = os.path.join(
        "reports",
        "employee_report.csv"
    )

    df.to_csv(
        file_path,
        index=False
    )

    return file_path