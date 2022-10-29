from django import forms

from admintion.models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('id', 'task_type', 'responsibles', 'deadline', 'comment', 'whom', 'user_status', 
                  'groups', 'leads', 'students', 'courses', 'parents')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['whom'].required=False
        self.fields['groups'].required=False
        self.fields['leads'].required=False 
        self.fields['students'].required=False
        self.fields['courses'].required=False 
        self.fields['parents'].required=False
        self.fields['comment'].required=False