from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from tenants.models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['name']


@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'domain']
    list_display_links = ['domain']
