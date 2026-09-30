import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os

DATA_FILE = "assignment_data.json"

data = []

def load_data():
    global data

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
        except:
            data = []
    else:
        data = []

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def clear_fields():
    enrollment_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    assignment_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)
    remarks_entry.delete(0, tk.END)
    status_var.set("Pending")

def validate_student():
    enrollment = enrollment_entry.get().strip()
    name = name_entry.get().strip()

    if not enrollment or not name:
        messagebox.showerror("Validation Error", "Enrollment and name are required.")
        return False

    if not enrollment.isdigit():
        messagebox.showerror("Validation Error", "Enrollment must contain only digits.")
        return False

    return True

def add_submission():
    if not validate_student():
        return

    assignment = assignment_entry.get().strip()
    marks_text = marks_entry.get().strip()
    remarks = remarks_entry.get().strip()
    status = status_var.get()

    if not assignment:
        messagebox.showerror("Validation Error", "Assignment name is required.")
        return

    if marks_text:
        try:
            marks = float(marks_text)
            if marks < 0 or marks > 100:
                raise ValueError
        except:
            messagebox.showerror(
                "Validation Error",
                "Marks must be a number between 0 and 100."
            )
            return
    else:
        marks = ""

    record = {
        "enrollment": enrollment_entry.get().strip(),
        "name": name_entry.get().strip(),
        "assignment": assignment,
        "status": status,
        "marks": marks,
        "remarks": remarks
    }

    data.append(record)
    save_data()
    refresh_table()
    clear_fields()

    messagebox.showinfo("Success", "Submission added successfully.")

def update_marks():
    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Select a record first.")
        return

    marks_text = marks_entry.get().strip()

    if not marks_text:
        messagebox.showerror("Validation Error", "Enter marks.")
        return

    try:
        marks = float(marks_text)
        if marks < 0 or marks > 100:
            raise ValueError
    except:
        messagebox.showerror(
            "Validation Error",
            "Marks must be a number between 0 and 100."
        )
        return

    item = table.item(selected[0])
    index = item["values"][6]

    data[int(index)]["marks"] = marks
    data[int(index)]["status"] = "Completed"
    data[int(index)]["remarks"] = remarks_entry.get().strip()

    save_data()
    refresh_table()

    messagebox.showinfo("Success", "Marks updated successfully.")

def filter_records(*args):
    refresh_table()

def refresh_table():
    for item in table.get_children():
        table.delete(item)

    selected_status = filter_var.get()

    for index, record in enumerate(data):
        if selected_status != "All" and record["status"] != selected_status:
            continue

        table.insert(
            "",
            tk.END,
            values=(
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"],
                record["remarks"],
                index
            )
        )

def select_record(event):
    selected = table.selection()

    if not selected:
        return

    item = table.item(selected[0])
    values = item["values"]

    clear_fields()

    enrollment_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    assignment_entry.insert(0, values[2])
    status_var.set(values[3])

    if values[4] != "":
        marks_entry.insert(0, values[4])

    remarks_entry.insert(0, values[5])

def export_csv():
    if not data:
        messagebox.showerror("Error", "No records available for export.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Enrollment",
                "Name",
                "Assignment",
                "Status",
                "Marks",
                "Remarks"
            ])

            for record in data:
                writer.writerow([
                    record["enrollment"],
                    record["name"],
                    record["assignment"],
                    record["status"],
                    record["marks"],
                    record["remarks"]
                ])

        messagebox.showinfo("Success", "CSV report exported successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

load_data()

root = tk.Tk()
root.title("Assignment Tracker")
root.geometry("1100x650")
root.minsize(900, 550)

title = tk.Label(
    root,
    text="Student Assignment Tracker",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

form = tk.Frame(root)
form.pack(pady=5)

tk.Label(form, text="Enrollment").grid(row=0, column=0, padx=5, pady=5)
enrollment_entry = tk.Entry(form, width=20)
enrollment_entry.grid(row=0, column=1, padx=5)

tk.Label(form, text="Name").grid(row=0, column=2, padx=5)
name_entry = tk.Entry(form, width=20)
name_entry.grid(row=0, column=3, padx=5)

tk.Label(form, text="Assignment").grid(row=1, column=0, padx=5, pady=5)
assignment_entry = tk.Entry(form, width=20)
assignment_entry.grid(row=1, column=1, padx=5)

tk.Label(form, text="Marks").grid(row=1, column=2, padx=5)
marks_entry = tk.Entry(form, width=20)
marks_entry.grid(row=1, column=3, padx=5)

tk.Label(form, text="Remarks").grid(row=2, column=0, padx=5, pady=5)
remarks_entry = tk.Entry(form, width=20)
remarks_entry.grid(row=2, column=1, padx=5)

tk.Label(form, text="Status").grid(row=2, column=2, padx=5)

status_var = tk.StringVar(value="Pending")

status_frame = tk.Frame(form)
status_frame.grid(row=2, column=3)

tk.Radiobutton(
    status_frame,
    text="Pending",
    variable=status_var,
    value="Pending"
).pack(side=tk.LEFT)

tk.Radiobutton(
    status_frame,
    text="Completed",
    variable=status_var,
    value="Completed"
).pack(side=tk.LEFT)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Submission",
    command=add_submission,
    width=15
).pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="Update Marks",
    command=update_marks,
    width=15
).pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=15
).pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="Export CSV",
    command=export_csv,
    width=15
).pack(side=tk.LEFT, padx=5)

filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)

filter_var = tk.StringVar(value="All")

filter_combo = ttk.Combobox(
    filter_frame,
    textvariable=filter_var,
    values=["All", "Pending", "Completed"],
    state="readonly",
    width=15
)
filter_combo.pack(side=tk.LEFT)
filter_combo.bind("<<ComboboxSelected>>", filter_records)

table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

columns = (
    "Enrollment",
    "Name",
    "Assignment",
    "Status",
    "Marks",
    "Remarks",
    "Index"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:
    table.heading(column, text=column)

table.column("Enrollment", width=100)
table.column("Name", width=140)
table.column("Assignment", width=160)
table.column("Status", width=100)
table.column("Marks", width=80)
table.column("Remarks", width=180)
table.column("Index", width=60)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=table.yview
)

table.configure(yscrollcommand=scrollbar.set)

table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

table.bind("<<TreeviewSelect>>", select_record)

refresh_table()

root.mainloop()