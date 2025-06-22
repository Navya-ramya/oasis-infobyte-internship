import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import pyttsx3

# Setup TTS
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# BMI calculation logic
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_weight_range(height):
    return 18.5 * (height ** 2), 24.9 * (height ** 2)

def get_height_range(weight):
    return (weight / 24.9) ** 0.5, (weight / 18.5) ** 0.5

def calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight_unit_var.get() == "lbs":
            weight *= 0.453592
        if height_unit_var.get() == "feet":
            height *= 0.3048

        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)
        w_min, w_max = get_weight_range(height)
        h_min, h_max = get_height_range(weight)

        bmi_label.config(text="BMI: {:.2f}".format(bmi))
        category_label.config(text="Category: {}".format(category))
        weight_range_label.config(text="Suggested Weight Range: {:.2f} - {:.2f} kg".format(w_min, w_max))
        height_range_label.config(text="Suggested Height Range: {:.2f} - {:.2f} m".format(h_min, h_max))

        speak(f"Your BMI is {bmi:.2f}, which is considered {category}")

        # Save to history
        history.append(f"BMI: {bmi:.2f}, Category: {category}")
        history_box.insert(tk.END, f"{bmi:.2f} - {category}")
    except:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

# Toggle theme
def toggle_theme():
    theme = theme_var.get()
    bg, fg = ("#1e1e1e", "white") if theme == "Dark" else ("#f0f0f0", "black")
    root.configure(bg=bg)
    for widget in root.winfo_children():
        widget.configure(bg=bg, fg=fg)

# Clear fields
def clear_fields():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    bmi_label.config(text="BMI:")
    category_label.config(text="Category:")
    weight_range_label.config(text="Suggested Weight Range:")
    height_range_label.config(text="Suggested Height Range:")

# GUI Setup
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("700x500")
root.configure(bg="#f0f0f0")

history = []

# Theme
theme_var = tk.StringVar(value="Light")
tk.Label(root, text="Theme: ", bg="#f0f0f0").place(x=550, y=10)
tk.OptionMenu(root, theme_var, "Light", "Dark", command=lambda x: toggle_theme()).place(x=600, y=5)

tk.Label(root, text="Weight:", font=("Helvetica", 12), bg="#f0f0f0").place(x=50, y=50)
weight_entry = tk.Entry(root, font=("Helvetica", 12))
weight_entry.place(x=150, y=50)

weight_unit_var = tk.StringVar(value="kgs")
ttk.Combobox(root, textvariable=weight_unit_var, values=["kgs", "lbs"], width=5).place(x=320, y=50)

tk.Label(root, text="Height:", font=("Helvetica", 12), bg="#f0f0f0").place(x=50, y=90)
height_entry = tk.Entry(root, font=("Helvetica", 12))
height_entry.place(x=150, y=90)

height_unit_var = tk.StringVar(value="meters")
ttk.Combobox(root, textvariable=height_unit_var, values=["meters", "feet"], width=5).place(x=320, y=90)

# Buttons
tk.Button(root, text="Calculate", font=("Helvetica", 11), bg="#4CAF50", fg="white", command=calculate).place(x=150, y=130)
tk.Button(root, text="Clear", font=("Helvetica", 11), bg="#FF5722", fg="white", command=clear_fields).place(x=250, y=130)

# Output
bmi_label = tk.Label(root, text="BMI:", font=("Helvetica", 12), bg="#f0f0f0")
bmi_label.place(x=50, y=180)

category_label = tk.Label(root, text="Category:", font=("Helvetica", 12), bg="#f0f0f0")
category_label.place(x=50, y=210)

weight_range_label = tk.Label(root, text="Suggested Weight Range:", font=("Helvetica", 12), bg="#f0f0f0")
weight_range_label.place(x=50, y=240)

height_range_label = tk.Label(root, text="Suggested Height Range:", font=("Helvetica", 12), bg="#f0f0f0")
height_range_label.place(x=50, y=270)

# History
tk.Label(root, text="History", font=("Helvetica", 12, "bold"), bg="#f0f0f0").place(x=500, y=100)
history_box = tk.Listbox(root, width=30, height=10)
history_box.place(x=450, y=130)

# BMI Chart
bmi_chart = """\nBMI Classification:\n
< 18.5 : Underweight
18.5 - 24.9 : Normal
25 - 29.9 : Overweight
≥ 30 : Obese
"""
tk.Label(root, text=bmi_chart, font=("Helvetica", 11), justify="left", bg="#f0f0f0").place(x=450, y=300)

root.mainloop()
