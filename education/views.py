from django.shortcuts import render

# Create your views here.

def test2_view(request):
    return render(request,'education/test.html')    

def groups_list_view(request):
    return render(request,'education/groups_list.html')  

def courses_list_view(request):
    return render(request,'education/courses_list.html')  
   
def course_detail_view(request,id):
    return render(request,'education/course_detail.html') 

<<<<<<< HEAD
def teacher_detail_view(request,id):
    return render(request,'education/teacher_detail.html') 

def employe_detail_view(request,id):
    return render(request,'education/employe_detail.html')   
=======
def techear_add_view(request):
    return render(request,'education/teacheradd.html')     

def guruhlar_view(request):
    return render(request,'education/guruhlar.html')  

def roomslist_view(request):
    return render(request,'education/roomslist.html')    

def employees_view(request):
    return render(request,'education/employees.html') 
>>>>>>> 6a796d0ab23f145efcbb6790741c911bdd95251b
