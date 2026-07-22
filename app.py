from flask import Flask, render_template, request, redirect, session, flash, send_file
from database.database import (
    create_database,
    register_user,
    login_user,
    save_history,
    get_history
)
from recommendation import recommend
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
app = Flask(__name__)
app.secret_key = "EcoTrackAI123"

create_database()

# ---------------- HOME ----------------

@app.route("/")
def home():

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:

            register_user(name,email,password)

            flash("Registration Successful!")

            return redirect("/")

        except Exception:

            flash("Email Already Exists!")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]

    password = request.form["password"]

    user = login_user(email,password)

    if user:

        session["user"] = user[1]

        return redirect("/dashboard")

    flash("Invalid Email or Password")

    return redirect("/")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    history = get_history()

    total_records = len(history)
    total_carbon = sum(i[7] for i in history) if history else 0
    average = round(total_carbon / total_records, 2) if total_records else 0

    transport_total = sum(i[1] for i in history) if history else 0
    electricity_total = sum(i[2] for i in history) if history else 0
    water_total = sum(i[3] for i in history) if history else 0
    plastic_total = sum(i[4] for i in history) if history else 0
    waste_total = sum(i[5] for i in history) if history else 0
    fuel_total = sum(i[6] for i in history) if history else 0

    return render_template(
        "dashboard.html",
        username=session["user"],
        total_records=total_records,
        total_carbon=total_carbon,
        average=average,
        eco_score=max(0, 100 - int(total_carbon)),
        trees_saved=round(total_carbon / 20, 1),
        transport_total=transport_total,
        electricity_total=electricity_total,
        water_total=water_total,
        plastic_total=plastic_total,
        waste_total=waste_total,
        fuel_total=fuel_total
    )

# ---------------- CALCULATOR ----------------

@app.route("/calculator",methods=["GET","POST"])
def calculator():

    if "user" not in session:

        return redirect("/")

    carbon=None

    category=""

    suggestion=""

    if request.method=="POST":

        transport=float(request.form["transport"])

        electricity=float(request.form["electricity"])

        water=float(request.form["water"])

        plastic=float(request.form["plastic"])

        waste=float(request.form["waste"])

        fuel=float(request.form["fuel"])

        carbon=round(

            transport*0.21+

            electricity*0.50+

            water*0.001+

            plastic*6+

            waste*1.5+

            fuel*2.3

        ,2)

        category,suggestion=recommend(carbon)

        save_history(

            transport,

            electricity,

            water,

            plastic,

            waste,

            fuel,

            carbon,

            category

        )

    return render_template(

        "calculator.html",

        carbon=carbon,

        category=category,

        suggestion=suggestion

    )


# ---------------- HISTORY ----------------

@app.route("/history")
def history():

    if "user" not in session:
        return redirect("/")

    return render_template(
        "history.html",
        history=get_history()
    )

# ---------------- REPORTS ----------------

@app.route("/reports")
def reports():

    if "user" not in session:

        return redirect("/")

    return render_template(

        "reports.html",

        history=get_history()

    )

@app.route("/download_pdf")
def download_pdf():

    if "user" not in session:
        return redirect("/")

    history = get_history()

    pdf = SimpleDocTemplate("Carbon_Report.pdf")

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>AI Carbon Footprint Report</b>",
            styles["Heading1"]
        )
    )

    data = [[

        "ID",

        "Transport",

        "Electricity",

        "Water",

        "Plastic",

        "Waste",

        "Fuel",

        "Carbon",

        "Category"

    ]]

    for row in history:

        data.append(list(row))

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.green),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),1,colors.black),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,0),10)

    ]))

    elements.append(table)

    pdf.build(elements)

    return send_file(

        "Carbon_Report.pdf",

        as_attachment=True

    )

# ---------------- PROFILE ----------------

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/")

    history = get_history()

    total_records = len(history)

    total_carbon = sum(i[7] for i in history) if history else 0

    eco_score = max(0, 100 - int(total_carbon))

    return render_template(
        "profile.html",
        username=session["user"],
        total_records=total_records,
        total_carbon=total_carbon,
        eco_score=eco_score
    )

# ---------------- ECO TIPS ----------------

@app.route("/eco-tips")
def eco_tips():

    if "user" not in session:
        return redirect("/")

    return render_template("eco_tips.html")


# ---------------- GOALS ----------------

@app.route("/goals")
def goals():

    if "user" not in session:
        return redirect("/")

    return render_template("goals.html")


# ---------------- LEADERBOARD ----------------

@app.route("/leaderboard")
def leaderboard():

    if "user" not in session:
        return redirect("/")

    history = get_history()

    total_carbon = sum(i[7] for i in history) if history else 0

    eco_score = max(0, 100 - int(total_carbon))

    return render_template(
        "leaderboard.html",
        username=session["user"],
        eco_score=eco_score
    )

@app.route("/about")
def about():

    if "user" not in session:
        return redirect("/")

    return render_template("about.html")

if __name__ == "__main__":

    app.run(debug=True)