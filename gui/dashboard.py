import customtkinter as ctk

from gui.employee import (open_add_employee,open_view_employees)

from database.db import connect_db

def get_total_employees():
    connection=connect_db()
    cursor=connection.cursor()
    query="select count(*) from employees"
    cursor.execute(query)
    total=cursor.fetchone()[0]
    return total

def refresh_employee_count():

    total = get_total_employees()

    employee_label.configure(
        text=f"Total Employees\n{total}"
)

def open_dashboard(app):
    dashboard=ctk.CTkToplevel(app)

    dashboard.geometry("800x500")
    dashboard.title("Dashboard")
    dashboard.protocol("WM_DELETE_WINDOW",app.destroy)
    title=ctk.CTkLabel(dashboard,text="Welcome to the Smart Payroll Management System",font=ctk.CTkFont(size=20,weight="bold"))
    title.pack(pady=40)

    main_frame = ctk.CTkFrame(
        dashboard,
        width=1100,
        height=550
    )

    main_frame.pack(pady=20)

    employee_card = ctk.CTkFrame(
        main_frame,
        width=200,
        height=120
    )

    employee_card.place(x=50, y=50)

    global employee_label

    employee_label = ctk.CTkLabel(
        employee_card,
        text="Total Employees\n0",
        font=("Arial", 20)
    )

    employee_label.place(relx=0.5, rely=0.5, anchor="center")
    refresh_employee_count()
    add_employee_button = ctk.CTkButton(
        main_frame,
        text="Add Employee",
        width=200,
        command=lambda: open_add_employee(app,refresh_employee_count)
    )

    

    add_employee_button.place(x=100, y=250)

    view_employee_button = ctk.CTkButton(
    main_frame,
    text="View Employees",
    width=200,
    command=lambda: open_view_employees(app)
    )

    view_employee_button.place(x=400, y=250)

    dashboard.mainloop()