from rest_framework import serializers

from payme_app.models import MerchatTransactionsModel


class MerchatTransactionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model: MerchatTransactionsModel = MerchatTransactionsModel
        fields: list = [
            "_id",
            "time",
            "amount",
            "order_id",
        ]

    def validate_amount(self, data):
        """Validator for Transactions Amount"""
        if data["amount"]:
            pass
