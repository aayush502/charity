from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
import pdb

class RegisterRequest(View):
    def get(self, request):
        form = NewUserForm()
        return render(request, 'user/register.html', context={"form":form})
    
    def post(self, request):
        user = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1==pass2:
            reg = User(username=user, email=email, password=pass1).save()
        else:
            messages.error(request, "Password donot match.")
        return redirect('/login')

class LoginRequest(View):
    def get(self, request):
        return render(request, "user/login.html", context={})

    def post(self, request):
        user = request.POST.get('user')
        password = request.POST.get('pass')
        match_user = User.objects.filter(username=user, password=password).first()
        if match_user is not None:
            user_password = match_user.password
            if user_password == request.POST.get('pass'):
                request.session['user_id'] = match_user.id
                messages.success(request, "Successful Login!!!")
                return redirect('home')
        else:
            messages.error(request, "username or password not match", extra_tags='alert')
            return redirect('/login')
        return HttpResponse("successfull login")

class Logout(View):
    def get(self, request):
        try:
            del request.session['user_id']
        except:
            return redirect('/login')
        return redirect('/login')

class HomeView(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            return render(request, "home.html", context={})
