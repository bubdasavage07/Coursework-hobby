import tkinter as tk

# Define the action for the button click
def increment_counter():
    global clicks
    clicks += 1
    # Update the text of the existing label
    counter_label.config(text=f"Button clicked: {clicks} times")

# Initialize counts
clicks = 0

# Create window
root = tk.Tk()
root.title("Interactive Counter")
root.geometry("350x250")

# Headline instruction label
title_label = tk.Label(root, text="Click the button below:", font=("Arial", 12))
title_label.pack(pady=15)

# Dynamic text label that changes on click
counter_label = tk.Label(root, text="Button clicked: 0 times", font=("Arial", 14, "bold"), fg="blue")
counter_label.pack(pady=10)

# Clickable Button widget
# Note: Use the function name without parentheses for the command argument
click_button = tk.Button(root, text="Click Me!", command=increment_counter, font=("Arial", 11), padx=10, pady=5)
click_button.pack(pady=20)

root.mainloop()
