from Site import db
from Site.models.rank import Rank


default = {
    'owner': {'priority': 1000, 'tag': 'Owner', 'tag_color': 'danger'},
    'admin': {'priority': 500, 'tag': 'Admin', 'tag_color': 'success'},
    'moderator': {'priority': 300, 'tag': 'Mod', 'tag_color': 'warning'},
    'user': {'priority': 0, 'tag': 'User', 'tag_color': 'dark'}, # Default rank must have 0 priority
}

def create_default_ranks() -> None:
    """
    Create Default Rank

    - priority
    - tag
    - color
    """
    if not Rank.query.all():
        for rank in default:
            new_perm = Rank(
                name=rank,
                priority=default[rank]['priority'],
                tag=default[rank]['tag'],
                tag_color=default[rank]['tag_color'],
            )
            db.session.add(new_perm)

        db.session.commit()