from Site import db


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(db.String(1024), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    
    @staticmethod
    def f(action:str) -> int:
        p = Permission.query.filter_by(
            action=action).first()
        return p.priority if p else None
    