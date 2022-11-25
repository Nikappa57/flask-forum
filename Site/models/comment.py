from datetime import datetime

from Site import db
from Site.models.users import Users
from Site.models.cmt_upvote import CmtUpvote

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)

    text = db.Column(db.String(1024), nullable=False)

    subcomments = db.relationship('Subcomments', backref='subcomments')
    upvote = db.relationship('CmtUpvote', backref='upvote')
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))

    @property
    def user(self) -> Users:
        return Users.query.get_or_404(self.user_id)
    
    @property
    def upvote_num(self) -> int:
        return len(self.upvote)
    
    def check_upvote(self, user_id:int) -> CmtUpvote or None:
        for u in self.upvote:
            if u.user_id == user_id:
                return u
        return None