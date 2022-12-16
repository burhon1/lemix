from django.shortcuts import render,redirect
from paycomuz import Paycom
from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from django.urls import reverse
from django.http import JsonResponse
import json
from clickuz import ClickUz
from django.http import HttpResponseRedirect
from admintion.models import Student
from finance.services.paid import student_paid

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

def check_paid(request,id):
    paycom = Paycom()
    url = paycom.create_initialization(amount=5.00, order_id='197', return_url='https://example.com/success/')
    # print(url)
    return redirect(url)  

class CheckOrder(Paycom):
    # order = 'bu yerda Order ID buladi'
    # account = 'bu yerga qaysi account ni yozish kerak?'

    def check_order(self, amount, account, *args, **kwargs):
        print(amount)
        # return self.ORDER_FOUND
        # return self.ORDER_NOT_FOND
        return self.INVALID_AMOUNT
        
    def successfully_payment(self, account, transaction, *args, **kwargs):
        print(account,1)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        print(account)
      
    # result = check_order(amount=1, account=2222)

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder

def pay_student(request):
    url = ClickUz.generate_url(order_id='172',amount='1000',return_url='http://example.com')
    return HttpResponseRedirect(url)

    


