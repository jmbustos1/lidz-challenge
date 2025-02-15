from django.contrib import admin
from .models import Client, Message, Debt

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rut', 'salary', 'savings', 'age')
    search_fields = ('name', 'rut')
    readonly_fields = ('id',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'text', 'role', 'sentAt')
    search_fields = ('client__name', 'text')
    list_filter = ('role',)

class DebtAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'institution', 'amount', 'dueDate')
    search_fields = ('client__name', 'institution')
    list_filter = ('institution',)

admin.site.register(Client, ClientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Debt, DebtAdmin)