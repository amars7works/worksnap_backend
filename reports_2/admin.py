from django.contrib import admin
from reports_2.models import BankAccountNumber
# Register your models here.

class BankAccountNumberAdmin(admin.ModelAdmin):
	list_display = ('user','account_number')
	search_fields = ('user',)

admin.site.register(BankAccountNumber,BankAccountNumberAdmin)
