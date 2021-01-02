'''
class User:
    is_superuser = False
    is_active = True
    is_staff = True
    id = 1
    pk = 1
'''

from django.contrib.auth.models import User, AnonymousUser


def stub(*args, **kwargs):
    return True

User.has_module_perms = stub
User.has_perm = stub

import explorer.views
#explorer.views.query.PlayQueryView.permission_required = 'view_permission'
#explorer.views.SchemaView.permission_required = 'view_permission'
explorer.views.query.QueryView.permission_required = 'super_permission'
explorer.views.CreateQueryView.permission_required = 'super_permission'
explorer.views.DeleteQueryView.permission_required = 'super_permission'
import explorer.permissions
def super_permission(request, *args, **kwargs):
    return request.user.is_superuser
explorer.permissions.super_permission = super_permission
#explorer.views.query..permission_required = 'view_permission'

from django.contrib.auth.middleware import get_user


class Middleware(object):
    def __init__(self, get_response):
        self.response = get_response

    def __call__(self, request):
        request.user = get_user(request)
        if isinstance(request.user, AnonymousUser) and not request.GET.get("forceauth"):
            request.user = User.objects.get(username='public')
        return self.response(request)