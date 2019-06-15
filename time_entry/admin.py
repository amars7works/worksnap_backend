from django.contrib import admin

from time_entry.models import WhitelistIpAddress, TimeEntry


# Register your models here.

class TimeEntryAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'from_timestamp', 'user_ip')
	search_fields = ('user_id', 'user_ip')


class WhitelistIpAddressAdmin(admin.ModelAdmin):
	list_display = ('ipaddress',)
	search_fields = ('ipaddress',)

admin.site.register(TimeEntry, TimeEntryAdmin)
admin.site.register(WhitelistIpAddress, WhitelistIpAddressAdmin)
