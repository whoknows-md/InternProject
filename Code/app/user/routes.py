from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
import os

user_bp = Blueprint('user', __name__, template_folder='../templates/user')

# ✅ Use consistent DB path
DB_PATH = os.path.join("data", "simulation.db")

# ✅ Show inbox with username & email link
@user_bp.route("/inbox/<inbox_link>")
def user_inbox(inbox_link):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE inbox_link=?", (inbox_link,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return render_template("inbox.html", username=row[0], link=inbox_link)
    return "Invalid inbox link", 404

# ✅ Phishing landing page (GET → track click, POST → track submit)
@user_bp.route("/phishing/<inbox_link>", methods=["GET", "POST"])
def phishing_page(inbox_link):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT template FROM users WHERE inbox_link=?", (inbox_link,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return "Invalid link", 404

    template_name = row[0] or "login_security_notice.html"
    
    if request.method == "POST":
        cursor.execute("UPDATE users SET submitted=1 WHERE inbox_link=?", (inbox_link,))
        conn.commit()
        conn.close()
        return redirect(url_for("user.educate"))

    cursor.execute("UPDATE users SET clicked=1 WHERE inbox_link=?", (inbox_link,))
    conn.commit()
    conn.close()

    return render_template(f"email/{template_name}", phishing_link=inbox_link)

@user_bp.route("/phishing_page/<inbox_link>", methods=["GET", "POST"])
def phishing_real_form(inbox_link):
    if request.method == "POST":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET submitted=1 WHERE inbox_link=?", (inbox_link,))
        conn.commit()
        conn.close()
        return redirect(url_for("user.educate"))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET clicked=1 WHERE inbox_link=?", (inbox_link,))
    conn.commit()
    conn.close()

    return render_template("user/phishing_page.html", link=inbox_link)


# ✅ Education page
@user_bp.route("/educate")
def educate():
    return render_template("educate.html")

@user_bp.route("/access", methods=["POST"])
def access_user_inbox():
    inbox_link = request.form.get("inbox_link")
    if inbox_link:
        return redirect(url_for("user.user_inbox", inbox_link=inbox_link))
    flash("Please enter a valid link.")
    return redirect("/")

from flask import request

@user_bp.route("/enter", methods=["GET", "POST"])
def enter_inbox():
    if request.method == "POST":
        link = request.form.get("inbox_link", "").strip()
        return redirect(url_for("user.user_inbox", inbox_link=link))
    return render_template("user_enter.html")




