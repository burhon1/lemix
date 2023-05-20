from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from admintion.models import Teacher, EduCenters
from admintion.services.teacher import update_teacher
from user.services.users import user_add
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse


def teachers_view(request):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method == "POST":
        if educenter.count() == 1:
            post = request.POST
            groups = Group.objects.filter(name="Teacher")
            status,obj = user_add(groups,request, True).values()
            teacer_type=post.get('teacer_type',False)
            if status==200 and teacer_type:
                teacher = Teacher(
                    teacer_type=teacer_type,
                    user=obj,
                    educenter=educenter.first()
                )
                teacher.save()
                return redirect('admintion:teachers')
            else:
                context['error'] = 'Malumotlar to\'liq kiritilmadi'  
                return redirect(reverse('admintion:teachers')+f"?error={context['error']}")
        return redirect(reverse('admintion:teachers')+f"?error=Filyalni tanlang")         
    educenter_ids = educenter.values_list('id',flat=True)              
    teacher = Teacher.teachers.teachers(educenter_ids) 
    context['objs'] = teacher
    context['educenters'] = EduCenters.objects.filter(id=ed_id).values('id','name')|EduCenters.objects.filter(parent__id=ed_id).values('id','name')
    return render(request,'admintion/teachers.html',context) 


def teacher_update_view(request, id):
    obj = get_object_or_404(Teacher, pk=id)
    if request.method == 'POST':
        
        post = request.POST
        update_teacher(obj, post)
        return JsonResponse({'obj':Teacher.teachers.teacher(id)}, status=200)
    return JsonResponse({
        'obj':Teacher.teachers.teacher(id), 
        'method':'get', 'message':'Method cannot be get. It must be a post.'})

def teacher_detail_view(request,id):
    context = {'obj':Teacher.teachers.teacher(id)}
    return render(request,'admintion/teacher_detail.html',context) 

@permission_required('admintion.delete_teacher')
def teacher_delete_view(request, id):
    teacher = get_object_or_404(Teacher, pk=id)
    if request.method == 'POST':
        user = teacher.user
        user.delete()
        status = 204
    else:
        status = 200
    return JsonResponse({}, status=status)

def get_teacher_edit_view(request,id):
    from django.db.models import Value, Count, When,Case,F,Q,Manager,Func,Subquery,CharField,TextField,Exists,OuterRef
    from django.contrib.postgres.aggregates import ArrayAgg
    # from django.contrib.postgres.functions import ToArray
    from django.db.models.functions import Concat,Substr,Cast
    teacher = Teacher.objects.filter(id=id)
    if teacher.exists():
        teacher=teacher.annotate(
            full_name=Concat(F('user__first_name'),Value(' '),F('user__last_name')),
            phone_number=Concat(
                Value('+998'),
                Value(' ('),
                Substr(F('user__phone'),1,2),
                Value(') '),
                Substr(F('user__phone'),3,3),
                Value(' '),
                Substr(F('user__phone'),6,2),
                Value(' '),
                Substr(F('user__phone'),8,2)
                )).values('id','full_name','phone_number','user__location','teacer_type','user__gender','user__birthday').first()
        return JsonResponse({'obj':teacher,'status':203})
    return JsonResponse({'message':'O\'qituvchi topilmadi','status':404})