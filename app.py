from flask import Flask, render_template, request
import mysql.connector
import os
from flask import send_from_directory



# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = "gllow_salon_secret_2026"

# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host="metro.proxy.rlwy.net",
        user="root",
        password="AYSlCiFitVZbCLupJVvPbODqkfzQwWkT",
        database="railway",
        port=37012
    )

# ---------------- OFFERS ----------------
offers = [
    {"title": "Hair Spa @ ₹299 💇‍♀️", "desc": "Beat the heat care"},
    {"title": "Cleanup @ ₹249 🌿", "desc": "Fresh summer skin"},
    {"title": "Full Handwax @ ₹199 💅", "desc": "Smooth finish"},
    {"title": "Full Legwax @ ₹499 🦵", "desc": "Summer ready"},
    {"title": "Facial @ ₹499 ✨", "desc": "Glow boost"},
    {"title": "Crystal Mani-Pedi 1+1 @ ₹2999 💎", "desc": "Luxury combo offer"},
    {"title": "Gel Polish @ ₹199 💅", "desc": "Long lasting shine"},
    {"title": "Hair Wash @ ₹149 🚿", "desc": "Quick refresh"},
    {"title": "Head Massage @ ₹199 💆‍♀️", "desc": "Relax & de-stress"}
]

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html", offers=offers)

# ---------------- PAGES ----------------
@app.route("/booking")
def booking():
    return render_template("booking.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register")
def register():
    return render_template("register.html")

# ---------------- BOOKING ----------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        service = request.form.get("service") or "Not selected"
        date = request.form.get("date")
        time = request.form.get("time")

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO bookings (name, phone, service, date, time) VALUES (%s,%s,%s,%s,%s)",
            (name, phone, service, date, time)
        )

        db.commit()
        cursor.close()
        db.close()

        return render_template("confirmation.html", msg="✨ Booking Confirmed 💅")

    except Exception as e:
        print("❌ ERROR:", e)
        return render_template("confirmation.html", msg="⚠️ Something went wrong")

# ---------------- CONTACT ----------------
@app.route("/contact_submit", methods=["POST"])
def contact_submit():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get("message")

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, phone, email, message) VALUES (%s,%s,%s,%s)",
            (name, phone, email, message)
        )

        db.commit()
        cursor.close()
        db.close()

        return render_template("confirmation.html", msg="💖 Message Sent Successfully!")

    except Exception as e:
        print("❌ ERROR:", e)
        return render_template("confirmation.html", msg="⚠️ Failed to send message")

# ---------------- REGISTER ----------------
@app.route("/register_submit", methods=["POST"])
def register_submit():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        course = request.form.get("course")
        batch = request.form.get("batch")

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO registrations (name, phone, email, course, batch) VALUES (%s,%s,%s,%s,%s)",
            (name, phone, email, course, batch)
        )

        db.commit()
        cursor.close()
        db.close()

        return render_template("confirmation.html", msg="🎓 Registration Successful!")

    except Exception as e:
        print("❌ ERROR:", e)
        return render_template("confirmation.html", msg="⚠️ Registration failed")

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)