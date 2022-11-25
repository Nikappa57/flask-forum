from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from Site import app, db
from Site.models.users import Users
from Site.views.Main.src.forms import LoginForm, RegisterForm
from Site.views.Main.src.messages import Error, Success
from Site.src.linkaccount import LinkAccount


@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if user is None or not user.check_password(form.password.data):
            flash(Error.passw_error, Error.name)

            return redirect(url_for('login'))

        login_user(user, remember=str(form.remember_me.data))

        return "userpanel" #TODO
    
    return render_template('login-manager/login.html', form=form)

@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
   
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data

        # Check Username
        check_username = Users.query.filter_by(username=username).first()
        if check_username:
            flash(Error.username, Error.name)
            return redirect(url_for('register'))


        new_user = Users(
            username=username,
            password=form.password.data,
            email=form.email.data
        )
        new_user.set_password_hash()

        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            flash(Error.generic)
            return render_template("main/register.html", form=form)
            
        login_user(new_user, remember=True)

        return redirect(url_for('homepage'))
        return "User Panel" #TODO

    return render_template("login-manager/register.html", form=form)


@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def resetpassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    try:
        email = LinkAccount.confirm_token(token)[0]
    except:
        return Error.link_expired
    
    user = Users.query.filter_by(email=email).all()

    if not user:
        return Error.link_expired
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = user[-1]
        user.password = form.password.data
        user.set_password_hash()

        db.session.commit()
        flash(Success.password_reset, Success.name)
        return "User Panel" #TODO
    return render_template('login-manager/reset-password.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for('homepage'))

