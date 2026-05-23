from tkinter import messagebox

import customtkinter as ctk

from gui.employee import (open_add_employee,open_view_employees)

from database.db import connect_db

from analytics.analytics import (get_total_payroll,get_average_salary,get_highest_salary,show_department_chart)

from models.export import export_employee_csv

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

    dashboard.geometry("1200x720")
    dashboard.minsize(1000, 600)
    dashboard.title("Dashboard")
    sidebar = ctk.CTkFrame(
        dashboard,
        width=180,
        height=700,
        corner_radius=0
    )

    sidebar_title = ctk.CTkLabel(
        sidebar,
        text="Payroll System",
        font=("Arial", 20, "bold")
    )

    sidebar_title.pack(pady=20)
    sidebar.pack(
        side="left",
        fill="y"
    )
    dashboard.protocol("WM_DELETE_WINDOW",app.destroy)
    title=ctk.CTkLabel(dashboard,text="Welcome to the Smart Payroll Management System",font=("Arial", 26, "bold"))
    title.pack(pady=25)
    

    total_payroll = get_total_payroll()

    average_salary = get_average_salary()

    highest_salary = get_highest_salary()

    main_frame = ctk.CTkFrame(
        dashboard,
        width=1000,
        height=320
    )

    main_frame.grid_columnconfigure(
        (0, 1, 2, 3),
        weight=1
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    employee_card = ctk.CTkFrame(
        main_frame,
        width=180,
        height=100,
        corner_radius=20
    )

    employee_card.grid(
        row=0,
        column=0,
        padx=15,
        pady=20
    )

    payroll_card = ctk.CTkFrame(
    main_frame,
    width=180,
    height=100,
    corner_radius=20
    )

    payroll_card.grid(
        row=0,
        column=1,
        padx=15,
        pady=20
    )

    global payroll_label

    payroll_label = ctk.CTkLabel(
        payroll_card,
        text=f"Total Payroll\n₹{total_payroll}",
        font=("Arial", 18, "bold")
    )

    payroll_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    average_card = ctk.CTkFrame(
    main_frame,
    width=180,
    height=100,
    corner_radius=20
    )

    average_card.grid(
        row=0,
        column=2,
        padx=15,
        pady=20
    )

    global average_label

    average_label = ctk.CTkLabel(
        average_card,
        text=f"Average Salary\n₹{average_salary}",
        font=("Arial",18, "bold")
    )

    average_label.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    highest_card = ctk.CTkFrame(
    main_frame,
    width=180,
    height=100,
    corner_radius=20
    )

    highest_card.grid(
        row=0,
        column=3,
        padx=15,
        pady=20
    )

    global highest_label

    highest_label = ctk.CTkLabel(
        highest_card,
        text=f"Highest Salary\n₹{highest_salary}",
        font=("Arial",18, "bold")
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
        font=("Arial", 18, "bold")
    )

    employee_label.place(relx=0.5, rely=0.5, anchor="center")
    refresh_dashboard()


    add_employee_button = ctk.CTkButton(
        sidebar,
        text="Add Employee",
        width=160,
        command=lambda: open_add_employee(app,refresh_dashboard),
        corner_radius=12,
        height=45,
        font=("Arial", 13, "bold")
    )

    add_employee_button.pack(
        pady=10,
        padx=20
    )

    view_employee_button = ctk.CTkButton(
    sidebar,
    text="Employees",
    width=160,
    command=lambda: open_view_employees(app,refresh_dashboard),
    corner_radius=12,
    height=45,
    font=("Arial", 13, "bold")
    )

    view_employee_button.pack(
        pady=10,
        padx=20
    )

    chart_button = ctk.CTkButton(
    sidebar,
    text="Analytics",
    width=160,
    command=show_department_chart,
    corner_radius=12,
    height=45,
    font=("Arial", 13, "bold")
    )

    chart_button.pack(
        pady=10,
        padx=20
    )

    export_button = ctk.CTkButton(
        sidebar,
        text="Export CSV",
        width=160,
        height=45,
        corner_radius=12,
        font=("Arial", 13, "bold"),
        command=export_employee_csv
    )

    export_button.pack(
        pady=10,
        padx=20
    )



    logout_button = ctk.CTkButton(
        sidebar,
        text="Logout",
        width=150,
        height=45,
        corner_radius=12,
        fg_color="red",
        hover_color="darkred",
        font=("Arial", 13, "bold"),
        command=dashboard.destroy
    )
    logout_button.pack(
        pady=20,
        padx=20
    )

    footer = ctk.CTkFrame(
        dashboard,
        height=40,
        corner_radius=0
    )

    footer.pack(
        side="bottom",
        fill="x"
    )

    footer_label = ctk.CTkLabel(
        footer,
        text="Smart Payroll Management System | Version 1.0 | Developed by G N Bhuvaneshwaran",
        font=("Arial", 10)
    )

    footer_label.pack(pady=8)

    refresh_dashboard()

    dashboard.mainloop()
