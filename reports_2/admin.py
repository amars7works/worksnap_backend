from django.contrib import admin
from reports_2.models import BankAccountNumber, ApplyLeave
# Register your models here.

class BankAccountNumberAdmin(admin.ModelAdmin):
	list_display = ('user','account_number')
	search_fields = ('user',)

admin.site.register(BankAccountNumber,BankAccountNumberAdmin)

class ApplyLeaveAdmin(admin.ModelAdmin):
	list_display = ('user','created_at','leave_start_date','leave_end_date','apply_reason','leave_status','denied_reason','Type_of_Request')
	search_fields = ('user',)

admin.site.register(ApplyLeave,ApplyLeaveAdmin)
