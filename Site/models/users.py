from datetime import datetime

from flask import url_for
from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from Site import db, login_manager
from Site.models.permission import Permission
from Site.models.rank import Rank


@login_manager.user_loader
def load_user(id:int):
    return Users.query.get(int(id))

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    
    username = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(52), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    limited = db.Column(db.Boolean, default=False)

    rank_id = db.Column(db.Integer, db.ForeignKey('rank.id'))

    threads = db.relationship('Threads', backref='user_threads')
    comments = db.relationship('Comments', backref='user_comments')
    subcomments = db.relationship('Subcomments', backref='user_subcomments')
    threadViews = db.relationship('ThreadsViews', backref='user_threadViews')
    cmtupvotes = db.relationship('CmtUpvote', backref='cmtupvotes')
    subupvotes = db.relationship('SubUpvote', backref='subupvotes')


    def set_password_hash(self) -> None:
        self.password = generate_password_hash(self.password)

    def set_rank(self, rank_name) -> None:
        self.rank_id = Rank.query.filter_by(name=rank_name).first().id

    def check_password(self, password:str) -> bool:
        return check_password_hash(self.password, password)
    
    @property
    def priority(self) -> int:
        return Rank.query.get_or_404(self.rank_id).priority

    @property
    def rank(self) -> int:
        return Rank.query.get_or_404(self.rank_id).name

    @property
    def tag(self) -> set:
        return "@" + self.username

    @property
    def profile_link(self) -> str:
        return url_for('profile', username=self.username)

    def check_perm(self, action:str) -> int or None:
        limited_fuction = (
            'create thread',
            'create comment'
        )

        p = Permission.f(action)
        if p is None:
            return False

        if current_user.priority < p:
            return False
        
        if current_user.limited:
            if action in limited_fuction:
                return False

        return True

    def __repr__(self) -> str:
        return f"User('{ self.id }', '{self.create_at}')"
