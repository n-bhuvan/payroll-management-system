import customtkinter as ctk

from gui.login import login_page

ctk.set_appearance_mode("dark")

app=ctk.CTk()

app.geometry("800x500")

app.title("Smart Payroll Management System")

login_page(app)

app.mainloop()