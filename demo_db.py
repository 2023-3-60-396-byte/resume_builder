"""Demonstrates one RETRIEVAL and one UPDATE (for the lab exam).  Run: python demo_db.py"""
import database as db
db.init_db()
print("== RETRIEVAL: resume #1 joined with user, education, experience, skills ==")
r = db.get_resume(1)
print(r["name"], "|", r["email"], "|", r["title"], "| modified:", r["last_modified"])
print("Education :", [(e["degree"], e["institution"]) for e in r["education"]])
print("Skills    :", r["skills"]["technical"])
print("\n== UPDATE: change resume #1 title and add a skill ==")
r["title"] = "Senior Backend Engineer Resume"; r["skills"]["technical"].append("Docker")
db.update_resume(1, r)
r2 = db.get_resume(1)
print(r2["title"], "| skills:", r2["skills"]["technical"], "| modified:", r2["last_modified"])
