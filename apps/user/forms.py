from django import forms

from user.models import CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def clean(self):
        phone = self.cleaned_data.get('phone')
        if self.instance is None:
            
            if CustomUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Bu raqamdan foydalanilgan.", code=400)
        if not self.cleaned_data.get('password', None) and self.instance is None:
            
            setattr(self.cleaned_data, 'password', phone)
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = False
        self.fields['password'].required = False

    def save(self):
        instance = super().save(commit=False)
        instance.is_active = True
        instance.set_password(self.cleaned_data['password'])
        instance.save()
        return instance