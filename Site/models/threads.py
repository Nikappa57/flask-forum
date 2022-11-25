from datetime import datetime

from Site import db
from Site.views.Forum.src import utilis
from Site.models.users import Users
from Site.models.threads_view import ThreadsViews

class Threads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)

    pinned = db.Column(db.Boolean, default=False)
    closed = db.Column(db.Boolean, default=False)

    title = db.Column(db.String(60), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    slug = db.Column(db.String(250), unique=True)
    img = db.Column(db.String(120))
    
    threadViews = db.relationship('ThreadsViews', backref='threadViews')
    comments = db.relationship('Comments', backref='comments')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

    @property
    def user(self) -> Users:
        return Users.query.get(self.user_id)
    
    @property
    def views(self) -> int:
        return len(self.threadViews)

    def add_view(self, user_id:int) -> None:
        if not Users.query.get(user_id):
            return
            
        if ThreadsViews.query.filter_by(thread_id=self.id, user_id=user_id).all():
            return
            
        new_view = ThreadsViews(
            user_id=user_id,
            thread_id=self.id
        )
        db.session.add(new_view)
        db.session.commit()
    
    def title_sluggifier(self) -> None:
        self.slug = "{}-{}".format(utilis.slugify(self.title), 
            utilis.generate_random_string())