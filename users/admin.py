from django.contrib import admin

from emailservice.models import Mailing, Client


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'period_mail', 'start_mail', 'stop_mail', 'owner')
    list_filter = ('owner',)
    search_fields = ('name', 'owner')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'last_name', 'owner')
    list_filter = ('owner',)
    search_fields = ('email', 'owner')