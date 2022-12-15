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


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(max_length=150)
    password1 = forms.CharField(max_length=150)
    password2 = forms.CharField(max_length=150)

    class Meta:
        model = CustomUser
        fields = ('password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].required = False

    def clean(self):
        old_password = self.cleaned_data.pop('old_password')
        if self.instance.check_password(old_password) is False:
            raise forms.ValidationError("Eski parol mos emas.")

        password1, password2 = self.cleaned_data.pop('password1'), self.cleaned_data.pop('password2')
        if password1 != password2:
            raise forms.ValidationError("Parol va qayta kiritilgan parol o'zaro mos emas.")
        self.cleaned_data['password'] = password1
        return self.cleaned_data

    def save(self):
        self.instance = super().save(commit=False)
        self.instance.set_password(self.cleaned_data['password'])
        self.instance.save(update_fields=['password'])

        return self.instance