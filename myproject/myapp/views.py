from django.shortcuts import render
from decimal import Decimal
from django.db.models import Sum
from django.db.models import F

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

name =None
user_id = None
def home(request):
    name = user_id = None
    if request.user.is_authenticated:
        if request.session.has_key('name'):
            name = request.session['name']
            user_id = request.session['id']
            return render(request, 'myapp/home.html', {'name':name, 'user_id':user_id})
        else:
            return render(request, 'myapp/signin.html' ,{'error':'something wrong occured, try signing again '})
        return render(request, 'myapp/signin.html')
    else:
        return render(request, 'myapp/signin.html')


@login_required(login_url='signin')
def findbus(request):
    context = {}
    if request.method == 'POST':
        source_r = request.POST.get('source')
        dest_r = request.POST.get('destination')
        date_r = request.POST.get('date')
        bus_list = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r)
        bus_name = Bus.objects.filter(source=source_r, dest=dest_r, date=date_r).values('bus_name')
        if bus_list:
            return render(request, 'myapp/list.html',{'bus_list':bus_list})
        else:
            context["error"] = "Sorry no buses availiable"
            return render(request, 'myapp/index.html', context)
    else:
        return render(request, 'myapp/index.html')


@login_required(login_url='signin')
def bookings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('cars')
        seats_r = int(request.POST.get('no_seats'))
        bus = Bus.objects.get(id=id_r)
        if bus:
            if bus.rem >= int(seats_r) and bus.rem !=0:
                name_r = bus.bus_name
                cost = int(seats_r) * bus.price
                source_r = bus.source
                dest_r = bus.dest
                nos_r = Decimal(bus.nos)
                price_r = bus.price
                date_r = bus.date
                time_r = bus.time
                username_r = request.user.username
                email_r = request.user.email
                userid_r = request.user.id
                rem_r = bus.rem - seats_r
                Bus.objects.filter(id=id_r).update(rem=rem_r)
                book = Book.objects.create(name=username_r, email=email_r, userid=userid_r, bus_name=name_r,
                                           source=source_r, busid=id_r,
                                           dest=dest_r, price=price_r, nos=seats_r, date=date_r, time=time_r,
                                           status='BOOKED')
                print('------------book id-----------', book.id)
                # book.save()
                return render(request, 'myapp/bookings.html', locals())
            else:
                context["error"] = "Sorry selected seats not available"
                return render(request, 'myapp/index.html', context)

    else:
        return render(request, 'myapp/index.html')


@login_required(login_url='signin')
def cancellings(request):
    context = {}
    if request.method == 'POST':
        id_r = request.POST.get('bus_id')
        #seats_r = int(request.POST.get('no_seats'))

        try:
            book = Book.objects.get(id=id_r)
            bus = Bus.objects.get(id=book.busid)
            rem_r = bus.rem + book.nos
            Bus.objects.filter(id=book.busid).update(rem=rem_r)
            #nos_r = book.nos - seats_r
            Book.objects.filter(id=id_r).update(status='CANCELLED')
            Book.objects.filter(id=id_r).update(nos=0)
            return redirect(seebookings)
        except Book.DoesNotExist:
            context["error"] = "Sorry You have not booked that bus"
            return render(request, 'myapp/error.html', context)
    else:
        return render(request, 'myapp/index.html')


@login_required(login_url='signin')
def seebookings(request,new={}):
    context = {}
    id_r = request.user.id
    book_list = Book.objects.filter(userid=id_r)
    if book_list:
        return render(request, 'myapp/booklist.html', locals())
    else:
        context["error"] = "Sorry no buses booked"
        return render(request, 'myapp/index.html', context)


def signup(request):
    session_id = request.session._get_or_create_session_key()
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        email_r = request.POST.get('email')
        password_r = request.POST.get('password')
        user = User.objects.create_user(name_r, email_r, password_r, )
        if user:
            login(request, user)
            request.session['name'] = name_r
            request.session['id'] = request.user.id
            return render(request, 'myapp/thank.html')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signup.html', context)
    else:
        return render(request, 'myapp/signup.html', context)


def signin(request):
    session_id = request.session._get_or_create_session_key()
    context = {}
    if request.method == 'POST':
        name_r = request.POST.get('name')
        password_r = request.POST.get('password')
        user = authenticate(request, username=name_r, password=password_r)
        if user:
            login(request, user)
            request.session['name'] = name_r
            request.session['id'] = request.user.id
            # context["user"] = name_r
            # context["id"] = request.user.id
            # return render(request, 'myapp/success.html', context)
            return render(request, 'myapp/success.html')
            # return HttpResponseRedirect('success')
        else:
            context["error"] = "Provide valid credentials"
            return render(request, 'myapp/signin.html', context)
    else:
        context["error"] = "You are not logged in"
        return render(request, 'myapp/signin.html', context)


@login_required(login_url='signin')
def update(request):
    book_id = request.POST.get('custId')
    book_ = Book.objects.filter(id=book_id)
    print("total-------------")
    cost = Book.objects.filter(id=book_id).aggregate(total=Sum(F('nos') * F('price')))['total']
    print(cost)
    if book_ is not None:
        return render(request,'myapp/update_seats.html', {'book_data':book_ , 'cost':cost})
    return render(request,'myapp/update_seats.html')
   
def update_seats(request):
    context ={}
    final = 0
    if request.method == "POST":
        busid = request.POST.get('custId')
        bookid = request.POST.get('bookId')
        seats= request.POST.get('u_seats')
        bookedseats =  Book.objects.filter(id=bookid).values_list('nos', flat=True)[0]
        number = Bus.objects.filter(id=busid).values_list('rem', flat=True)[0]
        remaining= str(int(number))
        print('remain:')
        print(remaining)
        print('seats:')
        print(seats)
        print('booked seats:')
        print(bookedseats)
        if int(remaining) <= 0:
            if int(seats) < int(bookedseats):
                final = int(remaining) + int(int(bookedseats) - int(seats))
        elif int(seats) == int(bookedseats):
                final = int(remaining) 
        else:
            if int(seats) < int(bookedseats):
                final = int(remaining) + int(int(bookedseats) - int(seats))
            elif int(seats) > int(bookedseats):
                final = int(remaining) - int(int(seats) - int(bookedseats))
            
            
        print('final')
        print(final)
        if int(seats) < (int(remaining) + int(seats)) :
            Book.objects.filter(id=bookid).update(nos=seats)
            Bus.objects.filter(id=busid).update(rem=final)
            return redirect('seebookings')
        else:
            book_ = Book.objects.filter(id=bookid)
            cost = Book.objects.filter(id=bookid).aggregate(total=Sum(F('nos') * F('price')))['total']
            if book_ is not None:
                return render(request,'myapp/update_seats.html', {'book_data':book_ , 'cost':cost, 'error':'number of entered seats not available'})
            
    return render(request , 'myapp/home.html')

def signout(request):
    context = {}
    logout(request)
    try:
        del request.session['name']
        return redirect('signin')
    except:
      pass
    context['error'] = "You have been logged out"
    return render(request, 'myapp/signin.html', context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'myapp/success.html', context)
