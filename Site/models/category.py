from datetime import datetime

from Site import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.Integer, nullable=False)

    sections = db.relationship('Section', backref='sections', 
        order_by="Section.position")
    
    def to_show(self, user):
        for section in self.sections:
            if user.priority >= section.priority_required:
                return True
        return False
