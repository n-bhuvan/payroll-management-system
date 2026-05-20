import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

ctk.set_appearance_mode("dark")

app=ctk.CTk()
app.geometry("800x500")
app.title("Smart Payroll Management System")

def login():
    username=username_entry.get()
    password=password_entry.get()

    print(username,password)

    try:
        connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="payroll_system"
        )
        print("Connected Successfully")
        cursor=connection.cursor()

        query="select * from admins where username=%s and password=%s"
        

        cursor.execute(query,(username,password))

        result=cursor.fetchone()
        print(result)

        if result:
            messagebox.showinfo("Login Successful!")
        else:
            messagebox.showerror("Invalid username or password",text="Please enter correct information")
    except Exception as e:
        print(e)
        messagebox.showerror("Database Error",str(e))

    
title=ctk.CTkLabel(app,text="Smart Payroll Management System",font=ctk.CTkFont(size=20,weight="bold"))

title.pack(pady=40)

username_entry=ctk.CTkEntry(app,placeholder_text="Username",width=250)

username_entry.pack(pady=10)

password_entry=ctk.CTkEntry(app,placeholder_text="Password",width=250,show="*")
password_entry.pack(pady=10)
login_button=ctk.CTkButton(app,command=login,text="Login")

login_button.pack(pady=20)

app.mainloop()