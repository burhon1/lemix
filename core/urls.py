from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='user/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('admintion/', include('admintion.urls')),
    path('education/', include('education.urls')),
    path('student/', include('student.urls')),
    path('finance/', include('finance.urls')),
    path('register/',include('admintion.form_urls')),
    path('sms/', include('sms.urls')),
    path('pyclick/', include('pyclick.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
