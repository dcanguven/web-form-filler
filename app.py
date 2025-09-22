from flask import Flask, render_template, request, redirect
import csv
import datetime
from form_filler import run_form_filler
import re

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 11 and phone.startswith("05")

app = Flask(__name__)

def read_csv():
    with open("data.csv", newline="", encoding="utf-8") as f:
        return list(csv.reader(f))[1:]

def read_log():
    try:
        with open("audit_log.txt", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []

def append_to_csv(name, email, phone):
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, email, phone])

def append_to_log(row_index, status, row_data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = status.upper()
    if status == "MANUAL ENTRY":
        is_valid = "VALID" if validate_email(row_data[1]) and validate_phone(row_data[2]) else "INVALID"
        status_aligned = is_valid.ljust(7)
        log_entry = f"{status_aligned}| Row {row_index} | {timestamp} | {', '.join(row_data)}"
    else:
        status_aligned = status.ljust(7)
        log_entry = f"{status_aligned}| Row {row_index} | {timestamp} | {', '.join(row_data)}"
    
    with open("audit_log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        append_to_csv(name, email, phone)
        append_to_log("Manual", "Manual Entry", [name, email, phone])
        return redirect("/")

    headers = ["Name", "Email", "Phone"]
    rows = read_csv()
    logs = read_log()
    return render_template("dashboard.html", headers=headers, rows=rows, logs=logs)

@app.route("/run-filler", methods=["POST"])
def run_filler():
    run_form_filler()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)