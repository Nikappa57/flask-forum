from Site import app, db
from Site.models.users import Users

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users}
