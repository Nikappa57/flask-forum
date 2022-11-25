from Site import db


class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(1024), nullable=False, unique=True)
    priority = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(16), nullable=False)
    tag_color = db.Column(db.String(16), nullable=False)

    users = db.relationship('Users', backref='user_rank')

    def __repr__(self) -> str:
        return "{} ({})".format(self.name, self.priority)