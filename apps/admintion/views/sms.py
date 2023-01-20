from django.shortcuts import get_list_or_404, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from admintion.services import send_sms, sms
from admintion.models import FormLead,Student,Messages,Group,Teacher,Parents,Course
from sms.services import send_messages, send_message, get_account


@login_required
def check_sms_availability(request):
    sms_integration = get_account()
    if request.method == 'POST' and sms_integration:
        sms_limit = sms_integration.free_sms
        if sms_integration.email and sms_integration.password:
            message = 'Email va parol kiritilgan'
            status = 'info'
        else:
            status = 'warning'
            message = 'Email va parol kiritilishi kerak, aks holda sms limiti tugagach sms yubora olmaysiz!'
        users = [] 
        lead_IDs = request.POST.getlist('leads', [])
        lead_IDs = [int(lead) for lead in lead_IDs]
        leads = FormLead.objects.filter(id__in=lead_IDs)
        users+=[lead.user for lead in leads if lead.user]

        student_IDs = request.POST.getlist('students', [])
        student_IDs = [int(student) for student in student_IDs]
        students = Student.objects.filter(id__in=student_IDs)
        users += [student.user for student in students]

        group_IDs = request.POST.getlist('groups',[])
        group_IDs = [int(group) for group in group_IDs]
        groups = Group.objects.filter(id__in=group_IDs)
        group_students = [group_student for group in groups for group_student in group.students.all()]
        students = set([group.student for group in group_students])
        leads = set([demo.lead for group in groups for demo in group.leaddemo_set.all() if demo.lead.activity!=3])
        users +=[student.user for student in students]
        users +=[lead.user for lead in leads]

        
        teacher_IDs = request.POST.getlist('teachers', [])
        teacher_IDs = [int(teacher) for teacher in teacher_IDs]
        teachers = Teacher.objects.filter(id__in=teacher_IDs)
        users += [teacher.user for teacher in teachers]

        parent_IDs = request.POST.getlist('parents', [])
        parent_IDs = [int(parent) for parent in parent_IDs]
        parents = Parents.objects.filter(id__in=parent_IDs)
        users += [parent.user for parent in parents]

        return JsonResponse({
            'sms_limit': sms_limit, 
            'message':message, 
            'status':status, 
            'users': len(users)
            })
    return JsonResponse({'message':'No data'})


def send_messages_result(email=None, password=None, text=None, request=None, users=[]):
    res = send_messages(email=email, password=password, text=text, request=request, users=users)
    if res == 404:
        status = "SMS Account tizimdan ro'yxatdan o'tmagan."
        code = 404
    elif res == 200:
        status = "SMS Xabar providerga yuborildi."
        code = 200
    elif res == 503:
        status = "Provider bilan muammo sodir bo'ldi."
        code = 503
    else:
        status = "Server Muammo"
        code = 500

    return status, code


@login_required
def send_sms_to_lead(request):
    sms_integration = sms.get_sms_integration()
    if request.method == 'POST' and sms_integration:
        lead_IDs = request.POST.getlist('leads')
        lead_IDs = [int(lead) for lead in lead_IDs]
        leads = get_list_or_404(FormLead, pk__in=lead_IDs)
        message = request.POST.get('message',None)
        users = [lead.user for lead in leads]
        message = request.POST.get('message', None)
        if message is None:
            return JsonResponse({'status':'Xabar kiritilishi majburiy'}, status=400)
        
        status, code = send_messages_result(email=None, password=None, text=message, request=request, users=users)
        return JsonResponse({'status': status}, status=code)
    return JsonResponse({'status':'bajarilmadi'}, status=400)


@login_required
def send_sms_to_group(request):
    if request.method == 'POST':
        group_IDs = request.POST.getlist('groups')
        group_IDs = [int(group) for group in group_IDs]
        groups = get_list_or_404(Group, pk__in=group_IDs)
        group_students = [group_student for group in groups for group_student in group.students.all()]
        students = set([group.student for group in group_students])
        leads = set([demo.lead for group in groups for demo in group.leaddemo_set.all() if demo.lead.activity!=3])
        message = request.POST.get('message', None)
        users = [student.user for student in students] + [lead.user for lead in leads]
        message = request.POST.get('message', None)
        if message is None:
            return JsonResponse({'status':'Xabar kiritilishi majburiy'}, status=400)
        
        status, code = send_messages_result(email=None, password=None, text=message, request=request, users=users)
        return JsonResponse({'status': status}, status=code)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)


@login_required
def send_sms_to_students(request):
    
    if request.method == 'POST':
        student_IDs = request.POST.getlist('students')
        student_IDs = [int(student) for student in student_IDs]
        students = get_list_or_404(Student, pk__in=student_IDs)
        message = request.POST.get('message', None)
        users = [student.user for student in students]
        message = request.POST.get('message', None)
        if message is None:
            return JsonResponse({'status':'Xabar kiritilishi majburiy'}, status=400)
        
        status, code = send_messages_result(email=None, password=None, text=message, request=request, users=users)
        return JsonResponse({'status': status}, status=code)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)






@login_required
def send_sms_to_teacher(request):
    if request.method == 'POST':
        teacher_IDs = request.POST.getlist('teachers')
        teacher_IDs = [int(teacher) for teacher in teacher_IDs]
        teachers = get_list_or_404(Teacher, pk__in=teacher_IDs)
        users = [teacher.user for teacher in teachers]
        message = request.POST.get('message', None)
        if message is None:
            return JsonResponse({'status':'Xabar kiritilishi majburiy'}, status=400)
        
        status, code = send_messages_result(email=None, password=None, text=message, request=request, users=users)
        return JsonResponse({'status': status}, status=code)

    return JsonResponse({'status':'Foydalanuvchi xatoligi'}, status=400)



@login_required
def send_sms_to_parent(request):
    if request.method == 'POST':
        message = request.POST.get('message', None)
        if message is None:
            return JsonResponse({'status':'Xabar kiritilishi majburiy'}, status=400)
        parent_IDs = request.POST.getlist('parents')
        parent_IDs = [int(parent) for parent in parent_IDs]
        parents = get_list_or_404(Parents, pk__in=parent_IDs)
        users = [ parent.user for parent in parents]
        status, code = send_messages_result(email=None, password=None, text=message, request=request, users=users)
        return JsonResponse({'status': status}, status=code)
    return JsonResponse({'status':'Foydalanuvchi xatoligi'}, status=400)


@login_required
def send_sms_to_course(request):
    
    if request.method == 'POST':
        course_IDs = request.POST.getlist('courses')
        course_IDs = [int(course) for course in course_IDs]
        courses = get_list_or_404(Course, pk__in=course_IDs)
        groups = [group for course in courses for group in course.groups.all()]
        group_students = [group_student for group in groups for group_student in group.students.all()]
        students = set([group.student for group in group_students])
        leads = set([demo.lead for group in groups for demo in group.leaddemo_set.all() if demo.lead.activity!=3])
        message = request.POST.get('message', None)
        users = [ student.user for student in students] + [lead.user for lead in leads]
        status, code = send_messages_result(email=None, password=None, text=message, request=request, users=users)
        return JsonResponse({'status': status}, status=code)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)