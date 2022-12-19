from rest_framework import serializers
from finance.models import ClickOrder

class ClickOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickOrder
        fields = ["amount", "is_paid"]