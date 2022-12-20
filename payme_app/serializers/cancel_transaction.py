from rest_framework import serializers


class CancelTransactionSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=24)
    reason_id = serializers.CharField(max_length=3, required=False)
