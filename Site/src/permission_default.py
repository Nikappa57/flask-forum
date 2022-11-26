from Site import db
from Site.models.permission import Permission


default = [
    ('create category', 1000),
    ('edit category', 500),
    ('delete category', 1000),

    ('create section', 500),
    ('edit section', 500),
    ('delete section', 500),

    ('close thread', 300),
    ('delete thread', 300),
    ('create thread', 0),
    ('pin thread', 500),

    ('delete comment', 300),
    ('create comment', 0),

    ('admin panel', 1000),
    ('limit user', 300),
]

def create_default_permission() -> None:
    """
    Create Default Permission

    - admin panel

    - limit user

    - create category
    - add section
    - close thread
    - delete thread
    - delete comment
    - pin thread
    """
    
    for action, priority in default:
        if not Permission.query.filter_by(action=action).first():
            new_perm = Permission(
                action=action,
                priority=priority
            )
            db.session.add(new_perm)

        db.session.commit()