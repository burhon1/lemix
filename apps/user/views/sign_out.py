from django.shortcuts import redirect
from django.contrib.auth import  logout



def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("user:login")