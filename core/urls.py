from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='user/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('education/', include('education.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)