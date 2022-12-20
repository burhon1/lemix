from rest_framework import serializers


class CheckTransactionSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=24)
