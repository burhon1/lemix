from django import forms

from student.models import Homeworks


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homeworks
        fields = ('id', 'text', 'file')