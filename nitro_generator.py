import random
import string
import threading
import tkinter as tk
from tkinter import scrolledtext
import time

# Global variables
generation_running = False
console_lock = threading.Lock()

# Function to generate a random Discord Nitro code
def generate_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    return code

# Function to start generating codes
def start_generation():
    global generation_running
    if not generation_running:
        generation_running = True
        threading.Thread(target=generate_codes_thread).start()
        status_label.config(text="Generating codes...", fg="blue")

# Function to stop generating codes
def stop_generation():
    global generation_running
    generation_running = False
    status_label.config(text="Generation stopped.", fg="orange")

# Function to generate codes in a separate thread
def generate_codes_thread():
    global generation_running
    while generation_running:
        code = generate_code()
        console_printer(f"Generated: discord.gift/{code}")
        save_to_file(f"discord.gift/{code}")
        time.sleep(1)  # Adjust delay as needed

# Function to print to console
def console_printer(message):
    with console_lock:
        output_text.insert(tk.END, f"{message}\n")
        output_text.see(tk.END)

# Function to save generated codes to file
def save_to_file(code):
    with open('generated_codes.txt', 'a+') as file:
        file.write(f"{code}\n")

# Function to animate the banner
def animate_banner():
    global banner_text
    banner_label.config(text=banner_text)
    banner_text = banner_text[1:] + banner_text[0]  # Rotate the text
    banner_label.after(200, animate_banner)  # Adjust speed of animation (milliseconds)

# Create main window
root = tk.Tk()
root.title("Discord Nitro Generator")

# Initial banner text (as a string)
banner_text = """
██████╗░██████╗░░█████╗░░██████╗░█████╗░██████╗░░░░░░░██╗███╗░░██╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗░░░░░░██║████╗░██║██╔══██╗
██║░░██║██║░░██║██║░░██║╚█████╗░██║░░██║██████╔╝█████╗██║██╔██╗██║██║░░██║
██║░░██║██║░░██║██║░░██║░╚═══██╗██║░░██║██╔═══╝░╚════╝██║██║╚████║██║░░██║
██████╔╝██████╔╝╚█████╔╝██████╔╝╚█████╔╝██║░░░░░░░░░░░██║██║░╚███║██████╔╝
╚═════╝░╚═════╝░░╚════╝░╚═════╝░░╚════╝░╚═╝░░░░░░░░░░░╚═╝╚═╝░░╚══╝╚═════╝░
"""

# Create and place widgets
banner_label = tk.Label(root, font=("Courier", 10), fg="purple")  # Setting text color to purple
banner_label.pack(pady=10)

start_button = tk.Button(root, text="Start Generation", command=start_generation)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Generation", command=stop_generation)
stop_button.pack(pady=5)

status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.pack(padx=10, pady=10)

# Initialize banner text (as a string)
banner_text = banner_text.strip()

# Start banner animation
animate_banner()

# Start the Tkinter event loop
root.mainloop()
