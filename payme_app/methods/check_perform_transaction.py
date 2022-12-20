from payme_app.utils.get_params import get_params

from payme_app.serializers.create_transaction import MerchatTransactionsModelSerializer
import random


class CheckPerformTransaction:
    def __call__(self, params: dict) -> dict:
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)

        # response = {
        #     "result": {
        #         "allow": True,
        #         }
        #     }
        
        datas = params
        
        response = {
            "result": {
                "allow": True,
            "items": [  #товарная позиция, обязательное поле для фискализации
                {
                    "title": "BellaTme",  #нааименование товара или услуги
                    "price": datas['amount'],  #цена за единицу товара или услуги, сумма указана в тийинах
                    "count": int(datas['account']['order_id']),  #кол-во товаров или услуг
                    "code": "10899001001000000",  # код *ИКПУ обязательное поле
                    "vat_percent": 15,  #обязательное поле, процент уплачиваемого НДС для данного товара или услуги
                    "package_code": f"{random.randint(100000,999999)}",  #Код упаковки для конкретного товара или услуги, содержится на сайте в деталях найденного ИКПУ.
                }
            ]
        }
    }


        return response
