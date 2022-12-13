from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from admintion.services import send_sms, sms
from admintion.models import FormLead,Student,Messages,Group,Teacher,Parents,Course

@login_required
def check_sms_availability(request):
    sms_integration = sms.get_sms_integration() or sms.get_sms_integration(main=True)
    if request.method == 'POST' and sms_integration:
        sms_limit = sms.get_bonus_smses(sms_integration)
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

@login_required
def send_sms_to_lead(request):
    sms_integration = sms.get_sms_integration()
    if request.method == 'POST' and sms_integration:
        lead_IDs = request.POST.getlist('leads')
        lead_IDs = [int(lead) for lead in lead_IDs]
        leads = get_list_or_404(FormLead, pk__in=lead_IDs)
        message = request.POST.get('message',None)
        if leads and message:
            unsent = sent = []
            for lead in leads:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(lead.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(lead.user, message, request.user,message_type=10,commit=False))
                elif status == 503:
                    unsent.append(lead)
            if len(sent):
                Messages.objects.bulk_create(sent)
            return JsonResponse({'status':'completed', 'sent': len(sent), 'unsent':len(unsent)}, safe=False)
    return JsonResponse({'status':'bajarilmadi'}, status=400)


@login_required
def send_sms_to_group(request):
    sms_integration = sms.get_sms_integration()
    if request.method == 'POST' and sms_integration:
        group_IDs = request.POST.getlist('groups')
        group_IDs = [int(group) for group in group_IDs]
        groups = get_list_or_404(Group, pk__in=group_IDs)
        group_students = [group_student for group in groups for group_student in group.students.all()]
        students = set([group.student for group in group_students])
        leads = set([demo.lead for group in groups for demo in group.leaddemo_set.all() if demo.lead.activity!=3])
        message = request.POST.get('message', None)
        if (students or leads) and message:
            unsent = sent = []
            for student in students:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(student.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(student.user, message, request.user,message_type=8,commit=False))
                elif status == 503:
                    unsent.append(student)
            for lead in leads:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(lead.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(lead.user, message, request.user,message_type=8,commit=False))
                elif status == 503:
                    unsent.append(lead)
            
            if len(sent):
                Messages.objects.bulk_create(sent)
            return JsonResponse({'status':'completed', 'sent': len(sent), 'unsent': len(unsent)}, safe=False)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)


@login_required
def send_sms_to_students(request):
    sms_integration = sms.get_sms_integration()
    if request.method == 'POST' and sms_integration:
        student_IDs = request.POST.getlist('students')
        student_IDs = [int(student) for student in student_IDs]
        students = get_list_or_404(Student, pk__in=student_IDs)
        message = request.POST.get('message', None)
        if students and message:
            unsent = sent = []
            for student in students:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(student.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(student.user, message, request.user,message_type=7,commit=False))
                elif status == 503:
                    unsent.append(student)
            if len(sent):
                Messages.objects.bulk_create(sent)
            return JsonResponse({'status':'completed', 'sent': len(sent), 'unsent': len(unsent)}, safe=False)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)


@login_required
def send_sms_to_teacher(request):
    sms_integration = sms.get_sms_integration()
    if request.method == 'POST' and sms_integration:
        teacher_IDs = request.POST.getlist('teachers')
        teacher_IDs = [int(teacher) for teacher in teacher_IDs]
        teachers = get_list_or_404(Teacher, pk__in=teacher_IDs)
        message = request.POST.get('message', None)
        if teachers and message:
            unsent = sent = []
            for teacher in teachers:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(teacher.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(teacher.user, message, request.user,message_type=2,commit=False))
                elif status == 503:
                    unsent.append(teacher)
            if len(sent):
                Messages.objects.bulk_create(sent)
            return JsonResponse({'status':'completed', 'sent': len(sent), 'unsent': len(unsent)}, safe=False)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)


@login_required
def send_sms_to_parent(request):
    sms_integration = sms.get_sms_integration()
    if request.method == 'POST' and sms_integration:
        parent_IDs = request.POST.getlist('parents')
        parent_IDs = [int(parent) for parent in parent_IDs]
        parents = get_list_or_404(Parents, pk__in=parent_IDs)
        message = request.POST.get('message', None)
        if parents and message:
            unsent = sent = []
            for parent in parents:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(parent.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(parent.user, message, request.user,message_type=4,commit=False))
                elif status == 503:
                    unsent.append(parent)
            if len(sent):
                Messages.objects.bulk_create(sent)
            return JsonResponse({'status':'completed', 'sent': len(sent), 'unsent': len(unsent)}, safe=False)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)


@login_required
def send_sms_to_course(request):
    sms_integration = sms.get_sms_integration()
    if request.method == 'POST' and sms_integration:
        course_IDs = request.POST.getlist('courses')
        course_IDs = [int(course) for course in course_IDs]
        courses = get_list_or_404(Course, pk__in=course_IDs)
        groups = [group for course in courses for group in course.groups.all()]
        group_students = [group_student for group in groups for group_student in group.students.all()]
        students = set([group.student for group in group_students])
        leads = set([demo.lead for group in groups for demo in group.leaddemo_set.all() if demo.lead.activity!=3])
        message = request.POST.get('message', None)
        if (students or leads) and message:
            unsent = sent = []
            for student in students:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(student.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(student.user, message, request.user,message_type=8,commit=False))
                elif status == 503:
                    unsent.append(student)
            for lead in leads:
                email, password = sms.get_sms_credentials()
                status = send_sms.send_message(lead.user.phone, message, email, password)
                if status == 201:
                    sms.set_used_smses(used=1)
                    sent.append(sms.save_sms(lead.user, message, request.user,message_type=8,commit=False))
                elif status == 503:
                    unsent.append(lead)
            
            if len(sent):
                Messages.objects.bulk_create(sent)
            return JsonResponse({'status':'completed', 'sent': len(sent), 'unsent': len(unsent)}, safe=False)
    return JsonResponse({'status':'Bajarilmadi'}, status=400)