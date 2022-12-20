from django.urls import path
from payme_app.views import MerchantAPIView
from payme_app.views import create_order

urlpatterns = [
    path('merchant', MerchantAPIView.as_view()),
    path('create_order', create_order, name='order'),

]
