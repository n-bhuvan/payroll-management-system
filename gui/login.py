import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

from database.db import connect_db

from gui.dashboard import open_dashboard



def login_page(app):

    def login():
        username=username_entry.get()
        password=password_entry.get()

        print(username,password)

        try:
            connection=connect_db()

            if not username.strip() or not password.strip():

                messagebox.showwarning(
                    "Missing Login",
                    "Please enter username and password"
                )

                username_entry.delete(0, "end")

                password_entry.delete(0, "end")

                return

            print("Connected Successfully")
            cursor=connection.cursor()

            query="select * from admins where username=%s and password=%s"
            

            cursor.execute(query,(username,password))

            result=cursor.fetchone()
            print(result)

            if result:
                app.withdraw()
                open_dashboard(app)
            else:
                messagebox.showwarning("Login Failed","Invalid Username or Password")
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
