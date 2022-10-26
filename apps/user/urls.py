from django.urls import path

from .views import sign_in,sign_out,account, user
app_name = 'user'

urlpatterns = [
    path('login/',sign_in.login_view,name='login'),
    path('logout/', sign_out.logout_view, name="logout" ),
    path('account/', account.account_view, name="account" ),
    path('create/', user.user_create_view, name='user_create'),
    path('<int:pk>/update/', user.user_update_view, name='user_update'),
]
