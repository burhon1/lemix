from django.shortcuts import render

def student_pay(request):
    return render(request,'finance/billing.html')