from django.contrib import admin
from .models import Client, Message, Debt

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rut', 'salary', 'savings')
    search_fields = ('name', 'rut')
    readonly_fields = ('id',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'text', 'role', 'sent_at')
    search_fields = ('client__name', 'text')
    list_filter = ('role',)

class DebtAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'institution', 'amount', 'due_date')
    search_fields = ('client__name', 'institution')
    list_filter = ('institution',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Debt, DebtAdmin)