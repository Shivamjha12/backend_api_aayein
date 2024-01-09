from django.urls import path, include
from .views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('coincheck/<str:user_id>', AddGoldCoins.as_view(),name="coincheck"),
    path('getcoins/<str:user>', getUserCoins.as_view(),name="getcoin"),
    path('addfriend', addFriend.as_view(),name="addfriend"),
    path('getfriends/<str:currentuser>', getFriends.as_view(),name="getfriends"),
    path('send-message/<str:sender_id>/<str:receiver_id>/', SendMessage.as_view(), name='send_message'),
    path('get-chat-history/<str:user_id_1>/<str:user_id_2>/', GetChatHistory.as_view(), name='get_chat_history')
    
]