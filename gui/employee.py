

import customtkinter as ctk

from tkinter import messagebox

from database.db import connect_db

from models.payroll import calculate_net_salary

from models.payslip import generate_payslip

from models.export import export_employee_csv

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
        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Employee Added Successfully!"
        )
        
    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )
        

def open_add_employee(app,refresh_callback):

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

        if (
            not name
            or not department
            or not position
            or not salary
            or not bonus
            or not deductions
        ):

            messagebox.showwarning(
                "Missing Data",
                "Please fill all fields"
            )

            return
        
        try:

            salary = float(salary)

            bonus = float(bonus)

            deductions = float(deductions)

        except:

            messagebox.showerror(
                "Invalid Input",
                "Salary, Bonus and Deductions must be numbers"
            )

            return
        
        if (
            salary < 0
            or bonus < 0
            or deductions < 0
        ):

            messagebox.showwarning(
                "Invalid Amount",
                "Values cannot be negative"
            )

            return
        
        if deductions > (salary + bonus):

            messagebox.showwarning(
                "Invalid Payroll",
                "Deductions cannot exceed total earnings"
            )

            return

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

        if refresh_callback:
            refresh_callback()

    save_button = ctk.CTkButton(
        employee_window,
        text="Save Employee",
        width=200,
        command=submit_employee
    )

    save_button.pack(pady=20)

    employee_window.mainloop()
    

