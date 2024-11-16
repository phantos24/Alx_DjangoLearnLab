from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import HttpResponseForbidden

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@user_passes_test(is_admin, login_url='/forbidden/')
def admin_view(request):
    return render(request, 'admin_view.html', {'message': 'Welcome, Admin!'})
