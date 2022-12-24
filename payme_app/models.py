from django.db import models
from payme.methods.generate_link import GeneratePayLink
from django.db.models.signals import pre_save
from django.dispatch import receiver
# from account.models import Account


class MerchatTransactionsModel(models.Model):
    _id = models.CharField(max_length=255, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=False)
    order_id = models.BigIntegerField(null=True, blank=True)
    amount = models.BigIntegerField(null=True, blank=True)
    time = models.BigIntegerField(null=True, blank=True)
    perform_time = models.BigIntegerField(null=True, default=0)
    cancel_time = models.BigIntegerField(null=True, default=0)
    state = models.BigIntegerField(null=True, default=1)
    reason = models.CharField(max_length=255, null=True, blank=True)
    created_at_ms = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self._id)


class Order(models.Model):
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # customer = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)

    customer_id = models.IntegerField()
    course_id = models.IntegerField()
    status = models.BooleanField(default=True)
    pay_link = models.URLField(blank=True, null=True)
    # pay_link = self.payme_link

    def __str__(self):
        return str(self.id)

    @property
    def payme_link(self):
        order_id = self.id
        order_amount = self.amount
        link = GeneratePayLink(order_id=order_id, amount=order_amount).generate_link()
        return link


# @receiver(pre_save, sender=Order)
# def amount_change(sender, instance=None, created=False, **kwargs):
#     instance.amount = instance.amount * 100
