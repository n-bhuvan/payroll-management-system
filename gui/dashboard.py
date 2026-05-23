import customtkinter as ctk

from gui.employee import (open_add_employee,open_view_employees)

from database.db import connect_db

from analytics.analytics import (get_total_payroll,get_average_salary,get_highest_salary,show_department_chart)

def get_total_employees():
    connection=connect_db()
    cursor=connection.cursor()
    query="select count(*) from employees"
    cursor.execute(query)
    total=cursor.fetchone()[0]
    return total

def refresh_dashboard():

    total_employees = get_total_employees()

    total_payroll = get_total_payroll()

    average_salary = get_average_salary()

    highest_salary = get_highest_salary()

    employee_label.configure(
        text=f"Total Employees\n{total_employees}"
    )

    payroll_label.configure(
        text=f"Total Payroll\n₹{total_payroll}"
    )

    average_label.configure(
        text=f"Average Salary\n₹{average_salary}"
    )

    highest_label.configure(
        text=f"Highest Salary\n₹{highest_salary}"
    )
    

def open_dashboard(app):
    dashboard=ctk.CTkToplevel(app)

    dashboard.geometry("800x500")
    dashboard.title("Dashboard")
    dashboard.protocol("WM_DELETE_WINDOW",app.destroy)
    title=ctk.CTkLabel(dashboard,text="Welcome to the Smart Payroll Management System",font=ctk.CTkFont(size=20,weight="bold"))
    title.pack(pady=40)

    total_payroll = get_total_payroll()

    average_salary = get_average_salary()

    highest_salary = get_highest_salary()

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

    payroll_card = ctk.CTkFrame(
    main_frame,
    width=220,
    height=120
    )

    payroll_card.place(x=320, y=50)

    global payroll_label

    payroll_label = ctk.CTkLabel(
        payroll_card,
        text=f"Total Payroll\n₹{total_payroll}",
        font=("Arial", 20)
    )

    payroll_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    average_card = ctk.CTkFrame(
    main_frame,
    width=220,
    height=120
    )

    average_card.place(x=590, y=50)

    global average_label

    average_label = ctk.CTkLabel(
        average_card,
        text=f"Average Salary\n₹{average_salary}",
        font=("Arial", 18)
    )

    average_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    highest_card = ctk.CTkFrame(
    main_frame,
    width=220,
    height=120
    )

    highest_card.place(x=860, y=50)

    global highest_label

    highest_label = ctk.CTkLabel(
        highest_card,
        text=f"Highest Salary\n₹{highest_salary}",
        font=("Arial", 18)
    )

    highest_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    global employee_label

    employee_label = ctk.CTkLabel(
        employee_card,
        text="Total Employees\n0",
        font=("Arial", 20)
    )

    employee_label.place(relx=0.5, rely=0.5, anchor="center")
    refresh_dashboard()
    add_employee_button = ctk.CTkButton(
        main_frame,
        text="Add Employee",
        width=200,
        command=lambda: open_add_employee(app,refresh_dashboard)
    )

    

    add_employee_button.place(x=100, y=250)

    view_employee_button = ctk.CTkButton(
    main_frame,
    text="View Employees",
    width=200,
    command=lambda: open_view_employees(app,refresh_dashboard)
    )

    view_employee_button.place(x=400, y=250)

    chart_button = ctk.CTkButton(
    main_frame,
    text="Show Analytics Chart",
    width=220,
    command=show_department_chart
    )

    chart_button.place(x=700, y=250)

    refresh_dashboard()

    dashboard.mainloop()
