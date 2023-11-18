from django.contrib import admin
from .models import Chat, ChatMessage, FaceInfo, User

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(FaceInfo)
