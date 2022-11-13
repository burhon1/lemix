from django import forms
from django.forms.formsets import formset_factory
from admintion.models import FormLead, LeadDemo,LeadForms,FormFields,Contacts,Sources
from user.models import CustomUser

class LeadForm(forms.ModelForm):
    class Meta:
        model = FormLead
        fields = "__all__"

        optional = ('source', 'status', 'comment', 'telegram', 'parents', 'p_phone',
                    'passport', 'file',  'course', 'author', 'activity', 'purpose', 'modified_at'
                    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.optional:
            self.fields[field].required = False
        # self.fields['user'].required = False


class DemoForm(forms.ModelForm):
    class Meta:
        model = LeadDemo
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['date'].required = False

DemoFormset = formset_factory(DemoForm, extra=0)

class LeadFormClass(forms.ModelForm):
    class Meta:
        model = LeadForms
        exclude = ('link','seen','qrcode',)

    def clean(self):
        title = self.cleaned_data.get('title')
        titles = [ obj['title'] for obj in list(self._meta.model.objects.values('title'))]
        name = self.cleaned_data.get('name', None)
        if self.instance is None:
            if title in titles:
                i = 1
                while f"{title} {i}" in titles: 
                    i += 1
                title = f"{title} {i}"
            names = [ obj['name'] for obj in list(self._meta.model.objects.values('name'))]
            if name in names:
                i = 1
                while f"{name} {i}" in names: 
                    i += 1
                name = f"{name} {i}"
            if name is None:
                name = title
        self.cleaned_data['title'] = title
        self.cleaned_data['name'] = name
        

        
        print(self.cleaned_data)
        return self.cleaned_data


class FieldsFormClass(forms.ModelForm):
    class Meta:
        model = FormFields
        exclude = ('order',)

FieldsFormSet = formset_factory(FieldsFormClass, extra=0)

class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = "__all__"

    def clean(self):
        print(self.cleaned_data)
        return self.cleaned_data

ContactsFormSet = formset_factory(ContactsForm, extra=0) 


class LeadFormRegisterForm(forms.Form):
    educenters = forms.ModelChoiceField(queryset=None,label="", required=True, widget=forms.Select(attrs={'id':'select-size-4','placeholder':"Filialni tanlang", 'class':'form-control  form-control-default mb-3', 'aria-describedby':'select-size-4'}))
    courses = forms.ModelChoiceField(queryset=None,label="", widget=forms.Select(attrs={'id':'select-size-5','placeholder':"Kursni tanlang", 'class':'form-control  form-control-default mb-3', 'aria-describedby':'select-size-5',}))
    sources = forms.ModelChoiceField(queryset=None,label="", widget=forms.Select(attrs={'id':'select-size-6','placeholder':"Bizni qanday topdingiz?", 'class':'form-control  form-control-default mb-3', 'aria-describedby':'select-size-6'}))
    phone_number = forms.CharField(max_length=9, label="", widget=forms.TextInput(
        attrs={'name':'phone_number', 'id':'id_phone_number', 'class':"form-control mb-3", 'placeholder':"Telefon raqam(xuddi: 998887766)",}
    ))
    telegram = forms.CharField(max_length=15, label="", widget=forms.TextInput(attrs={'class':'form-control  form-control-default mb-3','placeholder':'Telegram raqami'}))

    def __init__(self, form:LeadForms, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['educenters'].queryset = form.educenters.all() 
        self.fields['courses'].queryset = form.courses.all()
        self.fields['sources'].queryset = form.sources.all()
        
        fields = form.formfields_set.all().order_by('order')
        for field in fields:
            if field.title not in self.fields.keys() and field.title not in ('Telefon raqami', 'Telegram', 'Manbasi'):
                if field.title.lower().find('rasm')>=0 or field.title.lower().find('fayl')>=0 or field.title.lower().find('file')>=0:
                    self.fields[field.title] = forms.FileField(required=field.required, widget=forms.FileInput(attrs={'class':"form-control mb-3",'placeholder': field.title}))
                else:
                    self.fields[field.title] = forms.CharField(max_length=150, required=field.required)
                    self.fields[field.title].widget = forms.TextInput(attrs={'class':"form-control mb-3",'placeholder': field.title})
                self.fields[field.title].label = ""
    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone=phone_number).exists():
            raise forms.ValidationError("Bu telefon raqam ro'yxatdan o'tgan.")
        self.cleaned_data['user'] = {
            'phone':phone_number,
        }
        if 'Ismi' in self.fields.keys():
            self.cleaned_data['user'].update({'first_name':self.cleaned_data.get('Ismi')})
        if 'Familiya' in self.fields.keys():
            self.cleaned_data['user'].update({'last_name':self.cleaned_data.get('Familiya')})
        if 'Otasining ismi' in self.fields.keys():
            self.cleaned_data['user'].update({'middle_name':self.cleaned_data.get('Otasining ismi')})
        if 'Tug\'ilgan kuni' in self.fields.keys():
            self.cleaned_data['user'].update({'birthday':self.cleaned_data.get('Tug\'ilgan kuni')})
        if 'Manzil' in self.fields.keys():
            self.cleaned_data['user'].update({'location':self.cleaned_data.get('Manzil')})
        telegram = self.cleaned_data.get('telegram')
        self.cleaned_data.update({'lead':{'telegram': telegram} })
        self.cleaned_data['lead'].update({'source': self.cleaned_data['sources'].id|1})
        self.cleaned_data['lead'].update({'comment':''})
        for field, value in self.cleaned_data.items():
            if field not in ['user', 'lead', 'phone_number', 'telegram', 'first_name', 'last_name', 'middle_name', 'birthday', 'sources']:
                self.cleaned_data['lead']['comment'] += f'{field}: {value}\n'
        # print("Data: ", self.cleaned_data)
        return self.cleaned_data

    def save(self, *args,**kwargs):
        print(self.cleaned_data['lead'])
        try:
            user = CustomUser(**self.cleaned_data.get('user'), is_active=True)
            user.set_password(user.phone)
            user.save()
            lead = FormLead.objects.create(**self.cleaned_data.get('lead'), user=user)
        except Exception as e:
            CustomUser.objects.filter(phone=self.cleaned_data.get('user')['phone']).delete()
            raise e
        
        return lead
