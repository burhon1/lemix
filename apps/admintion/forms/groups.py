from django import forms

from admintion.models import Group, Teacher, Course, Room


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['teacher'].queryset = Teacher.objects.filter(teacer_type=True)
        self.fields['trainer'].queryset = Teacher.objects.filter(teacer_type=False)
        self.fields['course'].queryset = Course.objects.filter(status=True)
        self.fields['room'].queryset = Room.objects.filter(status=True)
