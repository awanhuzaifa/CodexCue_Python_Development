import tkinter as tk
from tkinter import messagebox

# Function to handle button clicks
def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = str(eval(screen.get()))
            screen.set(result)
        except ZeroDivisionError:
            screen.set("Error")
            messagebox.showerror("Error", "Division by zero is not allowed.")
        except Exception as e:
            screen.set("Error")
            messagebox.showerror("Error", f"Invalid input: {e}")
    elif text == "C":
        screen.set("")
    else:
        current = screen.get()
        screen.set(current + text)

# Initialize the main window
root = tk.Tk()
root.title("Calculator")
root.geometry("400x600")
root.configure(bg="#333333")

# Screen color customization
screen = tk.StringVar()
entry = tk.Entry(root, textvar=screen, font=("Arial", 24), bd=10, insertwidth=4, width=14, borderwidth=4, bg="#222222", fg="#FFFFFF")
entry.grid(row=0, column=0, columnspan=4, pady=20)

# Define button properties
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

row_val = 1
col_val = 0

# Button color customization
button_bg = "#444444"   # Button background color
button_fg = "#FFFFFF"   # Button text color
active_bg = "#555555"   # Active button background color

# Create and place buttons
for button in buttons:
    btn = tk.Button(root, text=button, font=("Arial", 18), padx=20, pady=20, bg=button_bg, fg=button_fg, activebackground=active_bg)
    btn.grid(row=row_val, column=col_val, padx=5, pady=5, sticky="nsew")
    btn.bind("<Button-1>", click)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Adjust the button grid to expand evenly
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(5):
    root.grid_rowconfigure(i, weight=1)

# Run the main loop
root.mainloop()
