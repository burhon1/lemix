from django.shortcuts import render,redirect
from django.urls import reverse

def leads_view(request):
    context = {}
    return render(request,'admintion/lid.html',context) 