from flask import Flask, flash, session, render_template, request, redirect, url_for
from database import Database, LoginModel, RegisterModel
from bmr import BmrInputs, Bmr
import bcrypt

app = Flask(__name__)
app.secret_key = "javad personal website"
db = Database()
bmrcal = Bmr()
loginuser = ""
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index")
def index1():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect(url_for("index"))

@app.route("/aiapps", methods=['GET', 'POST'])
def aiapps():
    if session.get("user_id"):
        if request.method == 'GET':
            return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser)
        elif request.method == 'POST':
            try:
                bmr = BmrInputs(
                        weight = float(request.form['weight']),
                        height = float(request.form['height']),
                        age = float(request.form['age'])
                )
                if request.form.get('sex') == 'Male':
                    bmr_res = bmrcal.men(bmr.weight, bmr.height, bmr.age)
                elif request.form.get('sex') == 'Female':
                    bmr_res = bmrcal.women(bmr.weight, bmr.height, bmr.age)
                return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser, bmr=bmr_res)
            except:
                flash("login format data not correct", "warning")
                return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser)
    else:
        return redirect(url_for("index"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    global loginuser
    if request.method == 'GET':
        return render_template("login.html", tabactivelogin="tab-pane fade show active", login_b="nav-link active", tabactiveregister="tab-pane fade", register_b="nav-link")
    elif request.method == 'POST':
        checkform = request.form["checkform"]
        if checkform == "login":
            if request.form.get("checkbox"):
                try:
                    login = LoginModel(
                    username = request.form['username'],
                    password = request.form['password']
                    )
                    loginuser = login.username
                    luser = db.read_from_database_by_username(login.username)
                    if luser is None:
                        flash("username is incorrect", "warning")
                        return redirect(url_for("login"))
                    else:
                        entered_password_byte = login.password.encode("utf-8")
                        if bcrypt.checkpw(entered_password_byte, luser.password):
                            flash("Welcome ", "success")
                            session["user_id"] = luser.id
                            return redirect(url_for("aiapps"))
                        else:
                            flash("password is incorrect", "danger")
                            return redirect(url_for("login"))                        
                except:
                    flash("login format data not correct", "warning")
                    return redirect(url_for("login"))
            else:
                flash("Confirm your not robot", "warning")
                return redirect(url_for("login"))  
        elif checkform == "register":
            try:
                register = RegisterModel(
                            username = request.form['rusername'],
                            password = request.form['rpassword'],
                            confirmpassword = request.form['rcpassword'])
                if register.password == register.confirmpassword:
                    ruser = db.read_from_database_by_username(register.username)
                    if ruser is None:
                        password_byte = register.password.encode("utf-8")
                        hashed_password = bcrypt.hashpw(password_byte, bcrypt.gensalt())
                        db.add_to_database(register.username, hashed_password)
                        return render_template("login.html", tabactivelogin="tab-pane fade show active", login_b="nav-link active", tabactiveregister="tab-pane fade", register_b="nav-link")
                    else:
                        flash("username is existed", "warning")
                        return render_template("login.html", tabactivelogin="tab-pane fade", login_b="nav-link", tabactiveregister="tab-pane fade show active", register_b="nav-link active")
                else:
                    flash("Passwords are not match.", "warning")
                    return render_template("login.html", tabactivelogin="tab-pane fade", login_b="nav-link", tabactiveregister="tab-pane fade show active", register_b="nav-link active")
            except:
                flash("Datas entered format's are not correct", "warning")
                return render_template("login.html", tabactivelogin="tab-pane fade", login_b="nav-link", tabactiveregister="tab-pane fade show active", register_b="nav-link active")