# Judul : Program Remote AC dengan GUI
# Keterangan : Program ini mensimulasikan remote AC melalui GUI

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import time
import speech_recognition as sr
import re

# Global Variables
power_status = "Off"
swing_status = "Off"
fan_status = "Low"
mode_status = "Normal"
timer_status = "Off"
temperature_status = 23
text = ""

# Functions and Procedures
def power():
    global power_status
    global text
    if text != "":
        if text == "nyalakan ac" and power_status == "Off":
            power_status = "On"
        elif text == "matikan ac" and power_status == "On":
            power_status = "Off"
            reset()
    else:
        if power_status == "Off":
            power_status = "On"
        else:
            power_status = "Off"
            reset()
    update_display()

def power_check():
    return power_status == "On"

def swing():
    global text
    global swing_status
    if power_check():
        if (text != ""):
            if text == "nyalakan swing" and swing_status == "Off":
                swing_status = "On"
            elif text == "matikan swing" and swing_status == "On":
                swing_status = "Off"
        else:
            swing_status = "On" if swing_status == "Off" else "Off"
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def fan():
    global text
    global fan_status
    if power_check():
        if fan_status == "Low":
            fan_status = "Medium"
        elif fan_status == "Medium":
            fan_status = "High"
        else:
            fan_status = "Low"
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def mode():
    global text
    global mode_status
    if power_check():
        modes = ["Normal", "Cool", "Dry", "Fan", "Turbo", "Quiet", "Sleep", "Auto"]
        current_index = modes.index(mode_status)
        mode_status = modes[(current_index + 1) % len(modes)]
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def timer_thread(duration_minutes):
    global power_status, timer_status
    time.sleep(duration_minutes * 60)
    reset()
    update_display()

def reset():
    global power_status, swing_status, fan_status, mode_status, timer_status, temperature_status
    power_status = "Off"
    swing_status = "Off"
    fan_status = "Low"
    mode_status = "Normal"
    timer_status = "Off"
    temperature_status = 23

def timer():
    global text
    global timer_status
    if power_check():
        try:
            if text != "":
                match = re.search(r'\d+', text)  # Cari angka pertama dalam string
                duration = match.group()
                duration_minutes = int(duration)
            else:
                duration_minutes = int(timer_entry.get())
                timer_entry.delete(0, tk.END)

            timer_status = f"{duration_minutes} min"
            threading.Thread(target=timer_thread, args=(duration_minutes,), daemon=True).start()
            update_display()
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid number for the timer.")
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def temperature_up():
    global text
    global temperature_status
    if power_check():
        if temperature_status < 32:
            temperature_status += 1
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def temperature_down():
    global text
    global temperature_status
    if power_check():
        if temperature_status > 16:
            temperature_status -= 1
        update_display()
    else:
        messagebox.showwarning("Warning", "Your power is off, cannot continue command.")

def update_display():
    if power_status == "Off":
        display_label.config(image=power_image, text="")
        control_frame.pack_forget()
    else:
        display_label.config(image="", text=f"Power: {power_status}\n"
                                            f"Temperature: {temperature_status} °C\n"
                                            f"Swing: {swing_status}\n"
                                            f"Fan: {fan_status}\n"
                                            f"Mode: {mode_status}\n"
                                            f"Timer: {timer_status}",
                             font=("Helvetica", 14), justify="center", foreground="#FFFFFF", background="#4A4A4A")
        control_frame.pack(pady=20)

def record_and_display():
    global text
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = recognizer.listen(source, timeout=5)
            
        text = recognizer.recognize_google(audio_data, language="id-ID")
        text = text.lower()
        
        
        if (text == "nyalakan ac" or text == "matikan ac"):
            power()
            text = ""
        elif (text == "naikkan suhu"):
            temperature_up()
            text = ""
        elif (text == "turunkan suhu"):
            temperature_down()
            text = ""
        elif (text == "nyalakan swing" or text == "matikan swing"):
            swing()
            text = ""
        elif (text == "ubah fan speed"):
            fan()
            text = ""
        elif (text == "ubah mode"):
            mode()
            text = ""
        elif (text.find("set timer") >= 0):
            timer()
            text = ""
            
# GUI Setup
root = tk.Tk()
root.title("Remote AC")
root.configure(bg="#1F1F1F")

# Center Window
window_width, window_height = 400, 600
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
offset_x, offset_y = (screen_width - window_width) // 2, (screen_height - window_height) // 2 - 50
root.geometry(f"{window_width}x{window_height}+{offset_x}+{offset_y}")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12), padding=5, relief="flat")
style.configure("TLabel", font=("Helvetica", 12), background="#1F1F1F", foreground="#FFFFFF")

# Power Image
power_image_file = "Power.png"
try:
    power_image = ImageTk.PhotoImage(Image.open(power_image_file).resize((150, 150)))
except FileNotFoundError:
    power_image = None

# Display
display_label = ttk.Label(root, background="#4A4A4A", anchor="center", width=50)
display_label.pack(pady=20)

# Controls
control_frame = ttk.Frame(root, style="TFrame")
control_frame.pack(pady=10)

# Power Button
power_button = ttk.Button(root, text="Power", command=power, style="TButton")
power_button.pack(pady=10)

# Temperature Controls
temp_frame = ttk.Frame(control_frame)
temp_frame.pack(pady=10)
temp_up_button = ttk.Button(temp_frame, text="Temperature (↑)", command=temperature_up)
temp_up_button.pack(side="left", padx=10)
temp_down_button = ttk.Button(temp_frame, text="Temperature (↓)", command=temperature_down)
temp_down_button.pack(side="left", padx=10)

# Swing Button
swing_button = ttk.Button(control_frame, text="Swing", command=swing)
swing_button.pack(pady=10)

# Mode & Fan Controls
mode_fan_frame = ttk.Frame(control_frame)
mode_fan_frame.pack(pady=10)
fan_button = ttk.Button(mode_fan_frame, text="Fan Speed", command=fan)
fan_button.pack(side="left", padx=10)
mode_button = ttk.Button(mode_fan_frame, text="Change Mode", command=mode)
mode_button.pack(side="left", padx=10)

# Timer Controls
timer_label = ttk.Label(control_frame, text="Set Timer (minutes):")
timer_label.pack(pady=5)
timer_entry = ttk.Entry(control_frame, width=10)
timer_entry.pack(pady=5)
timer_button = ttk.Button(control_frame, text="Set Timer", command=timer)
timer_button.pack(pady=10)

mic_image = Image.open("microphone.png")
mic_image = mic_image.resize((30, 30), Image.LANCZOS)
mic_photo = ImageTk.PhotoImage(mic_image)

# Tombol untuk merekam suara (berbentuk lingkaran dengan gambar mikrofon)
record_button = tk.Button(root, image=mic_photo, command=record_and_display, font=("Arial", 14), bd=0)
record_button.pack(pady=10)
record_button.config(width=30, height=30, highlightthickness=0)

update_display()
root.mainloop()
