from database.db import connect_db


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