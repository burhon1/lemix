from django.urls import path, include




urlpatterns = [
    path('v1.0/', include('apis.v1_0')),
]