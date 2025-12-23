from flask import Flask, render_template, request, redirect, session, abort
import joblib
import re
from sqlalchemy import func

from database import session as db_session, User, Complaint
from auth import login_required

app = Flask(__name__)
app.secret_key = "smart-complaint-secret"

# ================= LOAD ML MODEL =================
model = joblib.load("model/complaint_model.pkl")

# ================= PRIORITY LOGIC =================
def assign_priority(text):
    text = text.lower()
    if "no" in text or "overflow" in text or "danger" in text:
        return "High"
    elif "delay" in text or "problem" in text:
        return "Medium"
    else:
        return "Low"

# ================= SPAM FILTER =================
# ================= SPAM FILTER =================
SPAM_WORDS = {
    "hi", "hello", "hey", "test", "ok", "hii", "nothing",
    "abcd", "asdf", "1234"
}

def is_spam(text):
    text = text.lower().strip()
    words = text.split()

    # Block obvious spam words
    if any(w in SPAM_WORDS for w in words):
        return True

    # Block extremely short meaningless input
    if len(text) < 10:
        return True

    return False


# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db_session.query(User).filter_by(
            username=username,
            password=password
        ).first()

        if user:
            session["user_id"] = user.id
            session["role"] = user.role

            if user.role == "admin":
                return redirect("/operator_dashboard")
            else:
                return redirect("/client_dashboard")

    return render_template("login.html")

# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Username and password required", 400

        if db_session.query(User).filter_by(username=username).first():
            return "User already exists", 400

        user = User(username=username, password=password, role="citizen")
        db_session.add(user)
        db_session.commit()
        return redirect("/")

    return render_template("signup.html")

# ================= CLIENT DASHBOARD =================
@app.route("/client_dashboard", methods=["GET", "POST"])
@login_required(role="citizen")
def client_dashboard():
    if request.method == "POST":
        text = request.form.get("complaint")
        location = request.form.get("location")

        # --- VALIDATION ---
        if not text or not location:
            return "Complaint text and location are required", 400

        if is_spam(text):
            return "Spam or meaningless complaints are not allowed", 400

        clean = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        category = model.predict([clean])[0]
        priority = assign_priority(text)

        complaint = Complaint(
            text=text,
            category=category,
            priority=priority,
            status="Pending",
            location=location,
            user_id=session["user_id"]
        )

        db_session.add(complaint)
        db_session.commit()

    complaints = db_session.query(Complaint).filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "client_dashboard.html",
        complaints=complaints
    )

# ================= CLIENT DELETE (OWN ONLY) =================
@app.route("/delete_complaint/<int:id>")
@login_required(role="citizen")
def delete_complaint(id):
    complaint = db_session.query(Complaint).filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if not complaint:
        abort(403)

    db_session.delete(complaint)
    db_session.commit()
    return redirect("/client_dashboard")

# ================= OPERATOR DASHBOARD =================
@app.route("/operator_dashboard")
@login_required(role="admin")
def operator_dashboard():
    complaints = db_session.query(Complaint).all()

    total = len(complaints)
    pending = db_session.query(Complaint).filter_by(status="Pending").count()
    in_progress = db_session.query(Complaint).filter_by(status="In Progress").count()
    resolved = db_session.query(Complaint).filter_by(status="Resolved").count()

    cat_data = db_session.query(
        Complaint.category, func.count()
    ).group_by(Complaint.category).all()

    pri_data = db_session.query(
        Complaint.priority, func.count()
    ).group_by(Complaint.priority).all()

    stat_data = db_session.query(
        Complaint.status, func.count()
    ).group_by(Complaint.status).all()

    return render_template(
        "operator_dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        cat_labels=[c[0] for c in cat_data],
        cat_values=[c[1] for c in cat_data],
        priority_labels=[p[0] for p in pri_data],
        priority_values=[p[1] for p in pri_data],
        status_labels=[s[0] for s in stat_data],
        status_values=[s[1] for s in stat_data]
    )

# ================= UPDATE STATUS =================
@app.route("/update_status/<int:id>", methods=["POST"])
@login_required(role="admin")
def update_status(id):
    complaint = db_session.query(Complaint).get(id)
    if complaint:
        complaint.status = request.form.get("status", complaint.status)
        db_session.commit()
    return redirect("/operator_dashboard")

# ================= OPERATOR DELETE (ONLY IF RESOLVED) =================
@app.route("/operator_delete/<int:id>")
@login_required(role="admin")
def operator_delete(id):
    complaint = db_session.query(Complaint).get(id)

    if complaint and complaint.status == "Resolved":
        db_session.delete(complaint)
        db_session.commit()

    return redirect("/operator_dashboard")

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
