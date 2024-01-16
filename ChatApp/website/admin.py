from django.contrib import admin
from .models import ChatSession, Message, RequiredEntities, ChatEntities

admin.site.register(ChatSession)
admin.site.register(Message)
admin.site.register(RequiredEntities)
admin.site.register(ChatEntities)
