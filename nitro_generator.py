import os
import random
import threading
import requests
from tkinter import Tk, Label, scrolledtext, END
import time

# Global variables
generation_running = True
console_lock = threading.Lock()

# Ensure 'results' directory exists if it doesn't already
if not os.path.exists('results'):
    os.makedirs('results')

class Console():
    def __init__(self):
        self.generated_codes_file = 'results/generated_codes.txt'

    def printer(self, status, code):
        with console_lock:
            output_text.insert(END, f"{status} > discord.gift/{code}\n")
            output_text.see(END)
            output_text.update()
        
        # Save generated code to file
        with open(self.generated_codes_file, 'a+') as f:
            f.write(f"discord.gift/{code}\n")

class Worker():
    def run(self):
        global generation_running
        while generation_running:
            self.code = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(16))
            Console().printer("Generated", self.code)  # Log generated code
            try:
                req = requests.get(
                    f'https://discordapp.com/api/v6/entitlements/gift-codes/{self.code}?with_application=false&with_subscription_plan=true',
                    timeout=1,
                    verify=False
                )
                if req.status_code == 200:
                    Console().printer("Valid", self.code)
                    with open('results/hit.txt', 'a+') as f:
                        f.write(self.code + "\n")
                    # Webhook integration can be added here if needed
                elif req.status_code == 404:
                    Console().printer("Invalid", self.code)
                elif req.status_code == 429:
                    Console().printer("Rate Limited", self.code)
                    time.sleep(1)  # Adjust delay as needed
                else:
                    Console().printer("Retry", self.code)
            except requests.exceptions.RequestException as e:
                Console().printer("Error", self.code)
                with console_lock:
                    output_text.insert(END, f"Exception during request: {str(e)}\n")
                    output_text.see(END)

# Create main window
root = Tk()
root.title("Discord Nitro Generator")

# Create and place widgets
Label(root, text="Generated Codes:").pack(pady=5)
output_text = scrolledtext.ScrolledText(root, width=50, height=10)
output_text.pack(padx=10, pady=10)

status_label = Label(root, text="Generating codes...", fg="blue")
status_label.pack(pady=5)

# Banner ASCII Art
banner = """
██████╗░██████╗░░█████╗░░██████╗░█████╗░██████╗░░░░░░░██╗███╗░░██╗██████╗░
██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗░░░░░░██║████╗░██║██╔══██╗
██║░░██║██║░░██║██║░░██║╚█████╗░██║░░██║██████╔╝█████╗██║██╔██╗██║██║░░██║
██║░░██║██║░░██║██║░░██║░╚═══██╗██║░░██║██╔═══╝░╚════╝██║██║╚████║██║░░██║
██████╔╝██████╔╝╚█████╔╝██████╔╝╚█████╔╝██║░░░░░░░░░░░██║██║░╚███║██████╔╝
╚═════╝░╚═════╝░░╚════╝░╚═════╝░░╚════╝░╚═╝░░░░░░░░░░░╚═╝╚═╝░░╚══╝╚═════╝░
"""
Label(root, text=banner, font=("Courier", 10), fg="purple").pack()

# Initialize the console and worker
console = Console()
DNG = Worker()

# Start generating codes automatically
threading.Thread(target=DNG.run).start()

# Start the Tkinter event loop
root.mainloop()
