import io
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort
import database as db
from validators import validate
from pdf_generator import build_pdf

app = Flask(__name__)
app.secret_key = "change-me-in-production"
db.init_db()

def read_form(f):
    g = lambda k: f.get(k, "").strip()
    rows = lambda *keys: [dict(zip(keys, r)) for r in zip(*[[v.strip() for v in f.getlist(k)] for k in keys])]
    edu = [{"institution": r["edu_institution"], "degree": r["edu_degree"], "year": r["edu_year"], "result": r["edu_result"]}
           for r in rows("edu_institution", "edu_degree", "edu_year", "edu_result") if any(r.values())]
    exp = [{"company": r["exp_company"], "job_title": r["exp_title"], "duration": r["exp_duration"], "responsibilities": r["exp_resp"]}
           for r in rows("exp_company", "exp_title", "exp_duration", "exp_resp") if any(r.values())]
    skills = {c: [s.strip() for s in g("skills_" + c).split(",") if s.strip()] for c in db.CATS}
    return {"title": g("title"), "name": g("name"), "email": g("email"), "phone": g("phone"), "address": g("address"),
            "linkedin": g("linkedin"), "objective": g("objective"), "education": edu, "experience": exp, "skills": skills}

BLANK = {"title": "", "name": "", "email": "", "phone": "", "address": "", "linkedin": "", "objective": "",
         "education": [], "experience": [], "skills": {c: [] for c in db.CATS}}

@app.route("/")
def index():
    return render_template("index.html", resumes=db.list_resumes())

@app.route("/resume/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        d = read_form(request.form); errors = validate(d)
        if not errors:
            rid = db.create_resume(d); flash("Resume saved successfully.", "ok")
            return redirect(url_for("preview", rid=rid))
        return render_template("form.html", d=d, errors=errors, mode="new")
    return render_template("form.html", d=BLANK, errors={}, mode="new")

@app.route("/resume/<int:rid>/edit", methods=["GET", "POST"])
def edit(rid):
    cur = db.get_resume(rid) or abort(404)
    if request.method == "POST":
        d = read_form(request.form); errors = validate(d)
        if not errors:
            db.update_resume(rid, d); flash("Resume updated.", "ok")
            return redirect(url_for("preview", rid=rid))
        return render_template("form.html", d=d, errors=errors, mode="edit", rid=rid)
    return render_template("form.html", d=cur, errors={}, mode="edit", rid=rid)

@app.route("/resume/<int:rid>")
def preview(rid):
    return render_template("preview.html", d=db.get_resume(rid) or abort(404), rid=rid)

@app.route("/resume/<int:rid>/pdf")
def pdf(rid):
    d = db.get_resume(rid) or abort(404)
    try: data = build_pdf(d)
    except Exception:
        flash("Could not generate the PDF. Please try again.", "err"); return redirect(url_for("preview", rid=rid))
    return send_file(io.BytesIO(data), mimetype="application/pdf", as_attachment=True,
                     download_name=f"{d['name'].replace(' ', '_')}_Resume.pdf")

@app.route("/resume/<int:rid>/delete", methods=["POST"])
def delete(rid):
    db.delete_resume(rid); flash("Resume deleted.", "ok"); return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
