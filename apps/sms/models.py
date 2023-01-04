from django.db import models
from django.conf import settings

from sms.querysets import messages

class SMSAccount(models.Model):
    email = models.EmailField("SMS Email", max_length=350)
    password = models.CharField("SMS Password", max_length=350)
    sent_sms = models.IntegerField("Yuborilgan smslar soni", default=0)
    sent_sms_soums = models.PositiveIntegerField("Sarflangan mablag'", default=0)
    free_sms = models.IntegerField("Yuborilgan smslar soni", default=100)

    class Meta:
        verbose_name = 'SMS Account'
        verbose_name_plural = 'SMS Account'
        unique_together = ('email', 'password')
    
    def __str__(self):
        return self.email
    
    def has_bonus_sms(self):
        return self.free_sms > 0

    @property
    def credentials(self):
        if self.has_bonus_sms():
            return settings.ESKIZ_EMAIL.values()
        return self.email, self.password

    def set_sent_sms(self, sms_count: int, sms_soums: int):
        update_fields = []
        self.sent_sms += sms_count
        if self.free_sms:
            self.free_sms -= sms_count
            self.save(update_fields=['sent_sms', 'free_sms'])
        else:
            self.sent_sms_soums += sms_soums
            self.save(update_fields=['sent_sms', 'sent_sms_soums'])


class SMSMessage(models.Model):
    message    = models.CharField("Xabar matni", max_length=160)
    who_sent   = models.ForeignKey('user.CustomUser', models.SET_NULL, null=True)
    soums      = models.IntegerField("Sarflangan xarajat", null=True)
    timedelta  = models.FloatField("Sarflangan vaqt", null=True)
    created_at = models.DateTimeField("Xabar yaratildi", auto_now_add=True)
    sms_count  = models.PositiveIntegerField("Xabarlar soni", default=0)
    dispatch_id = models.IntegerField("Dispatch ID", null=True, blank=True)
    type       = models.CharField("Xabar turi", max_length=70, null=True)
    
    phone_number = models.CharField("Telefon raqam", max_length=12, null=True, blank=True)
    country      = models.CharField("Davlati", max_length=10, null=True)
    status       = models.CharField("Xabar statusi", max_length=20, null=True)

    objects = models.Manager()
    messages = messages.SMSMessageManager()

    class Meta:
        verbose_name = "SMS Message"
        verbose_name_plural = "SMS Messages"
        ordering = ('-created_at',)

    def __str__(self):
        return self.message

    def has_dispatch(self):
        if self.dispatch_id:
            return True
        return False

    def update(self, fields:dict):
        """
            Fields must be `dict`.
        """
        update_fields = []
        for field, value in fields.items():
            if field == 'soums':
                self.set_price(value)
                update_fields.append(field)
            elif hasattr(self, field):
                setattr(self, field, value)
                update_fields.append(field)
        self.save(update_fields=update_fields)

    def set_price(self, price: int)->int:
        """
            Returns difference of changed price and old one.
            It may need to calculate Account sent sms soums.
        """
        
        if self.soums == price or price == 0:
            return 0
        diff: int = abs(price-(self.soums or 0))
        self.soums = price
        self.save(update_fields=['soums'], )
        return diff
