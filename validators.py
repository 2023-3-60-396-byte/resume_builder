import re
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE = re.compile(r"^\+?[0-9\s\-]{7,16}$")

def validate(d):
    """Server-side validation (activity diagram). Returns {field: message}."""
    e = {}
    if not d["title"].strip(): e["title"] = "Resume title is required."
    if not d["name"].strip(): e["name"] = "Full name is required."
    if not EMAIL.match(d["email"].strip()): e["email"] = "Enter a valid email address."
    if not PHONE.match(d["phone"].strip()): e["phone"] = "Enter a valid phone number (7-16 digits)."
    if not d["objective"].strip(): e["objective"] = "Career objective is required."
    if not d["education"]: e["education"] = "Add at least one education entry."
    for i, r in enumerate(d["education"]):
        if not (r["institution"] and r["degree"]): e[f"edu{i}"] = "Institution and degree are required."
        elif not (r["year"].isdigit() and 1950 <= int(r["year"]) <= 2100): e[f"edu{i}"] = "Enter a valid passing year."
    for i, r in enumerate(d["experience"]):
        if not (r["company"] and r["job_title"] and r["duration"]): e[f"exp{i}"] = "Company, position and duration are required."
    if not any(d["skills"].values()): e["skills"] = "Add at least one skill."
    return e
