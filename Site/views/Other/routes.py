from flask import render_template

from Site import app, db
from Site.models.users import Users


@app.route("/profile/<string:username>/")
def profile(username:str):
    user = Users.query.filter_by(username=username).first_or_404()
    return render_template('other/user.html', user=user)
