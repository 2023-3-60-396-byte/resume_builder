const form = document.getElementById("rf"), pv = document.getElementById("pv");
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/, PHONE = /^\+?[0-9\s\-]{7,16}$/;
const CATS = ["technical","soft","language","certification","other"];
const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const val = n => (form.elements[n]?.value || "").trim();
const all = n => [...form.querySelectorAll(`[name="${n}"]`)].map(e => e.value.trim());

function render() {   // dynamic live resume preview
  const edu = all("edu_institution").map((_, i) => `<p><b>${esc(all("edu_degree")[i])}</b> — ${esc(all("edu_institution")[i])} (${esc(all("edu_year")[i])})<br><span class="muted">${esc(all("edu_result")[i])}</span></p>`).join("");
  const exp = all("exp_company").map((_, i) => `<p><b>${esc(all("exp_title")[i])}</b>, ${esc(all("exp_company")[i])} <span class="muted">(${esc(all("exp_duration")[i])})</span><br>${esc(all("exp_resp")[i])}</p>`).join("");
  const sk = CATS.filter(c => val("skills_"+c)).map(c => `<p><b>${c[0].toUpperCase()+c.slice(1)}:</b> ${esc(val("skills_"+c))}</p>`).join("");
  pv.innerHTML = `<h2>${esc(val("name")) || "Your Name"}</h2><p class="muted">${[val("email"),val("phone"),val("address"),val("linkedin")].filter(Boolean).map(esc).join(" | ")}</p>
  <h4>Career Objective</h4><p>${esc(val("objective"))}</p><h4>Education</h4>${edu}${exp ? "<h4>Experience</h4>"+exp : ""}<h4>Skills</h4>${sk}`;
}
function addRow(t) { document.getElementById(t).appendChild(document.getElementById("t-"+t).content.cloneNode(true)); render(); }
document.querySelectorAll("[data-add]").forEach(b => b.onclick = () => addRow(b.dataset.add));
form.addEventListener("click", e => { if (e.target.classList.contains("rm")) { e.target.closest(".item").remove(); render(); } });
form.addEventListener("input", render);
if (!document.querySelector("#edu .item")) addRow("edu");

function setErr(el, msg) {   // "Show inline errors" (activity diagram)
  el.classList.toggle("bad", !!msg);
  const old = el.nextElementSibling; if (old && old.classList.contains("js")) old.remove();
  if (msg) { const s = document.createElement("small"); s.className = "err js"; s.textContent = msg; el.after(s); }
  return !msg;
}
form.addEventListener("submit", e => {
  let ok = true; const chk = (n, test, msg) => ok = setErr(form.elements[n], test(val(n)) ? "" : msg) && ok;
  chk("title", v => v, "Resume title is required."); chk("name", v => v, "Full name is required.");
  chk("email", v => EMAIL.test(v), "Enter a valid email address."); chk("phone", v => PHONE.test(v), "Enter a valid phone number.");
  chk("objective", v => v, "Career objective is required.");
  const items = form.querySelectorAll("#edu .item");
  items.forEach(it => {
    const [i, d, y] = it.querySelectorAll("input"), yr = +y.value;
    ok = setErr(y, i.value.trim() && d.value.trim() && yr >= 1950 && yr <= 2100 ? "" : "Institution, degree and a valid year are required.") && ok;
  });
  if (!items.length) { alert("Add at least one education entry."); ok = false; }
  if (!CATS.some(c => val("skills_"+c))) { alert("Add at least one skill."); ok = false; }
  if (!ok) { e.preventDefault(); form.querySelector(".bad")?.scrollIntoView({behavior:"smooth", block:"center"}); }
});
render();