def open_view_employees(app,refresh_callback=None):

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
    table_frame.pack(pady=10)

    

    search_entry = ctk.CTkEntry(
        view_window,
        placeholder_text="Search Employee Name",
        width=250
    )

    search_entry.pack(pady=10)

    search_button = ctk.CTkButton(
        view_window,
        text="Search",
        width=150,
        command=lambda: search_employee(
            table_frame,
            search_entry.get()
        )
    )

    search_button.pack(pady=10)

    update_button = ctk.CTkButton(
    view_window,
    text="Update Employee",
    width=200,
    command=lambda: open_update_employee(app,refresh_callback)
    )

    update_button.pack(pady=10)
    

    delete_button = ctk.CTkButton(
    view_window,
    text="Delete Employee",
    width=200,
    fg_color="red",
    hover_color="darkred",
    command=lambda: open_delete_employee(app, refresh_callback)
    )

    delete_button.pack(pady=10)

    payslip_button = ctk.CTkButton(
        view_window,
        text="Generate Payslip",
        width=220,
        command=lambda: open_payslip_window(app)
    )

    payslip_button.pack(pady=10)

    export_button = ctk.CTkButton(
        view_window,
        text="Export CSV Report",
        width=220,
        command=export_csv
    )

    export_button.pack(pady=10)

    headers = [
    "ID",
    "Name",
    "Department",
    "Position",
    "Salary",
    "Bonus",
    "Deductions",
    "Net Salary"
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
            salary,
            bonus,
            deductions
            FROM employees
        """

        cursor.execute(query)

        employees = cursor.fetchall()
        cursor.close()
        connection.close()

        for row_num, employee in enumerate(
            employees,
            start=1
        ):

            salary = employee[4]

            bonus = employee[5]

            deductions = employee[6]

            net_salary = calculate_net_salary(
                salary,
                bonus,
                deductions
            )

            employee = list(employee)

            employee.append(net_salary)
            
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
        
def open_update_employee(app,refresh_callback=None):

    update_window = ctk.CTkToplevel(app)

    update_window.geometry("500x700")

    update_window.title("Update Employee")

    update_window.attributes("-topmost", True)
    update_window.focus_force()
    update_window.after(
    100,
    lambda: update_window.attributes("-topmost", False)
    )

    title = ctk.CTkLabel(
        update_window,
        text="Update Employee",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    id_entry = ctk.CTkEntry(
        update_window,
        placeholder_text="Employee ID",
        width=300
    )

    id_entry.pack(pady=10)

    name_entry = ctk.CTkEntry(
        update_window,
        placeholder_text="New Name",
        width=300
    )

    name_entry.pack(pady=10)

    department_entry = ctk.CTkEntry(
        update_window,
        placeholder_text="New Department",
        width=300
    )

    department_entry.pack(pady=10)

    position_entry = ctk.CTkEntry(
        update_window,
        placeholder_text="New Position",
        width=300
    )

    position_entry.pack(pady=10)

    salary_entry = ctk.CTkEntry(
        update_window,
        placeholder_text="New Salary",
        width=300
    )

    salary_entry.pack(pady=10)

    bonus_entry = ctk.CTkEntry(
        update_window,
        placeholder_text="New Bonus",
        width=300
    )

    bonus_entry.pack(pady=10)

    deduction_entry = ctk.CTkEntry(
        update_window,
        placeholder_text="New Deductions",
        width=300
    )

    deduction_entry.pack(pady=10)

    def update_employee():

        try:

            connection = connect_db()

            cursor = connection.cursor()

            query = """
            UPDATE employees
            SET name=%s,
                department=%s,
                position=%s,
                salary=%s,
                bonus=%s,
                deductions=%s
            WHERE employee_id=%s
            """

            values = (
                name_entry.get(),
                department_entry.get(),
                position_entry.get(),
                salary_entry.get(),
                bonus_entry.get(),
                deduction_entry.get(),
                id_entry.get()
            )

            cursor.execute(query, values)

            connection.commit()
            if refresh_callback:
                refresh_callback()
            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Employee Updated Successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    update_btn = ctk.CTkButton(
        update_window,
        text="Update Employee",
        width=200,
        command=update_employee
    )
    update_btn.pack(pady=20)

def open_delete_employee(app,refresh_callback=None):

    delete_window = ctk.CTkToplevel(app)

    delete_window.geometry("400x300")

    delete_window.title("Delete Employee")

    delete_window.attributes("-topmost",True)
    delete_window.focus_force()
    delete_window.after(
        100,
        lambda: delete_window.attributes("-topmost",False)
    )

    title = ctk.CTkLabel(
        delete_window,
        text="Delete Employee",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    id_entry = ctk.CTkEntry(
        delete_window,
        placeholder_text="Employee ID",
        width=250
    )

    id_entry.pack(pady=20)

    def delete_employee():

        employee_id = id_entry.get()

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this employee?"
        )

        if not confirm:
            return

        try:

            connection = connect_db()

            cursor = connection.cursor()

            query = """
            DELETE FROM employees
            WHERE employee_id=%s
            """

            cursor.execute(query, (employee_id,))

            connection.commit()
            cursor.close()
            connection.close()
            
            if refresh_callback:
                refresh_callback()

            messagebox.showinfo(
                "Success",
                "Employee Deleted Successfully!"
            )

            delete_window.destroy()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    delete_btn = ctk.CTkButton(
        delete_window,
        text="Delete Employee",
        width=200,
        fg_color="red",
        hover_color="darkred",
        command=delete_employee
    )

    delete_btn.pack(pady=20)

def open_payslip_window(app):

    payslip_window = ctk.CTkToplevel(app)
    

    payslip_window.geometry("400x300")
    

    payslip_window.title("Generate Payslip")

    payslip_window.attributes("-topmost",True)
    payslip_window.focus_force()
    payslip_window.after(
        100,lambda:payslip_window.attributes("-topmost",False)
    )

    

    title = ctk.CTkLabel(
        payslip_window,
        text="Generate Payslip",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    id_entry = ctk.CTkEntry(
        payslip_window,
        placeholder_text="Employee ID",
        width=250
    )

    id_entry.pack(pady=20)

    def generate_pdf():

        employee_id = id_entry.get()

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
            WHERE employee_id=%s
            """

            cursor.execute(query, (employee_id,))

            employee = cursor.fetchone()

            cursor.close()
            connection.close()

            if employee:

                file_name = generate_payslip(employee)

                messagebox.showinfo(
                    "Success",
                    f"Payslip Generated!\n{file_name}"
                )

            else:

                messagebox.showwarning(
                    "Not Found",
                    "Employee ID not found"
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    generate_button = ctk.CTkButton(
        payslip_window,
        text="Generate PDF",
        width=200,
        command=generate_pdf
    )

    generate_button.pack(pady=20)

def search_employee(table_frame, search_value):

    for widget in table_frame.winfo_children():

        widget.destroy()

    headers = [
        "ID",
        "Name",
        "Department",
        "Position",
        "Salary",
        "Bonus",
        "Deductions",
        "Net Salary"
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
               salary,
               bonus,
               deductions
        FROM employees
        WHERE name LIKE %s
        """

        cursor.execute(
            query,
            (f"%{search_value}%",)
        )

        employees = cursor.fetchall()
        cursor.close()
        connection.close()

        for row_num, employee in enumerate(
            employees,
            start=1
        ):

            salary = employee[4]

            bonus = employee[5]

            deductions = employee[6]

            net_salary = calculate_net_salary(
                salary,
                bonus,
                deductions
            )

            employee = list(employee)

            employee.append(net_salary)

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

def export_csv():

    try:

        file_path = export_employee_csv()

        messagebox.showinfo(
            "Export Successful",
            f"CSV Report Saved!\n{file_path}"
        )

    except Exception as e:

        messagebox.showerror(
            "Export Error",
            str(e)
        )
    


