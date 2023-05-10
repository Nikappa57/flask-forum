from datetime import datetime

from Site import db
from Site.views.Forum.src import utilis


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)

    name = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String(1024), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    priority_required = db.Column(db.Integer, default=0)
    priority_required_create = db.Column(db.Integer, default=0)
    slug = db.Column(db.String(250), unique=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    threads = db.relationship('Threads', backref='threads')

    def title_sluggifier(self) -> None:
        self.slug = "{}-{}".format(utilis.slugify(self.name), 
            utilis.generate_random_string())

    def to_show(self, user) -> bool:
        if (user.is_authenticated and user.rank.priority >= self.priority_required):
            return True
        return self.priority_required == 0

    @property
    def last_post(self):
        return self.threads[-1] if self.threads else None
