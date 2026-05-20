import customtkinter as ctk


def open_dashboard(app):
    dashboard=ctk.CTkToplevel(app)

    dashboard.geometry("800x500")
    dashboard.title("Dashboard")
    dashboard.protocol("WM_DELETE_WINDOW",app.destroy)
    title=ctk.CTkLabel(dashboard,text="Welcome to the Smart PayrollDashboard",font=ctk.CTkFont(size=20,weight="bold"))
    title.pack(pady=40)

    