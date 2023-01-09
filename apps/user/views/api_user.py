from rest_framework.generics import UpdateAPIView
from rest_framework import status

from user.serializers import ChangePasswordSerializer, UserPhoneSerializer, ChangePassword2Serializer
from user.models import CustomUser

class ChangePasswordView(UpdateAPIView):
    """
    `Headers`: 
        Authorization: Bearer <token>
    `POST`:
        old_password
        new_password
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Неправильный пароль."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save(update_fields='password')
            return Response("Success", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ForgotPasswordView(generics.CreateAPIView):
#     serializer_class = UserPhoneSerializer
#     permission_classes = (AllowAny,)

#     def perform_create(self, serializer):
#         try:
#             instance = User.objects.get(username__exact=serializer.validated_data.get('username'))
#         except User.DoesNotExist as e:
#             try:
#                 instance = User.objects.get(username__exact=serializer.validated_data.get('username'))
#             except User.DoesNotExist as e:
#                 raise ValidationError2("Пользователь с этим номером телефона не найден")
#         instance.set_reset_password_token()
#         instance.save()
#         # TODO: sending otp logic will be here when sms service is ready


# class UserResetPasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for changing password.
#     """
#     serializer_class = ChangePassword2Serializer
#     model = User
#     permission_classes = (AllowAny,)

#     def update(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             self.object = User.objects.get(username__exact=request.data.get('username'))
#         except User.DoesNotExist:
#             try:
#                 self.object = User.objects.get(username__exact=request.data.get('username'))
#             except User.DoesNotExist:
#                 raise ValidationError2("Не удалось найти пользователя.", code="NOT_FOUND",
#                                        status_code=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             # Check old password
#             if serializer.data.get("token") != self.object.reset_password_token:
#                 raise ValidationError2("Неверный код.", code="token", status_code=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.reset_password_token = None
#             self.object.confirm_register_token()
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return Response({"status": "Success"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)