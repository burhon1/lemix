from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.forms import model_to_dict
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from admintion.models import Course,EduCenters,Group,Teacher,Room,Student
from admintion.forms.courses import CourseForm
from admintion.data.chooses import COURCE_DURATION_TYPES,LESSON_DURATION_TYPES,PRICE_TYPES, GROUPS_DAYS,GROUPS_STATUS
from education.selectors import get_courses_data
from django.contrib import messages
from user.utils import get_admins
from admintion.utils import get_list_of_dict,get_list_of_filter


# @permission_required(['admintion.view_course'], raise_exception=True)
def courses_view(request):
    context = {}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    if request.method == "POST":
        # if(request.user.has_perm('admintion.add_courses') is False):
        #     raise PermissionDenied
        if educenter.count() == 1:
            post = request.POST
            title = post.get('title',False)
            duration = post.get('duration',False)
            lesson_duration = post.get('lesson_duration',False)
            price = post.get('price',False)
            comment = post.get('comment',False)
            course_duration_type = post.get('course_duration_type',False)
            lesson_duration_type = post.get('lesson_duration_type',False)
            price_type = post.get('price_type',False)
            if title and lesson_duration and duration and price:
                course = Course(
                    title=title,
                    duration=duration,
                    lesson_duration=lesson_duration,
                    price=price,
                    duration_type=course_duration_type,
                    lesson_duration_type=lesson_duration_type,
                    price_type=price_type,
                    educenter=educenter.first()
                )
                if comment:
                    course.comment=comment
                course.save()
                return redirect(reverse('admintion:courses')+f"?success={True}")
            else:
                return redirect(reverse('admintion:courses')+f"?error=Ma'lumotlar to'liq kiritilmadi")    
        return redirect(reverse('admintion:courses')+f"?error=Filyalni tanlang")          
    educenter_ids=educenter.values_list('id',flat=True)
    context['course_duration_types'] =[{'id':i[0],'title':i[1]} for i in COURCE_DURATION_TYPES]
    context['lesson_duration_types'] =[{'id':i[0],'title':i[1]} for i in LESSON_DURATION_TYPES]
    context['price_types'] =[{'id':i[0],'title':i[1]} for i in PRICE_TYPES]
    context['objs'] = Course.courses.courses(educenter_ids)
    context['keys'] = ['check','title','duration','price','group_count','student_count','status','action']
    return render(request,'admintion/courses_list.html',context) 


def courses_by_filter_view(request):
    context={}
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter_ids = EduCenters.objects.filter(qury).values_list('id',flat=True)   

    status = request.GET
    filter_keys=get_list_of_filter(status)

    courses = list(Course.courses.course_filter(filter_keys,educenter_ids))
    return JsonResponse({'data':courses,'status':200})

@permission_required('admintion.delete_course')
def course_delete_view(request, pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return redirect(reverse('admintion:courses')+f"?success={True}")
    else:
        return redirect(reverse('admintion:courses')+f"?error=Xatolik sodir bo'ldi.") 


@permission_required('admintion.view_course')
def course_detail_view(request, pk):
    context = dict()
    ed_id=request.session.get('branch_id',False)
    qury = Q(id=ed_id)
    if int(ed_id) == 0:
        qury=(Q(id=request.user.educenter) | Q(parent__id=request.user.educenter))
    educenter = EduCenters.objects.filter(qury)
    
    if request.method == "POST":
        post = request.POST
        title = post.get('title',False)
        duration = post.get('duration',False)
        lesson_duration = post.get('lesson_duration',False)
        price = post.get('price',False)
        comment = post.get('comment',False)
        course_duration_type = post.get('course_duration_type',False)
        lesson_duration_type = post.get('lesson_duration_type',False)
        price_type = post.get('price_type',False)

        course = Course.objects.get(id=pk)
        if title and lesson_duration and duration and price:
            course.title=title
            course.duration=duration
            course.lesson_duration=lesson_duration
            course.price=price
            course.duration_type=course_duration_type
            course.lesson_duration_type=lesson_duration_type
            course.price_type=price_type

            if comment:
                course.comment=comment
            course.save()
            return redirect(request.path)
        messages.error(request, f"Ma'lumotlarni to'ldiring") 
    # context['course'] = get_courses_data([course], teacher=request.user.teacher_set.first())[0]
    educenter_ids = educenter.values_list('id',flat=True)             
    teacher = Teacher.teachers.teacher_all(educenter_ids) 
    context['course'] = Course.courses.course(pk)
    context['teachers'] = teacher.main_teacher()
    context['trainers'] = teacher.trainer_list() 
    context['rooms'] = Room.rooms.rooms(educenter_ids)
    context['groups'] = Group.groups.groups_by_course(educenter_ids,pk)
    context['days'] = [{'id':i[0],'title':i[1]} for i in GROUPS_DAYS]
    context['group_status'] = [{'id':i[0],'title':i[1]} for i in GROUPS_STATUS] 
    context['course_id']=pk
    from django.db.models.functions import JSONObject
    from django.db.models import OuterRef
    course_list = Course.objects.filter(group__teacher__id=OuterRef("pk")).distinct().values(json=JSONObject(title="title", id="id"))
    context['teachers_list']=Teacher.teachers.teachers_by_course(educenter_ids,pk,course_list)
    context['student_list']=Student.students.students_by_course(educenter_ids,pk)
    print(context['teachers_list'])
    return render(request,'admintion/course_detail.html', context) 



def course_update_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('admintion:courses')+f"?success={True}")
    else:
        return redirect(reverse('admintion:courses')+f"?error=Ma'lumotlar to'liq kiritilmadi.") 

def get_course_list_view(request):
    if request.method=='POST':
        educenter = request.POST.get('educenters')
        courses = Course.objects.filter(educenter__id=int(educenter)).values('id','title')
        return JsonResponse({'objs':list(courses)})
    return JsonResponse({}, status=200)


def get_course_edit_view(request,pk):
    course = Course.objects.filter(id=pk)
    if course.exists():
        course=course.values('id','title','duration','duration_type','lesson_duration','lesson_duration_type','price','price_type','comment').first()
        return JsonResponse({'obj':course,'status':203})
    return JsonResponse({'message':'Kurs topilmadi','status':404})