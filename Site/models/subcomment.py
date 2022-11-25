from datetime import datetime

from Site import db
from Site.models.users import Users
from Site.models.sub_upvote import SubUpvote

class Subcomments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    text = db.Column(db.String(1024), nullable=False)
    to_user_id = db.Column(db.Integer, nullable=False)

    upvote = db.relationship('SubUpvote', backref='upvote')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    @property
    def user(self) -> Users:
        return Users.query.get(self.user_id)

    @property
    def upvote_num(self) -> int:
        return len(self.upvote)
    
    @property
    def tag(self) -> set or None:
        tag_user = Users.query.get(self.to_user_id)
        
        if not tag_user:
            return ""

        # user_link = url_for('profile', user_id=tag_user.id)
        return ("@" + tag_user.username, tag_user) # user_link

    def check_upvote(self, user_id:int) -> SubUpvote or None:
        for u in self.upvote:
            if u.user_id == user_id:
                return u
        return None