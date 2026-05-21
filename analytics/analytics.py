from database.db import connect_db



import matplotlib.pyplot as plt


def show_department_chart():

    connection = connect_db()

    cursor = connection.cursor()

    query = """
    SELECT department,
           COUNT(*)
    FROM employees
    GROUP BY department
    """

    cursor.execute(query)

    data = cursor.fetchall()

    departments = []
    counts = []

    for row in data:

        departments.append(row[0])

        counts.append(row[1])

    plt.figure(figsize=(8, 5))

    plt.bar(departments, counts)

    plt.title("Department-wise Employee Count")

    plt.xlabel("Department")

    plt.ylabel("Employees")

    plt.show()

def get_total_payroll():

    connection = connect_db()

    cursor = connection.cursor()

    query = """
    SELECT SUM(
        salary + bonus - deductions
    )
    FROM employees
    """

    cursor.execute(query)

    result = cursor.fetchone()[0]

    return result if result else 0


def get_average_salary():

    connection = connect_db()

    cursor = connection.cursor()

    query = """
    SELECT AVG(salary)
    FROM employees
    """

    cursor.execute(query)

    result = cursor.fetchone()[0]

    return round(result, 2) if result else 0


def get_highest_salary():

    connection = connect_db()

    cursor = connection.cursor()

    query = """
    SELECT MAX(salary)
    FROM employees
    """

    cursor.execute(query)

    result = cursor.fetchone()[0]

    return result if result else 0