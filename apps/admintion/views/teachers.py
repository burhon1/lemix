from django.shortcuts import render,redirect
from django.urls import reverse

def teachers_view(request):
    return render(request,'admintion/roomslist.html') 