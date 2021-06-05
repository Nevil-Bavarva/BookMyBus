from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import SESSION_KEY, authenticate, login


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
    session_id = request.session._get_or_create_session_key()
    if request.method == "POST":
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['name'] = user.get_username()
            # request.session['id'] = session_id
            # print("id : " + session_id)
            return redirect("/")
        else:
            print("ufff yeh invalid integrity")
            return redirect("/login")
    else:
        return render(request, "LoginRegister/Login.html")


def Logout(request):
    try:
        del request.session['name']
        return redirect('MainIndex:home')
    except:
      pass
    return redirect('MainIndex:home')

