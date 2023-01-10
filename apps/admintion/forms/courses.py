from django import forms

from admintion.models import Course


class CourseForm(forms.ModelForm):
    """
        Fields: title(req), duration(req), lesson_duration(req), price(req), comment(req), status(opt.), educenter(opt.).
        req -> talab qilinadi. opt.-> kiritish majburiy emas.
        Hozircha faqat kursni yangilash uchun ishlatildi. 
    """
    class Meta:
        model = Course
        exclude = ('author', )