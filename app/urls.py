from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('user/create', views.createUser, name='user-create'),
    path('user/list', views.getUsersList, name='users-list'),
    path('user/<int:id>', views.getUser, name='users-get'),
    path('user/patch/<int:id>', views.patchUser, name='users-patch'),
    path('user/delete/<int:id>', views.deleteUser, name='users-delete'),
    path('user/chats/<int:id>', views.getUserChats, name='users-chats'),
    path('user/<int:id>/face/add', views.addFaceInfo, name='users-face-add'),
    path('user/<int:id>/face/remove',
         views.removeFaceInfo, name='users-face-remove'),
    path('chat/message', views.sendMessage, name='chat-message'),
    path('chat/create', views.createChat, name='chat-create'),
    path('chat/join', views.joinChat, name='chat-join'),
    path('chat/leave', views.leaveChat, name='chat-leave'),
    path('chat/<int:id>', views.getChat, name='chat-get'),
]
