import tkinter as tk
from tkinter import messagebox, simpledialog
from db import create_db, add_user, get_user_credentials
from admin_dashboard import AdminDashboard
from user_dashboard import UserDashboard

create_db()

class MainApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hotel Management System")
        self.window.geometry("400x300")

        tk.Label(self.window, text="Hotel Management System", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.window, text="Admin Login", command=self.admin_login).pack(pady=10)
        tk.Button(self.window, text="User Login", command=self.user_login).pack(pady=10)
        tk.Button(self.window, text="Register New User", command=self.register_user).pack(pady=10)

    def admin_login(self):
        username = simpledialog.askstring("Admin Login", "Enter admin username:")
        password = simpledialog.askstring("Admin Login", "Enter admin password:", show="*")

        if username == "admin" and password == "admin":
            self.window.destroy()
            AdminDashboard().run()
        else:
            messagebox.showerror("Error", "Invalid admin credentials")

    def user_login(self):
        username = simpledialog.askstring("User Login", "Enter username:")
        password = simpledialog.askstring("User Login", "Enter password:", show="*")

        user = get_user_credentials(username, password)
        if user:
            self.window.destroy()
            UserDashboard(user[0]).run()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register_user(self):
        username = simpledialog.askstring("Register", "Enter a username:")
        contact = simpledialog.askstring("Register", "Enter contact information:")
        password = simpledialog.askstring("Register", "Enter a password:", show="*")

        if username and contact and password:
            success = add_user(username, contact, password)
            if success:
                messagebox.showinfo("Registration Successful", "User registered successfully!")
            else:
                messagebox.showerror("Registration Failed", "Username already exists.")
        else:
            messagebox.showerror("Error", "All fields are required")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    MainApp().run()
