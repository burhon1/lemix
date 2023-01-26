from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.forms import model_to_dict
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from admintion.models import Course,EduCenters
from admintion.forms.courses import CourseForm
from user.utils import get_admins


# @permission_required(['admintion.view_course'], raise_exception=True)
def courses_view(request):
    context = {}
    if request.method == "POST":
        if(request.user.has_perm('admintion.add_courses') is False):
            raise PermissionDenied
        post = request.POST
        title = post.get('title',False)
        duration = post.get('duration',False)
        lesson_duration = post.get('lesson_duration',False)
        price = post.get('price',False)
        comment = post.get('comment',False)
        status = post.get('status',False)
        if title and lesson_duration and duration and price and comment :
            course = Course(
                title=title,
                duration=duration,
                lesson_duration=lesson_duration,
                price=price,
                comment=comment,
                status=status
            )
            course.save()
            return redirect(reverse('admintion:courses')+f"?success={True}")
        else:
            return redirect(reverse('admintion:courses')+f"?error=Ma'lumotlar to'liq kiritilmadi")    
    ed_id=request.user.educenter
    educenter_ids = EduCenters.objects.filter(id=ed_id).values_list('id',flat=True)|EduCenters.objects.filter(parent__id=ed_id).values_list('id',flat=True)   
    context['objs'] = Course.courses.courses(educenter_ids)
    return render(request,'admintion/courses_list.html',context) 

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
