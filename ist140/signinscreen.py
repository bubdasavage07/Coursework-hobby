import tkinter as tk
from tkinter import messagebox

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Success", "Welcome!")
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials")

# Create main window
window = tk.Tk()
window.title("Login")
window.geometry("300x200")
window.configure(background="#FF66AA")

# Username
tk.Label(window, text="Username").pack()
username_entry = tk.Entry(window)
username_entry.pack()

# Password
tk.Label(window, text="Password").pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# Login Button
tk.Button(window, text="Login", command=validate_login).pack()

window.mainloop()
