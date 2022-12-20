from rest_framework import serializers
# from account.models import *
from payme_app.models import Order


class OrderSerializers(serializers.ModelSerializer):
    # payme = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'course_id', 'amount', 'payme_link']
        # fields = ['id', 'amount', 'customer', 'payme_link']







