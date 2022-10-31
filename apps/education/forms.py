from django import forms
from django.forms.formsets import formset_factory
from admintion.models import Tasks
from student.models import Homeworks
from user.models import CustomUser

from education.models import Modules, Lessons, Contents, FAQ

class LessonAddForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ('id', 'module', 'title', 'comment')
        
    def save(self, author:CustomUser):
        self.instance = super().save(commit=False)
        self.instance.author = author
        self.instance.save()
        return self.instance

class ContentForm(forms.ModelForm):
    class Meta:
        model = Contents
        fields = ('title', 'video', 'video_link', 'text', 'homework', 'opened_at', 'closed_at', 
                'required', 'status')
class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ('question', 'answer', )

FAQFormSet = formset_factory(FAQForm, extra=0, max_num=100)


class TextContentForm(forms.ModelForm):
    class Meta:
        model = Contents
        fields=('id', 'title', 'text', 'required', 'status')

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Modules
        fields = ('id', 'title', 'comment', 'course')

class HomeworkActionForm(forms.ModelForm):
    class Meta:
        model = Homeworks
        fields = ('id', 'comment', 'ball', 'comment_file', )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['whom'].required=False
        self.fields['author'].required=False
        self.fields['comment'].required=False
        self.fields['status'].required = False