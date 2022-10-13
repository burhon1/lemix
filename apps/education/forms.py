from django import forms
from user.models import CustomUser

from education.models import Lessons

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
