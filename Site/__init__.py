import sys

from flask import Flask

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

from config import Config

# APP #
app = Flask(__name__)
app.config.from_object(Config)

# DATABASE #
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)


# ADMIN #
admin = Admin(app, template_mode='bootstrap3')


# MAIL #
mail = Mail()
mail.init_app(app)


with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from Site.models.permission import Permission
    from Site.models.users import Users
    from Site.models.section import Section
    from Site.models.category import Category
    from Site.models.threads_view import ThreadsViews
    from Site.models.threads import Threads
    from Site.models.cmt_upvote import CmtUpvote
    from Site.models.comment import Comments
    from Site.models.sub_upvote import SubUpvote
    from Site.models.subcomment import Subcomments
    if not "db" in sys.argv[1]:
        from Site.views.Admin import routes
        from Site.views.Main import routes
        from Site.views.Forum import routes
        from Site.views.Errors import routes
        from Site.views.Other import routes
        from Site.src.permission_default import create_default_permission
        from Site.src.rank_default import create_default_ranks
        create_default_permission()
        create_default_ranks()