from Site import db
from Site.models.permission import Permission


default = [
    ('create category', 0),
    ('edit category', 0),
    ('delete category', 0),

    ('create section', 0),
    ('edit section', 0),
    ('delete section', 0),

    ('close thread', 0),
    ('delete thread', 0),
    ('open thread', 0),
    ('pin thrad', 0),

    ('delete comment', 0),
    ('create comment', 0),

    ('admin panel', 0),
    ('limit user', 0),
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