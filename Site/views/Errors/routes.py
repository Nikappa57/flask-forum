from flask import render_template

from Site import app
from Site.views.Errors import errors


@app.errorhandler(errors.e404.number)
def error404(error):
    return render_template("errors/error.html", 
        error=errors.e404), errors.e404.number

@app.errorhandler(errors.e401.number)
def error401(error):
    return render_template("errors/error.html", 
        error=errors.e401), errors.e401.number

@app.errorhandler(errors.e502.number)
def error502(error):
    return render_template("errors/error.html", 
        error=errors.e502), errors.e502.number