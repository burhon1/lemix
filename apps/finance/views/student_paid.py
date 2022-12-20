from http.client import HTTPResponse
from django.shortcuts import render,redirect
from paycomuz import Paycom
from paycomuz.views import MerchantAPIView
from paycomuz import Paycom
from paycomuz.models import Transaction
from rest_framework.generics import CreateAPIView
from pyclick import PyClick
from pyclick.views import PyClickMerchantAPIView
from django.urls import reverse
from django.http import JsonResponse
import json
from clickuz import ClickUz
from clickuz.views import ClickUzMerchantAPIView
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

def check_paid(request,id):
    paycom = Paycom()
    url = paycom.create_initialization(amount=5.00, order_id='197', return_url='https://example.com/success/')
    # print(url)
    print(url)
    return redirect(url)  

class CheckOrder(Paycom):
    # order = 'bu yerda Order ID buladi'
    # account = 'bu yerga qaysi account ni yozish kerak?'

    def check_order(self, amount, account, *args, **kwargs):
        # print(,args)
        result=None
        result = Transaction.objects.filter(order_key=account['Lemix_kassa'])
        key_tran = kwargs.get('id',False)
        
        if key_tran:
            return self.ORDER_FOUND
            
        if result.exists():
            if int(result.first().amount)*100!=amount:
                return self.INVALID_AMOUNT    
            elif result.exists() and int(result.first().amount)*100==amount:
                return self.ORDER_FOUND
        else:
            return self.ORDER_NOT_FOND
        
        # if result.exists(): #ma'lumotlari omborida huddi shunday buyurtma bor narxi ham to'g'ri keladi 
        #     return self.ORDER_FOUND 
        # else: #agar bunday buyurtma bo'lmasa 
        #     return self.ORDER_NOT_FOND   
        
    def successfully_payment(self, account, transaction, *args, **kwargs):
        print(account,1)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        print(account)
        # now = timezone.now()
        # print(now,2)
      
    # result = check_order(amount=1, account=2222)

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder
    # VALIDATE_CLASS.cancel_payment()

def pay_student(request):
    url = ClickUz.generate_url(order_id='1',amount='1000')
    print(url)
    
    return HttpResponseRedirect(url)

from clickuz.views import ClickUzMerchantAPIView


class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: str):
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        print(order_id)

class TestClickView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment

    
#pip install

class CreateClickOrderView(CreateAPIView):
    serializer_class = ClickOrderSerializer

    def post(self, request, *args, **kwargs):
        amount = request.POST.get('amount')
        order = ClickOrder.objects.create(amount=amount)
        return_url = 'http://t.lemix.uz/finance/fnc'
        url = PyClick.generate_url(order_id=order.id, amount=str(amount), return_url=return_url)
        return redirect(url)

class OrderCheckAndPayment(PyClick):
    def check_order(self, order_id: str, amount: str):
        print(order_id,amount)
        if order_id:
            try:
                order = ClickOrder.objects.get(id=order_id)
                if int(amount) == order.amount:
                    return self.ORDER_FOUND
                else:
                    return self.INVALID_AMOUNT
            except ClickOrder.DoesNotExist:
                return self.ORDER_NOT_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        try:
            order = ClickOrder.objects.get(id=order_id)
            order.is_paid = True
            order.save()
        except ClickOrder.DoesNotExist:
            print(f"no order object not found: {order_id}")


class OrderTestView(PyClickMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment 