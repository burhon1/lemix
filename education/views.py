from django.shortcuts import render

# Create your views here.

def test2_view(request):
    return render(request,'education/test.html')    

def teachers_view(request):
    return render(request,'education/teachers.html')  

def courses_list_view(request):
    return render(request,'education/courses_list.html')    
   
def course_detail_view(request,id):
    return render(request,'education/course_detail.html') 

def teacher_detail_view(request,id):
    return render(request,'education/teacher_detail.html') 
    
def group_detail_view(request,id):
    return render(request,'education/group_detail.html') 

def employe_detail_view(request,id):
    return render(request,'education/employe_detail.html') 
    
def teacher_add_view(request):
    return render(request,'education/teacheradd.html')     

def groupslist_view(request):
    return render(request,'education/guruhlar.html')  

def roomslist_view(request):
    return render(request,'education/roomslist.html')    

def employees_view(request):
    return render(request,'education/employees.html') 

def students_list_view(request):
    return render(request,'education/students_list.html') 

def parents_list_view(request):
    return render(request,'education/parents_list.html')

def expenses_list_view(request):
    return render(request,'education/expenses.html')