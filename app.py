from flask import Flask, flash, session, render_template, request, redirect, url_for
from database import Database, LoginModel, RegisterModel
from bmr import BmrInputs, Bmr
import bcrypt
import os
import ast
from age_prediction import predict

app = Flask("personal website")
app.config["UPLOAD_FOLDER"] = './static/uploads'
app.config["ALLOWED_EXTENSIONS"] = {'png', 'jpg', 'jpeg'}
app.secret_key = "javad personal website"
db = Database()
bmrcal = Bmr()
# loginuser = ""

def allowed_files(file_name):
    return True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/read-your-mind", methods=["POST", "GET"])
def read_your_mind():
    if request.method == "POST":
        x = request.form["number"]

        return redirect(url_for("read_your_mind_result", number=x))
    
    return render_template("read-your-mind.html")

@app.route("/read-your-mind/result", methods=["POST", "GET"])
def read_your_mind_result():
    y = request.args.get("number")
    
    return render_template("read-your-mind-result.html", number=y)

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
        if request.method == 'POST':
            if request.form["appnum"] == "5":
                try:
                    usernumber = float(request.form["usernum"])
                    return redirect(url_for("aiapps", usernumber=usernumber))
                    # return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser, bmr=bmr_res)
                except:
                    flash({"type":"warning", "id":5, "text": "Input format data is not correct"})
                    # return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser)
                    return redirect(url_for("aiapps"))
            if request.form["appnum"] == "2":
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
                    return redirect(url_for("aiapps", bmr=bmr_res))
                    # return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser, bmr=bmr_res)
                except:
                    flash({"type":"warning", "id":2, "text": "Input format data is not correct"})
                    # return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser)
                    return redirect(url_for("aiapps"))
            elif request.form["appnum"] == "1":
                my_image = request.files['face']
                if my_image.filename == "":
                    flash({"type":"info", "id":1, "text": "First, you must upload your file."})
                    return redirect(url_for("aiapps"))
                    # return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser)
                else:
                    if my_image and allowed_files(my_image.filename):
                        save_path = os.path.join(app.config["UPLOAD_FOLDER"], my_image.filename)    
                        my_image.save(save_path)
                        paths = predict(save_path)
                        print(paths)
                    return redirect(url_for("aiapps", paths=f"{paths}"))
                    # return render_template("aiapps.html", tabactivelogin="tab-pane fade show active", tabactiveregister="tab-pane fade", username=loginuser, paths=paths)
        # if request.args.get("origin") == "frompost":
        paths = request.args.get('paths')
        bmr_res = request.args.get("bmr") 
        usernumber = request.args.get("usernumber")
        # else:
        print("session: ",session["user_name"])
        if bmr_res == None:
            bmr_res = " "
        if usernumber == None:
            usernumber = " "
        if paths == None:
            paths = []
        else:
            paths = ast.literal_eval(paths)
        tabactivelogin = "tab-pane fade show active"
        tabactiveregister = "tab-pane fade" 
        print("BMR_RES", usernumber)
        return render_template("aiapps.html", tabactivelogin=tabactivelogin, tabactiveregister=tabactiveregister, bmr=bmr_res, paths=paths, usernumber=usernumber, username=session["user_name"])
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
                            session["user_name"] = luser.username
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