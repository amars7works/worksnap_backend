from django.contrib import admin
from summary_report.models import BankAccountNumbers, Salary


class BankAccountNumberAdmin(admin.ModelAdmin):
	list_display = ('user','account_number','IFSC_code')
	search_fields = ('user',)

admin.site.register(BankAccountNumbers,BankAccountNumberAdmin)

class SalaryAdmin(admin.ModelAdmin):
	list_display = ('user','Salary')
	search_fields = ('user',)

admin.site.register(Salary,SalaryAdmin)