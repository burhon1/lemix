from django import forms
from django.forms.formsets import formset_factory
from admintion.models import FormLead, LeadDemo


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