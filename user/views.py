from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    return render(request,'user/login.html')

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("user:login")
