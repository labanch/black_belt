from __future__ import unicode_literals
from .models import User
from ..poke.models import Poke
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
def index(request):

    return render(request, 'login/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/')

def login(request):
    result = User.objects.validate_login(request.POST)
    print 'Result'
    print result
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    request.session['user_name'] = result.name
    messages.success(request, "Successfully logged in!")
    return HttpResponseRedirect(reverse("poke:index"))

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, "Thanks for visiting. You are now logged out.")
    return redirect('/')

def success(request):
    if result['status']:
        request.session['user_id'] = result['user_id']
        path = 'poke:index'
    else:
        for error in result['errors']:
            messages.error(request, error['message'])
        path = 'login:index'
    return path

# def show(request, user_id):
#     user = User.objects.get(id=user_id)
#     unique_ids = User.pokes_made.all().values("pokes").distinct()
#     unique_pokes = []
#     for pokes in unique_ids:
#         unique_pokes.append(Pokes.objects.get(id=poke['pokes']))
#     context = {
#         'user': user,
#         'unique_pokes': unique_pokes
#     }
#     print unique_pokes.values()
#     return render(request, 'poke/index.html', context)
