from django.contrib import admin
from messenger_app import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id',)
