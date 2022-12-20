from rest_framework import serializers


class PerformTransactionSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=24)
