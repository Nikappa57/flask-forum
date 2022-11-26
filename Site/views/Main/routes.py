from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from Site import app, db
from Site.models.users import Users
from Site.views.Main.src.forms import LoginForm, RegisterForm, \
    ResetPasswordForm, ResetPassword2Form
from Site.views.Main.src.messages import Error, Success
from Site.src.linkaccount import LinkAccount
from Site.src.email import send_email

@app.route("/")
def homepage():
    return redirect(url_for("forumHomepage"))
    # return render_template("homepage.html")

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
        new_user.set_rank('user')

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



@app.route("/reset-password/", methods=['GET', 'POST'])
def resetpassword():
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if not user:
            flash("There is no user with this email", "error")
            return redirect(url_for('login'))

        token = user.generate_confirmation_token()
        reset_url = url_for('reset_password_token', token=token, _external=True)
        html = render_template('mail/reset.html', reset_url=reset_url)
        subject = "Reset your password"
        send_email(user.email, subject, html)

        flash("Reset email sent successfully", "success")
        return redirect(url_for('login'))
    return render_template('login-manager/reset-password.html', form=form)


@app.route("/reset-password/<token>", methods=['GET', 'POST'])
def reset_password_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    try:
        email = Users.confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'error')

        return redirect(url_for('login'))
    
    user = Users.query.filter_by(email=email).all()
    if not user:
        flash('The confirmation link is invalid or has expired.', 'error')

        return redirect(url_for('login'))
    
    form = ResetPassword2Form()
    if form.validate_on_submit():
        user = user[-1]
        user.password = form.password.data
        user.set_password_hash()

        db.session.commit()
        flash('password successfully reset', 'success')
        return redirect(url_for('login'))
    return render_template('login-manager/reset-password-2.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for('homepage'))

