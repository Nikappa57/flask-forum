from Site import admin, db
from Site.models.users import Users
from Site.models.permission import Permission
from Site.views.Admin.src import admin_view

admin.add_view(admin_view.UsersViews(Users, db.session))
admin.add_view(admin_view.PermsViews(Permission, db.session))