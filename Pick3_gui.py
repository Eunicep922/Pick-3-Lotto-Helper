# --- Pick 3 Lotto Helper (GUI App) with State and Draw Dropdowns ---
import datetime
import tkinter as tk
from tkinter import messagebox

# --- CONFIGURATION ---
KEY_DIGITS = {0, 5, 2, 7}
DEFAULT_RUNDOWN_PATTERN = [3, 1, 7]
DEFAULT_START_NUMBER = 988
STATES = [
    "IL", "MS", "NC", "TX", "TN", "FL", "GA", "NM", "NY",
    "SC", "PA", "OH", "MI", "LA", "CA", "NJ", "VA", "IN", "WI",
    "AL", "KY", "MO", "AZ", "CO", "WA", "MN", "MA", "OK", "NV"
]
DRAWS = ["Morning", "Midday", "Evening", "Night"]

# --- FUNCTIONS ---
def apply_rundown(start_num, pattern):
    results = []
    current = [int(d) for d in str(start_num).zfill(3)]
    for _ in range(10):
        results.append("".join(str(d) for d in current))
        current = [(d + p) % 10 for d, p in zip(current, pattern)]
    return results

def digit_sum(number):
    return sum(int(d) for d in str(number))

def calculate_score(number, date_sum):
    hit_sum = digit_sum(number)
    score = 0
    if hit_sum == date_sum:
        score += 3
    score += sum(1 for d in str(number) if int(d) in KEY_DIGITS)
    return score

def get_date_sum(date):
    return sum(int(c) for c in date.strftime('%m%d%Y'))

def generate_numbers():
    try:
        start_number = int(start_entry.get())
        pattern = [int(p.strip()) for p in pattern_entry.get().split(',')]
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")
        return

    state = state_var.get()
    draw = draw_var.get()
    today = datetime.date.today()
    date_sum = get_date_sum(today)
    rundown_numbers = apply_rundown(start_number, pattern)

    scored_numbers = []
    for num in rundown_numbers:
        score = calculate_score(num, date_sum)
        scored_numbers.append((num, score))

    scored_numbers.sort(key=lambda x: -x[1])
    top_10 = scored_numbers[:10]

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"📍 State: {state} | 🎲 Draw: {draw}\n")
    output_text.insert(tk.END, f"📅 Date: {today.strftime('%Y-%m-%d')}\n")
    output_text.insert(tk.END, f"🔢 Date Sum: {date_sum}\n\n")
    output_text.insert(tk.END, "🔍 Top 10 Strong Numbers:\n")
    for num, score in top_10:
        output_text.insert(tk.END, f"  {num} (Score: {score})\n")

    output_text.insert(tk.END, "\n📋 All Rundown Numbers:\n")
    output_text.insert(tk.END, ", ".join(rundown_numbers))

def reset_fields():
    start_entry.delete(0, tk.END)
    pattern_entry.delete(0, tk.END)
    output_text.delete("1.0", tk.END)
    start_entry.insert(0, str(DEFAULT_START_NUMBER))
    pattern_entry.insert(0, ", ".join(map(str, DEFAULT_RUNDOWN_PATTERN)))
    state_var.set(STATES[0])
    draw_var.set(DRAWS[0])

# --- GUI SETUP ---
root = tk.Tk()
root.title("Pick 3 Lotto Helper")
root.geometry("550x550")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Start Number:").grid(row=0, column=0, sticky="e")
start_entry = tk.Entry(frame)
start_entry.grid(row=0, column=1)
start_entry.insert(0, str(DEFAULT_START_NUMBER))

tk.Label(frame, text="Rundown Pattern (comma-separated):").grid(row=1, column=0, sticky="e")
pattern_entry = tk.Entry(frame)
pattern_entry.grid(row=1, column=1)
pattern_entry.insert(0, ", ".join(map(str, DEFAULT_RUNDOWN_PATTERN)))

state_var = tk.StringVar(value=STATES[0])
draw_var = tk.StringVar(value=DRAWS[0])

tk.Label(frame, text="Select State:").grid(row=2, column=0, sticky="e")
state_menu = tk.OptionMenu(frame, state_var, *STATES)
state_menu.grid(row=2, column=1, sticky="w")

tk.Label(frame, text="Select Draw:").grid(row=3, column=0, sticky="e")
draw_menu = tk.OptionMenu(frame, draw_var, *DRAWS)
draw_menu.grid(row=3, column=1, sticky="w")

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Generate Numbers", command=generate_numbers).pack(side="left", padx=5)
tk.Button(button_frame, text="Reset", command=reset_fields).pack(side="left", padx=5)

output_text = tk.Text(root, height=20, width=65)
output_text.pack(pady=10)

root.mainloop()
