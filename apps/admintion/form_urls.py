from django.urls import path

from admintion.views.forms import lead_registration_view,lead_registration2_view


urlpatterns = [
    path('<int:pk>/', lead_registration2_view, name='lead_registration_view'),
    path('<int:pk>/test/', lead_registration2_view, name='lead_registration2_view'),
]