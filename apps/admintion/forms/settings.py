from django import forms
from admintion.models import EduCenters

class EduCentersForm(forms.ModelForm):
    class Meta:
        model = EduCenters
        fields = ('logo', 'oferta', 's_contract', 'j_contract', 't_contract')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = False
