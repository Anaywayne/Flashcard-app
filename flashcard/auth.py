from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login' ,methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):

                login_user(user,remember=True)
                return redirect(url_for("views.dashboard"))
            else:
                flash("Incorrect Password,try again",category = "error")
        else:
            flash("User doesn't exist",category = "error")

    return redirect(url_for("views.home"))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/sign-up',methods = ["GET","POST"])
def sign_up():
    if request.method == "POST":
        email = request.form['email']
        first_name = request.form['Name']
        password1 = request.form['password1']


        user = User.query.filter_by(email = email).first()
        if user:
            flash("Email already exists",category = "error")
        elif len(password1) < 4:
            flash("Password must be atleast 4 character long",category = "error")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created !",category = "success")
            return redirect(url_for("views.home"))
    return render_template("home.html")
