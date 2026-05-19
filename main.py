import customtkinter as ctk

ctk.set_appearance_mode("dark")

app=ctk.CTk()
app.geometry("800x500")
app.title("Smart Payroll Management System")

title=ctk.CTkLabel(app,text="Smart Payroll Management System",font=ctk.CTkFont(size=20,weight="bold"))

title.pack(pady=40)

username_entry=ctk.CTkEntry(app,placeholder_text="Username",width=250)

username_entry.pack(pady=10)

password_entry=ctk.CTkEntry(app,placeholder_text="Password",width=250,show="*")
password_entry.pack(pady=10)
login_button=ctk.CTkButton(app,text="Login")

login_button.pack(pady=20)

app.mainloop()