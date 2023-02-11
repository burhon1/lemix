from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.forms import model_to_dict
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from admintion.models import Course,EduCenters
from admintion.forms.courses import CourseForm
from admintion.data.chooses import COURCE_DURATION_TYPES,LESSON_DURATION_TYPES,PRICE_TYPES
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
            if title and lesson_duration and duration and price and comment:
                course = Course(
                    title=title,
                    duration=duration,
                    lesson_duration=lesson_duration,
                    price=price,
                    comment=comment,
                    duration_type=course_duration_type,
                    lesson_duration_type=lesson_duration_type,
                    price_type=price_type,
                    educenter=educenter.first()
                )
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
    course = get_object_or_404(Course, pk=pk)
    return JsonResponse(
        model_to_dict(course, exclude=('author'))
        )


@permission_required('admintion.change_course')
def course_update_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('admintion:courses')+f"?success={True}")
    else:
        return redirect(reverse('admintion:courses')+f"?error=Ma'lumotlar to'liq kiritilmadi.") 
