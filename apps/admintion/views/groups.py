from django.shortcuts import render,redirect
from django.urls import reverse

def groups_view(request):
    context = {}
    if request.method == "POST":
        post = request.POST
    return render(request,'admintion/groups.html',context)