import pyshorteners
import tkinter as tk
from tkinter import messagebox

# Function to shorten the URL using the selected service
def shorten_url():
    long_url = url_entry.get()
    service = service_var.get()
    try:
        shortener = pyshorteners.Shortener()
        if service == "TinyURL":
            short_url = shortener.tinyurl.short(long_url)
        elif service == "Bitly":
            short_url = shortener.bitly.short(long_url)  # Note: Requires API key configuration
        else:
            short_url = shortener.tinyurl.short(long_url)  # Default to TinyURL
        
        result_label.config(text=f"Short URL: {short_url}")
        copy_button.config(state=tk.NORMAL)  # Enable the copy button
        result_label.short_url = short_url  # Store the short URL in the label for easy access
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to copy the short URL to the clipboard
def copy_to_clipboard():
    short_url = result_label.short_url
    app.clipboard_clear()
    app.clipboard_append(short_url)
    messagebox.showinfo("Copied", "Short URL copied to clipboard")

# Initialize the GUI application
app = tk.Tk()
app.title("URL Shortener")

# URL input
tk.Label(app, text="Enter the long URL:").pack(pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

# Service selection
service_var = tk.StringVar(value="TinyURL")
tk.Label(app, text="Select the shortening service:").pack(pady=5)
tk.Radiobutton(app, text="TinyURL", variable=service_var, value="TinyURL").pack(anchor=tk.W)
tk.Radiobutton(app, text="Bitly", variable=service_var, value="Bitly").pack(anchor=tk.W)

# Shorten button
shorten_button = tk.Button(app, text="Shorten URL", command=shorten_url)
shorten_button.pack(pady=20)

# Result label
result_label = tk.Label(app, text="")
result_label.pack(pady=5)
result_label.short_url = ""  # Attribute to store the short URL

# Copy button
copy_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard, state=tk.DISABLED)
copy_button.pack(pady=5)

# Run the application
app.mainloop()
