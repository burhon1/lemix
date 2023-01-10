from django import forms
from user.utils import add_or_get_user, add_to_group
from admintion.models import EduCenters, Countries, Regions, Districts, EduFormats


class EducentersForm(forms.ModelForm):
    """
        - O'quv markaz filialini yaratish/tahrirlash uchun FormClass.
        - Bunda `full_name` va `phone` -> majburiy. Ular asnosida foydalanuvchi (director sifatida)
        yaratiladi, agar mavjud bo'lsa, unga directorlar uchun bo'lganidek permissionlar beriladi -> save() methodda.
        - O'quv markazi lokatsiyasini olish uchun davlatlar, viloyatlar, tumanlar birliklari nomlanishlaridan 
        foydalaniladi. -> __init__() methodda.
        - Telefon raqam sonlardan iborat bo'lishi kerak(`+` mumkin emas.):
            998XXYYYZZZZ yoki XXYYYZZZZ.
    """
    full_name = forms.CharField(label='Filial rahbari FIO', max_length=120, required=False)
    phone = forms.CharField(label='Telefon raqam', max_length=13, required=True)
    class Meta:
        model = EduCenters
        fields = ('name', 'director', 'country', 'district', 'region', 'address', 'max_groups', 'max_students',
                  'teacher_can_see_payments', 'teacher_can_sign_contracts', 'parent', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['country'].queryset = Countries.objects.all()
        self.fields['region'].queryset = Regions.objects.all()
        self.fields['district'].queryset = Districts.objects.all()
        self.fields['parent'].queryset = self._meta.model.objects.filter(parent=None)
        if self.instance:
            self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(id=self.instance.id)

    def clean(self):
        attrs = super().clean()
        if 'phone' in attrs.keys():
            phone = attrs.get('phone')
            if phone.isnumeric() == False:
                raise forms.ValidationError("Telefon raqam noto'g'ri kiritilgan.")
        return attrs

    def save(self):
        director = add_or_get_user(
            phone=self.cleaned_data.pop('phone')
        )
        if director and self.cleaned_data['full_name']:
            director.last_name, director.first_name = self.cleaned_data.pop('full_name').split()
            director = add_to_group(director, 'Direktor', False)
            director.save(update_fields=['first_name', 'last_name'])
        self.cleaned_data['director'] = director
        self.instance = super(EducentersForm, self).save(commit=False)
        if self.instance.director is None:
            self.instance.director = director

        self.instance.save()
        return self.instance 