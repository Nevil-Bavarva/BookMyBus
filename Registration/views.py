from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login


# Create your views here.
def registration(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        email =request.POST.get("email","")

        user = User.objects.create_user(username=username,password=password, email=email)
        user.save()
        print('user created')
        return redirect("/login")
    else:
        return render(request,"LoginRegister/Register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            print("ufff yeh invalid integrity")
            return redirect("/login")
    else:
        return render(request, "LoginRegister/Login.html")
