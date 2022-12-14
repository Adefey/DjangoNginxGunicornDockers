from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'date')
    list_dosplay_links = ('author', 'text')
    search_fields = ('author', 'text')


admin.site.register(Message, MessageAdmin)
