from django.shortcuts import get_object_or_404
from user.models import CustomUser
from admintion.models import FormLead
from education.models import Contents


def set_lead_content_viewed_status(content:Contents, lead: FormLead):
    content.leads.add(lead)
    content.save()
    return content