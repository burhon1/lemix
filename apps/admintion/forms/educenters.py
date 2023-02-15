from django import forms
from user.utils import add_or_get_user, add_to_group
from admintion.models import EduCenters, Countries, Regions, Districts, EduFormats


class EducentersForm(forms.ModelForm):
    full_name = forms.CharField(label='Filial rahbari FIO', max_length=120, required=False)
    phone = forms.CharField(label='Telefon raqam', max_length=13, required=True)
    class Meta:
        model = EduCenters
        fields = ('name', 'director', 'country', 'district', 'region', 'address', 'max_groups', 'max_students',
                  'teacher_can_see_payments', 'teacher_can_sign_contracts',  )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Countries.objects.all()
        self.fields['region'].queryset = Regions.objects.all()
        self.fields['district'].queryset = Districts.objects.all()
        
    def clean(self):
        attrs = super().clean()
        if 'phone' in attrs.keys():
            phone = attrs.get('phone')
            if phone.isnumeric() == False:
                raise forms.ValidationError("Telefon raqam noto'g'ri kiritilgan.")
        return attrs

    def save(self,educenter):
        phone_number=self.cleaned_data.pop('phone')
        director = add_or_get_user(
            phone=phone_number
        )
        if director and self.cleaned_data['full_name']:
            director.last_name = self.cleaned_data.pop('full_name')
            director = add_to_group(director, 'Director', False)
            director.save(update_fields=['first_name', 'last_name'])
        self.cleaned_data['director'] = director
        self.instance = super(EducentersForm, self).save(commit=False)
        if self.instance.director is None:
            self.instance.director = director
        self.instance.parent = self._meta.model.objects.filter(id=educenter).first()
        self.instance.phone_number = phone_number
        self.instance.save()
        return self.instance 