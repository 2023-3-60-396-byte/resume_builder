import sqlite3, os
from datetime import datetime
BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "resume.db")
CATS = ["technical", "soft", "language", "certification", "other"]

def conn():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON"); return c

def init_db(seed=True):
    c = conn(); c.executescript(open(os.path.join(BASE, "schema.sql")).read())
    if seed and c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        c.executescript(open(os.path.join(BASE, "seed.sql")).read())
    c.commit(); c.close()

def list_resumes():
    with conn() as c:
        return c.execute("""SELECT r.resume_id, r.title, r.last_modified, u.name, u.email
            FROM resumes r JOIN users u USING(user_id) ORDER BY r.last_modified DESC""").fetchall()

def get_resume(rid):
    """RETRIEVE: returns the whole resume as one dict (or None)."""
    with conn() as c:
        r = c.execute("""SELECT r.*, u.name, u.email, u.phone_number AS phone FROM resumes r
            JOIN users u USING(user_id) WHERE resume_id=?""", (rid,)).fetchone()
        if not r: return None
        d = dict(r); d["objective"] = d.pop("career_objective") or ""
        d["education"] = [dict(x, year=str(x["graduation_year"])) for x in
            c.execute("SELECT * FROM education WHERE resume_id=? ORDER BY graduation_year DESC", (rid,))]
        d["experience"] = [dict(x) for x in c.execute("SELECT * FROM experience WHERE resume_id=? ORDER BY exp_id", (rid,))]
        d["skills"] = {k: [] for k in CATS}
        for s in c.execute("SELECT * FROM skills WHERE resume_id=? ORDER BY skill_id", (rid,)):
            d["skills"][s["category"]].append(s["skill_name"])
        return d

def _children(c, rid, d):
    for r in d["education"]:
        c.execute("INSERT INTO education(resume_id,institution,degree,graduation_year,result) VALUES(?,?,?,?,?)",
                  (rid, r["institution"], r["degree"], int(r["year"]), r["result"]))
    for r in d["experience"]:
        c.execute("INSERT INTO experience(resume_id,company,job_title,duration,responsibilities) VALUES(?,?,?,?,?)",
                  (rid, r["company"], r["job_title"], r["duration"], r["responsibilities"]))
    for cat, items in d["skills"].items():
        for s in items:
            c.execute("INSERT INTO skills(resume_id,skill_name,category) VALUES(?,?,?)", (rid, s, cat))

def _user(c, d):
    u = c.execute("SELECT user_id FROM users WHERE email=?", (d["email"],)).fetchone()
    if u:
        c.execute("UPDATE users SET name=?, phone_number=? WHERE user_id=?", (d["name"], d["phone"], u[0])); return u[0]
    return c.execute("INSERT INTO users(name,email,phone_number) VALUES(?,?,?)", (d["name"], d["email"], d["phone"])).lastrowid

def create_resume(d):
    with conn() as c:
        uid = _user(c, d)
        rid = c.execute("INSERT INTO resumes(user_id,title,address,linkedin,career_objective) VALUES(?,?,?,?,?)",
                        (uid, d["title"], d["address"], d["linkedin"], d["objective"])).lastrowid
        _children(c, rid, d); return rid

def update_resume(rid, d):
    """UPDATE: transactionally rewrites parent row and replaces child rows."""
    with conn() as c:
        uid = _user(c, d)
        c.execute("""UPDATE resumes SET user_id=?, title=?, address=?, linkedin=?, career_objective=?,
                     last_modified=? WHERE resume_id=?""",
                  (uid, d["title"], d["address"], d["linkedin"], d["objective"],
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rid))
        for t in ("education", "experience", "skills"):
            c.execute(f"DELETE FROM {t} WHERE resume_id=?", (rid,))
        _children(c, rid, d)

def delete_resume(rid):
    with conn() as c: c.execute("DELETE FROM resumes WHERE resume_id=?", (rid,))
