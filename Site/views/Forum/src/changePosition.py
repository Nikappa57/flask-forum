from Site.models.category import Category
from Site.models.section import Section


def category(position:int, last_position:int=None) -> None:
    category_to_change = Category.query.filter_by(
        position=position).first()
    
    if category_to_change:
        if last_position:
            if category_to_change.position == last_position:
                return
        else:
            last_position = Category.query.order_by(
                'position').all()[-1].position + 1
        
        if category_to_change.position < last_position:
            category(position=category_to_change.position + 1,
                last_position=last_position)
            category_to_change.position += 1
        else:
            category(position=category_to_change.position - 1,
                last_position=last_position)
            category_to_change.position -= 1



def section(position:int, category_id:int, last_position:int=None) -> None:
    section_to_change = Section.query.filter_by(position=position, 
        category_id=category_id).first()
    if section_to_change:
        if last_position:
            if section_to_change.position == last_position:
                return
        else:
            last_position = Section.query.filter_by(
                category_id=category_id).order_by('position'
                    ).all()[-1].position + 1
        if section_to_change.position < last_position:
            section(position=section_to_change.position + 1, 
                category_id=category_id, last_position=last_position)
            section_to_change.position += 1
        else:
            section(position=section_to_change.position - 1, 
                category_id=category_id, last_position=last_position)
            section_to_change.position -= 1
