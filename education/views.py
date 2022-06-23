from django.shortcuts import render

# Create your views here.

def test2_view(request):
    return render(request,'education/test.html')    

def groups_list_view(request):
    return render(request,'education/groups_list.html')  

def courses_list_view(request):
    return render(request,'education/courses_list.html')  
   