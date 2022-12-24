from django.urls import path
from .views import sms_journal_view, get_callback_view, sms_message_users

app_name = 'sms'

urlpatterns = [
    path('journal/', sms_journal_view, name='sms-journal'),
    path('<int:pk>/messages/', sms_message_users, name='sms-users'),
    path('get-callback/', get_callback_view, name='get-callback'),
]