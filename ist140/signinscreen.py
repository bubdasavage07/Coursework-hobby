import tkinter as tk
from tkinter import messagebox, Frame
from PIL import Image, ImageTk

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
window.geometry("400x500")
window.configure(background="#FF66AA")

frame = Frame(window, width=300, height=300, bg="white")
frame.pack(pady=20)

image_path = "/Users/ethan/PFGgamer.png"

image = Image.open(image_path)
image = image.resize((300, 300))

photo_image = ImageTk.PhotoImage(image)

image_label = tk.Label(frame, image=photo_image)
image_label.image = photo_image

image_label.pack()


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
