from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.forms import model_to_dict
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from admintion.models import Course
from admintion.forms.courses import CourseForm
from user.utils import get_admins


@permission_required(['admintion.view_course'], raise_exception=True)
def courses_view(request):
    """
        foydalanuvchida kurslarni ko'rishga permission bo'lishi kerak.
        method lari: `get`, `post`. 
        `GET` so'rov natijasi: {'objs': Courses Queryset,}
        `POST`: 
            - foydalanuvchida kurs qo'shishga permission bo'lishi kerak.
            - Kiritilishi kerak SOHALAR: 
                    `title`, `duration`, `lesson_duration`, `price`, `comment`, `status`.
                    bunda `status` -> optional field. DEFAULT: `False`
            - course obyekt yaratadi, yoki xatolik qaytaradi.
            - Natijada {% url 'admintion:courses' %} urlga qaytaradi.
    """
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
    context['objs'] = Course.objects.all()
    return render(request,'admintion/courses_list.html',context) 

@permission_required('admintion.delete_course')
def course_delete_view(request, pk):
    """
        - o'chirish uchun permission talab qilinadi. 
        - Kursni, unga bog'langan guruh, onlayn dars materiallarini o'chiradi.
        - Methodlari: `POST`.
        - Kurs topilmasa, 404 xatolik qaytaradi.
        - Natija: {% url 'admintion:courses' %} urlga qaytaradi. 
    """
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return redirect(reverse('admintion:courses')+f"?success={True}")
    else:
        return redirect(reverse('admintion:courses')+f"?error=Xatolik sodir bo'ldi.") 


@permission_required('admintion.view_course')
def course_detail_view(request, pk):
    """
        - kursni ko'rish uchun permission talab qilinadi.
        - Course obyektini olib beradi (JSON ko'rinishda). 
        - Methodlari: `GET`.
        - Kurs topilmasa, 404 xatolik qaytaradi.
    """
    course = get_object_or_404(Course, pk=pk)
    return JsonResponse(
        model_to_dict(course, exclude=('author'))
        )


@permission_required('admintion.change_course')
def course_update_view(request, pk):
    """
        - kurs ma'lumotlarini yangilash uchun permission talab qilinadi.
        - Course obyekti bazada mavjud bo'lmasa, 404 xatolik qaytaradi. 
        - Methodlari: `GET`, `POST`.
            bunda `GET`:faqat formani olish uchun.
        - Kurs topilmasa, 404 xatolik qaytaradi.
    """
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST, instance=course)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(reverse('admintion:courses')+f"?success={True}")
    else:
        return redirect(reverse('admintion:courses')+f"?error=Ma'lumotlar to'liq kiritilmadi.") 
