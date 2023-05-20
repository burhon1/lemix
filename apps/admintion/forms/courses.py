from django import forms

from admintion.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('author','educenter' )