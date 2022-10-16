from django import forms
from django.forms.formsets import formset_factory
from user.models import CustomUser

from education.models import Lessons, Contents, FAQ

class LessonAddForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ('id', 'module', 'title', 'comment')
        
    def save(self, author:CustomUser):
        self.instance = super().save(commit=False)
        self.instance.author = author
        self.instance.save()
        print(self.instance, "in form")
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
