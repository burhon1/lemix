from django.urls import path

from education.views import *

app_name = 'education'

urlpatterns = [
    path('test/',test2_view,name='test'),
    path('groups/list/',groups_list_view,name='test')
]
