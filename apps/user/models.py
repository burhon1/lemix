from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


from .data.chooses import COURSES_SEXES, COURSES_STATUS
from .querysets.managers import CustomUserManager, UserManager
from .querysets.devices_managers import DeviceManager

# Foydalanuvchilarni malumotlari saqlanadi
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(
        _('Telefon raqam'), max_length=200, unique=True
    )
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    picture = models.ImageField(upload_to='user/',null=True,blank=True,default='https://www.computerhope.com/issues/pictures/win10-user-account-default-picture.jpg')
    birthday = models.DateField(null=True,blank=True)
    gender = models.PositiveSmallIntegerField(choices=COURSES_SEXES,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True)
    otp = models.PositiveIntegerField("OTP", null=True)
    educenter = models.PositiveIntegerField(blank=True, null=True)
    
    def full_name(self):
        return str(self.first_name)+" "+str(self.last_name) # qiymati none bo'lsa xato qaytardi

    class Meta:
        ordering = ("created_at",)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    users = UserManager()
    def __str__(self):
        return self.phone
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     print("before: ", self.user_permissions.all())
    #     permissions = [perm.id for group in self.groups.all() for perm in group.permissions.all()]
    #     self.user_permissions.add(permissions)
    #     print("then: ", self.user_permissions.all())
        

class Logger(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

# # Leadni qayerdan kelib tushganlar ro'yxati turadi
# class LeadWhere(models.Model):
#     icon = models.CharField(max_length=50,null=True,blank=True)
#     title = models.CharField(max_length=100)
    
#     def __str__(self) -> str:
#         return self.title
    
# # Lead modeli kursga qiziquvchilar ro'yxati saqlanadi
# class Lead(models.Model):
#     fio = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=50)
#     sex = models.PositiveSmallIntegerField(choices=COURSES_SEXES)
#     birtday = models.DateField()
#     status = models.PositiveSmallIntegerField(choices=COURSES_STATUS)
#     lead_where = models.ForeignKey(LeadWhere,on_delete=models.CASCADE)
#     comment = models.TextField()
#     course = models.ForeignKey(Course,on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.fio

class UserDevices(models.Model):
    STATUS = (
        (1, 'Yangi'),
        (2, 'Bloklangan'),
        (3, 'Qayta ochilgan'),
    )
    ip = models.CharField("Foydalanuvchi IP si.", max_length=100)
    device = models.CharField("Qurilma", max_length=100)
    mac_address=models.CharField(max_length=100,null=True,blank=True)
    connected = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, models.CASCADE)
    status = models.PositiveSmallIntegerField(
        "Qurilma statusi", choices=STATUS, default=1
    )
    objects = models.Manager()
    devices = DeviceManager()
    def __str__(self):
        return self.user.full_name()