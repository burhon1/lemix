from django.urls import path,include
from manages.views import educenters

urlpatterns = [
    path('',educenters.educenters_view),
]
