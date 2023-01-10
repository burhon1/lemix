from django.urls import path, include
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('v1.0/', include('apis.v1_0')),
]