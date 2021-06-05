from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

name =None
def home(request):
    name=None
    if request.session.has_key('name'):
        name=request.session['name']
    return render(request,"home.html" ,{'name':name})