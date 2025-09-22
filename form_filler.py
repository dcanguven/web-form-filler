import csv
import datetime
import time
import re

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 11 and phone.startswith("05")

def run_form_filler():
    with open("data.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)

    with open("audit_log.txt", "a", encoding="utf-8") as log:
        for idx, row in enumerate(rows, start=1):
            name, email, phone = row
            time.sleep(0.1)
            status = "VALID" if validate_email(email) and validate_phone(phone) else "INVALID"
            status = status.ljust(7)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"{status}| Row {idx} | {timestamp} | {name}, {email}, {phone}\n")