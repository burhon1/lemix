from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    """
        Change password Serializer
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


# class UserPhoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['phone']

#     # def create(self, validated_data):
#     #     # send otp-sms service
#     #     return 


# class ChangePassword2Serializer(serializers.Serializer):
#     """
#         Reset Password Serializer 
#     """
#     phone_number = serializers.CharField(required=True)
#     token = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)