from datetime import date


from flask import abort
from wtforms import SelectField
from flask_login import current_user
from flask_admin.model import typefmt
from flask_admin.contrib.sqla import ModelView

from Site.models.rank import Rank


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: lambda view, value: value.strftime('%d/%m/%Y %H:%M:%S')
})

class LimitedModelView(ModelView):
    column_type_formatters = MY_DEFAULT_FORMATTERS

    def is_accessible(self):
        if not current_user.is_authenticated:
            return abort(401)

        if not current_user.check_perm('admin panel'):
            return abort(401)
        
        return True


class UsersViews(LimitedModelView):
    column_list = ('create_at', 'email', 'limited')
    column_editable_list = ('email', 'limited')
    
    can_create, can_delete, can_edit = False, False, True
    column_searchable_list = ('email',)


class PermsViews(LimitedModelView):
    can_create, can_delete = False, False
    column_editable_list = ('id', 'priority')

    form_overrides = dict(
        priority=SelectField
    )

    form_args = dict(
        priority=dict(
            choices=[
                (rank.priority, rank.name) for rank in Rank.query.all()
            ],
            coerce=int
        )
    )
