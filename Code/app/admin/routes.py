from flask import Blueprint, render_template, request, redirect, session, url_for

import sqlite3
import uuid
from flask import flash
import os

from utils.smtp_simulator import simulate_send_email

DB_PATH = os.path.join("data", "simulation.db")

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

# Dummy admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")


@admin_bp.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, inbox_link, email_sent, clicked, submitted FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        inbox_id = row[1]  # Just the UUID snippet like 'a1b2c3d4'
        users.append((row[0], inbox_id, row[2], row[3], row[4]))

    return render_template("dashboard.html", users=users)



@admin_bp.route("/create_campaign", methods=["GET", "POST"])
def create_campaign():
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        username = request.form.get("username")
        template_name = request.form.get("template", "login_security_notice.html")  # 🟢 Get selected template
        print("Email template selected: ", template_name)
        inbox_link = str(uuid.uuid4())[:8]  # 🟢 Generate unique inbox ID

        phishing_link = f"/user/phishing_page/{inbox_link}"  # 🟢 Create phishing link
        simulate_send_email(username, phishing_link, template_name)  # 🟢 Simulate email sending

        # 🟢 Store campaign data in database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, inbox_link, email_sent, template) VALUES (?, ?, ?, ?)",
                       (username, inbox_link, 1, template_name))
        conn.commit()
        conn.close()

        flash(f"Simulated email sent to {username}. Inbox: /user/inbox/{inbox_link}", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("campaign_create.html")

@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

@admin_bp.route("/delete_user/<inbox_link>", methods=["POST"])
def delete_user(inbox_link):
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE inbox_link = ?", (inbox_link,))
    conn.commit()
    conn.close()

    flash("User deleted successfully.", "info")
    return redirect(url_for("admin.dashboard"))


