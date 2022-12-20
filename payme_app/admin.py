from django.contrib import admin

from payme_app.models import Order
from payme_app.models import MerchatTransactionsModel

class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'updated_at')
    list_display_links = ('id',)
    search_fields = ('id', 'amount',)
    list_filter = ('id',)


admin.site.register(Order, TodoAdmin)
admin.site.register(MerchatTransactionsModel)
