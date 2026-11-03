"""Manuel Gomez portfolio - Flask app.
# hhh
Run:  pip install -r requirements.txt
      python app.py          ->  http://127.0.0.1:5000
"""
import os
import threading
import webbrowser
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage

from flask import Flask, abort, jsonify, render_template, request, send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_DIR = os.path.join(BASE_DIR, "static")
RESUME_FILE = "resume.pdf"          
MESSAGES_LOG = os.path.join(BASE_DIR, "messages.txt")

PROFILE = {
    "name": "Manuel Gomez",
    "email": "gomexzmanuell@gmail.com",
    "phone": "09912440525",
    "location": "Tanza, Cavite",
    
    "socials": {"GitHub": "", "LinkedIn": ""},
    "year": datetime.now().year,
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@app.route("/")
def index():
    return render_template("index.html", p=PROFILE)


@app.route("/resume/view")
def resume_view():
    if not os.path.exists(os.path.join(RESUME_DIR, RESUME_FILE)):
        abort(404, "Wala pa ang resume. Ilagay ang PDF sa static/resume.pdf")
    return send_from_directory(RESUME_DIR, RESUME_FILE)


@app.route("/resume/download")
def resume_download():
    if not os.path.exists(os.path.join(RESUME_DIR, RESUME_FILE)):
        abort(404, "Wala pa ang resume. Ilagay ang PDF sa static/resume.pdf")
    return send_from_directory(
        RESUME_DIR, RESUME_FILE, as_attachment=True,
        download_name="Manuel_Gomez_Resume.pdf",
    )


def send_email(name, email, subject, message):
    """Send via SMTP kung naka-set ang env vars; kung wala, return False."""
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    if not (host and user and password):
        return False
    msg = EmailMessage()
    msg["Subject"] = f"[Portfolio] {subject}"
    msg["From"] = user
    msg["To"] = PROFILE["email"]
    msg["Reply-To"] = email
    msg.set_content(f"From: {name} <{email}>\n\n{message}")
    with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "587")), timeout=15) as s:
        s.starttls()
        s.login(user, password)
        s.send_message(msg)
    return True


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}
    name, email = data.get("name", "").strip(), data.get("email", "").strip()
    subject, message = data.get("subject", "").strip(), data.get("message", "").strip()

    if not (name and email and subject and message):
        return jsonify(ok=False, error="Please fill in every field."), 400
    if not EMAIL_RE.match(email):
        return jsonify(ok=False, error="Enter a valid email address."), 400
    if len(name) > 100 or len(subject) > 150 or len(message) > 3000:
        return jsonify(ok=False, error="Your message is too long."), 400

    try:
        sent = send_email(name, email, subject, message)
    except Exception:
        app.logger.exception("SMTP failed")
        sent = False

    if not sent:  
        with open(MESSAGES_LOG, "a", encoding="utf-8") as f:
            f.write(f"--- {datetime.now():%Y-%m-%d %H:%M} ---\n"
                    f"{name} <{email}>\n{subject}\n{message}\n\n")
    return jsonify(ok=True, message="Message sent. Thank you!")


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":  
        threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)
