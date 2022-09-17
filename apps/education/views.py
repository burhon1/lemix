from django.shortcuts import render

# Create your views here.

def test2_view(request):
    return render(request,'education/test.html')     

def teachers_view(request):
    return render(request,'education/teachers.html')

def lid_view(request):
    return render(request,'education/lid.html')

def lid_royhati_view(request):
    return render(request,'education/lidlar_royxati.html')

def lid_arxiv_view(request):
    return render(request,'education/lid.html')  

def onlin_view(request):
    return render(request,'education/onlin.html')  

def onlins_view(request,id):
    return render(request,'education/onlins.html') 

def courses_list_view(request):
    return render(request,'education/courses_list.html')    
   
def course_detail_view(request,id):
    return render(request,'education/course_detail.html') 

def teacher_detail_view(request,id):
    return render(request,'education/teacher_detail.html') 
    
def group_detail_view(request,id):
    return render(request,'education/group_detail.html') 

def student_detail_view(request,id):
    return render(request,'education/student_detail.html') 

def employe_detail_view(request,id):
    return render(request,'education/employe_detail.html') 

def parents_detail_view(request,id):
    return render(request,'education/parents_detail.html')     
    
def teacher_add_view(request):
    return render(request,'education/teacheradd.html')     

def groupslist_view(request):
    return render(request,'education/guruhlar.html')  

def roomslist_view(request):
    return render(request,'education/roomslist.html')

def task_view(request):
    return render(request,'education/task.html')    

def employees_view(request):
    return render(request,'education/employees.html') 

def students_list_view(request):
    return render(request,'education/students_list.html') 

def parents_list_view(request):
    return render(request,'education/parents_list.html')

def finance_list_view(request):
    return render(request,'education/finance_list.html')    

def expenses_list_view(request):
    return render(request,'education/expenses.html')

def debt_list_view(request):
    return render(request,'education/debt_list.html') 

def debt_groups_view(request,id):
    return render(request,'education/debt_groups.html')

def debt_course_view(request,id):
    return render(request,'education/debt_course.html')

def message_settings_view(request):
    return render(request,'education/message_settings.html') 

def lid_first_view(request):
    return render(request,'education/lid_first.html') 

def lid_sk_view(request):
    return render(request,'education/lid_sk.html') 

def lid_ry_view(request):
    return render(request,'education/lid_ry.html') 

