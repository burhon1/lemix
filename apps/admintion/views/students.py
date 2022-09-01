from django.shortcuts import render,redirect
from django.urls import reverse

def students_view(request):
    context = {}
    if request.method == "POST":
        pass
    return render(request,'admintion/students.html',context) 