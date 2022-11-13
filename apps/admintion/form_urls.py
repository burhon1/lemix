from django.urls import path

from admintion.views.forms import lead_registration_view


urlpatterns = [
    path('<int:pk>/', lead_registration_view, name='lead_registration_view'),
]