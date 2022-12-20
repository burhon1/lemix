from http.client import HTTPResponse
from django.shortcuts import render,redirect
from rest_framework.generics import CreateAPIView
from django.urls import reverse
from django.http import JsonResponse
import json
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from admintion.models import Student
from finance.services.paid import student_paid
from finance.serializers import *

# Create your views here.
def student_pay(request,id):
    if request.method == "POST":
        post = request.POST
        student = Student.objects.filter(id=id).first()
        price = post.get('price',False)
        goal_type = post.get('goal-type',False)
        paid_type = post.get('pay-type',False)
        description = post.get('description',False)
        student_paid(student,price,paid_type,goal_type,description,request.user)
        return redirect(reverse('admintion:student-detail',kwargs={'id':id})+f"?success={True}")


def group_students_pay(request):
    data = json.loads(request.body)
    student = Student.objects.filter(id=data['id']).first()
    price = data.get('price',False)
    goal_type = data.get('goal_type',False)
    paid_type = data.get('pay_type',False)
    description = data.get('description',False)
    val = student_paid(student,price,paid_type,goal_type,description,request.user)
    return JsonResponse({'status':201,'balance':val}) 






