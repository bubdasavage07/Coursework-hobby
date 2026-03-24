import tkinter as tk
from tkinter import messagebox, Frame, Label, ttk
from PIL import Image, ImageTk

def on_button_click(weapon_name):
    print(f"{weapon_name} selected!")

# Create main window
window = tk.Tk()
window.title("Zombie HUD")
window.geometry("850x700")
window.configure(background="#1a1a1a")  # Darker background for a "horror" feel

# --- 1. TITLE ---
title_label = tk.Label(window, text="BRAIN RAIDERS", font=("Chiller", 50, "bold"), fg="#39FF14", bg="#1a1a1a")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# --- 2. IMAGE SECTION ---
image_frame = Frame(window, bg="black", highlightbackground="#39FF14", highlightthickness=2)
image_frame.grid(row=1, column=0, columnspan=2, pady=20)

try:
    image_path = "C:\\Users\\jvo101\\Documents\\IST 140 - Spring 2026 Python\\pfg_logo.png"
    image = Image.open(image_path)
    image = image.resize((700, 250))
    photo_image = ImageTk.PhotoImage(image)
    image_label = Label(image_frame, image=photo_image, bg="black")
    image_label.grid()
except:
    # Placeholder if the image file isn't found
    placeholder = Label(image_frame, text="[ LOGO PLACEHOLDER ]", fg="white", bg="black", width=60, height=10)
    placeholder.grid()

# --- 3. PLAYER STATS BOX ---
stats_box = ttk.LabelFrame(window, text=" PLAYER STATS ")
stats_box.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

# We use labels inside the stats_box
tk.Label(stats_box, text="Health: 100%", font=("Courier", 12), fg="red").grid(row=0, column=0, sticky="w", padx=10)
tk.Label(stats_box, text="Kill Count: 0", font=("Courier", 12)).grid(row=1, column=0, sticky="w", padx=10)
tk.Label(stats_box, text="Bottle Caps: 50", font=("Courier", 12), fg="blue").grid(row=2, column=0, sticky="w", padx=10)

# --- 4. WEAPON SELECT BOX ---
weapon_box = ttk.LabelFrame(window, text=" WEAPON SELECT ")
weapon_box.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

weapons = [
    ("Fists", "btn1"), 
    ("Pipe Wrench", "btn2"), 
    ("Pepper Spray", "btn3"), 
    ("AR-15", "btn4"), 
    ("F-Nuke", "btn5")
]

for i, (name, id) in enumerate(weapons):
    btn = ttk.Button(weapon_box, text=name, command=lambda n=name: on_button_click(n))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)

# --- 5. ACTION AREA ---
attack_btn = tk.Button(window, text="UNLEASH ATTACK", font=("Impact", 20), bg="red", fg="white", 
                       activebackground="darkred", command=lambda: print("Attacking!"))
attack_btn.grid(row=3, column=0, columnspan=2, pady=30, ipadx=50)

# Configure grid weights so things center nicely
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

window.mainloop()