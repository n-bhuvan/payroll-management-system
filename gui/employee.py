import customtkinter as ctk

from tkinter import messagebox

from database.db import connect_db


def save_employee(
    name,
    department,
    position,
    salary,
    bonus,
    deductions
):

    try:

        connection = connect_db()

        cursor = connection.cursor()

        query = """
        INSERT INTO employees
        (name, department, position, salary, bonus, deductions)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            name,
            department,
            position,
            salary,
            bonus,
            deductions
        )

        cursor.execute(query, values)

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Employee Added Successfully!"
        )
        
    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )
        

def open_add_employee(app,referesh_callback):

    employee_window = ctk.CTkToplevel(app)
    

    employee_window.geometry("500x650")

    employee_window.title("Add Employee")
    employee_window.attributes("-topmost", True)
    employee_window.focus_force()
    employee_window.after(
    100,
    lambda: employee_window.attributes("-topmost", False)
    )
    title = ctk.CTkLabel(
        employee_window,
        text="Add Employee",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    name_entry = ctk.CTkEntry(
        employee_window,
        placeholder_text="Employee Name",
        width=300
    )

    name_entry.pack(pady=10)

    department_entry = ctk.CTkEntry(
        employee_window,
        placeholder_text="Department",
        width=300
    )

    department_entry.pack(pady=10)

    position_entry = ctk.CTkEntry(
        employee_window,
        placeholder_text="Position",
        width=300
    )

    position_entry.pack(pady=10)

    salary_entry = ctk.CTkEntry(
        employee_window,
        placeholder_text="Salary",
        width=300
    )

    salary_entry.pack(pady=10)

    bonus_entry = ctk.CTkEntry(
        employee_window,
        placeholder_text="Bonus",
        width=300
    )

    bonus_entry.pack(pady=10)

    deduction_entry = ctk.CTkEntry(
        employee_window,
        placeholder_text="Deductions",
        width=300
    )

    deduction_entry.pack(pady=10)

    def submit_employee():

        name = name_entry.get()
        department = department_entry.get()
        position = position_entry.get()
        salary = salary_entry.get()
        bonus = bonus_entry.get()
        deductions = deduction_entry.get()

        save_employee(
            name,
            department,
            position,
            salary,
            bonus,
            deductions
        )
        name_entry.delete(0, "end")

        department_entry.delete(0, "end")

        position_entry.delete(0, "end")

        salary_entry.delete(0, "end")

        bonus_entry.delete(0, "end")

        deduction_entry.delete(0, "end")

        referesh_callback()

    save_button = ctk.CTkButton(
        employee_window,
        text="Save Employee",
        width=200,
        command=submit_employee
    )

    save_button.pack(pady=20)

    employee_window.mainloop()
    

def open_view_employees(app):

    view_window = ctk.CTkToplevel(app)

    view_window.geometry("900x500")

    view_window.title("View Employees")

    view_window.attributes("-topmost", True)
    view_window.focus_force()
    view_window.after(
    100,
    lambda: view_window.attributes("-topmost", False)
    )

    title = ctk.CTkLabel(
        view_window,
        text="Employee Records",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    table_frame = ctk.CTkFrame(view_window)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    headers = [
        "ID",
        "Name",
        "Department",
        "Position",
        "Salary"
    ]

    for col, header in enumerate(headers):

        header_label = ctk.CTkLabel(
            table_frame,
            text=header,
            font=("Arial", 18, "bold"),
            width=150
        )

        header_label.grid(
            row=0,
            column=col,
            padx=10,
            pady=10
        )

    try:

        connection = connect_db()

        cursor = connection.cursor()

        query = """
        SELECT employee_id,
               name,
               department,
               position,
               salary
        FROM employees
        """

        cursor.execute(query)

        employees = cursor.fetchall()

        for row_num, employee in enumerate(
            employees,
            start=1
        ):

            for col_num, value in enumerate(employee):

                data_label = ctk.CTkLabel(
                    table_frame,
                    text=str(value),
                    font=("Arial", 16),
                    width=150
                )

                data_label.grid(
                    row=row_num,
                    column=col_num,
                    padx=10,
                    pady=5
                )
        

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
    )

        