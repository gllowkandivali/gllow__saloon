from flask import Flask, render_template, request
import mysql.connector
import os

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

# ---------------- HOME ----------------
offers = [
    {"title": "50% OFF Facial ✨", "desc": "Limited time offer"},
    {"title": "Hair Spa @ ₹299 💇‍♀️", "desc": "Weekend Special"},
    {"title": "Free Eyebrow with Facial 💅", "desc": "Combo Offer"}
]

@app.route("/")
def home():
    return render_template("index.html", offers=offers)

# ---------------- PAGES ----------------
@app.route("/booking")
def booking():
    return render_template("confirmation.html", msg="Booking Received!")

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
    return render_template("contact.html")  # 👈 FIX (form page hona chahiye)

@app.route("/register")
def register():
    return render_template("register.html")  # 👈 FIX

# ---------------- BOOKING ----------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        service = request.form.get("services") or "Not selected"
        date = request.form.get("date")
        time = request.form.get("time")

        try:
            db = get_db()
            cursor = db.cursor()

            cursor.execute(
                "INSERT INTO bookings (name, phone, service, date, time) VALUES (%s,%s,%s,%s,%s)",
                (name, phone, service, date, time)
            )

            db.commit()
            cursor.close()
            db.close()

        except Exception as db_error:
            print("❌ DB ERROR:", db_error)

        return render_template("confirmation.html", msg="Booking Confirmed 💅")

    except Exception as e:
        return f"Error: {str(e)}"

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

        return render_template("confirmation.html", msg="Message Sent Successfully 💖")

    except Exception as e:
        return f"Error: {str(e)}"

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

        return render_template("confirmation.html", msg="Registration Successful 🎓")

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)