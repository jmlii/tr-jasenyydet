from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, UserForm


# Käyttäjien sisäänkirjautuminen
@app.route("/auth/login/", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user or user.account_active == False:
        return render_template("auth/loginform.html", form = form, error = "No such username or password")

    login_user(user)
    return redirect(url_for("index"))    

# Käyttäjän uloskirjautuminen
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))


# Käyttäjien listaaminen
@app.route("/users/", methods=["GET"])
def users_index():
    return render_template("auth/list.html", users = User.query.all())

# Uuden käyttäjän luominen
@app.route("/users/new/")
def users_form():
    return render_template("/auth/new.html", form = UserForm())

# Luodun käyttäjän tiedot tietokantaan
@app.route("/users/", methods=["POST"])
def users_create():
    form = UserForm(request.form)
    
    if not form.validate():
        return render_template("auth/new.html", form=form)

    u = User(form.first_name.data, form.last_name.data, 
        form.username.data, form.password.data)
    
    db.session().add(u)
    db.session().commit()

    return redirect(url_for("users_index"))
    
@app.route("/users/inactivate<user_id>/", methods=["POST"])
def users_set_inactive(user_id):
    u = User.query.get(user_id)
    u.account_active = False
    u.date_inactivated = db.func.current_timestamp()
    db.session().commit()

    return redirect(url_for("users_index"))