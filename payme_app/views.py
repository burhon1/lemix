import base64
import binascii

from django.conf import settings
from django.http import HttpResponse
from payme.methods.generate_link import GeneratePayLink

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from payme_app.utils.logger import logged

from payme_app.errors.exceptions import MethodNotFound
from payme_app.errors.exceptions import PermissionDenied
from payme_app.errors.exceptions import PerformTransactionDoesNotExist

from payme_app.methods.check_transaction import CheckTransaction
from payme_app.methods.cancel_transaction import CancelTransaction
from payme_app.methods.create_transaction import CreateTransaction
from payme_app.methods.perform_transaction import PerformTransaction
from payme_app.methods.check_perform_transaction import CheckPerformTransaction

from rest_framework.permissions import IsAuthenticated

class MerchantAPIView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        password = request.META.get('HTTP_AUTHORIZATION')
        if self.authorize(password):
            incoming_data: dict = request.data
            incoming_method: str = incoming_data.get("method")
            logged_message: str = "Incoming {data}"

            logged(
                logged_message=logged_message.format(
                    method=incoming_method,
                    data=incoming_data
                ),
                logged_type="info"
            )
            try:
                paycom_method = self.get_paycom_method_by_name(
                    incoming_method=incoming_method
                )
            except ValidationError:
                raise MethodNotFound()
            except PerformTransactionDoesNotExist:
                raise PerformTransactionDoesNotExist()

            paycom_method = paycom_method(incoming_data.get("params"))

        return Response(data=paycom_method)

    @staticmethod
    def get_paycom_method_by_name(incoming_method: str) -> object:
        """Use this static method to get the paycom method by name.

        :param incoming_method: string -> incoming method name
        """
        available_methods: dict = {
            "CheckTransaction": CheckTransaction,
            "CreateTransaction": CreateTransaction,
            "CancelTransaction": CancelTransaction,
            "PerformTransaction": PerformTransaction,
            "CheckPerformTransaction": CheckPerformTransaction
        }

        try:
            MerchantMethod = available_methods[incoming_method]
        except Exception:
            error_message = "Unavailable method: %s" % incoming_method
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise MethodNotFound(error_message=error_message)

        merchant_method = MerchantMethod()

        return merchant_method

    @staticmethod
    def authorize(password: str) -> None:
        """Authorize the Merchant.
        :param password: string -> Merchant authorization password
        """
        is_payme: bool = False
        error_message: str = ""

        if not isinstance(password, str):
            error_message = "Request from an unauthorized source!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        password = password.split()[-1]

        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            error_message = "Error when authorize request to merchant!"
            logged(
                logged_message=error_message,
                logged_type="error"
            )
            raise PermissionDenied(error_message=error_message)

        merchant_key = password.split(':')[-1]

        if merchant_key == settings.PAYCOM.get('paycom_key'):
            is_payme = True

        if merchant_key != settings.PAYCOM.get('paycom_key'):
            logged(
                logged_message="Invalid key in request!",
                logged_type="error"
            )

        if is_payme is False:
            raise PermissionDenied(
                error_message="Unavailable data for unauthorized users!"
            )

        return is_payme



#************

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payme_app.serializers.order_serializers import OrderSerializers
from payme_app.models import Order


@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def create_order(request):
    # account = request.user
    # user = Order(customer=account)
    print("!!!!!!!!!: ", request.data)

    if 'customer_id' and 'course_id' in request.data.keys():
        if request.method == 'POST':
            serializer = OrderSerializers(data=request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                print("%%%%%%%: ", serializer.data)
                print("''''''''''': ", Order.amount)
                print("*********: ", serializer.data['id'])
                print("*********: ", serializer.data['amount']*100)
                print("*********: ", serializer.data)
                data['response'] = "Order successfully created."

                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return HttpResponse("Please authenticate!")