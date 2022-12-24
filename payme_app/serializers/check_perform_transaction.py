from rest_framework import serializers


class CheckPerformTransactionSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True)
    order_id = serializers.IntegerField(allow_null=True)
