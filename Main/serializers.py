# serializers.py
from rest_framework import serializers
from .models import *

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password']
        
class GoldCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = goldCoin
        fields = '__all__'
        # exclude = ['password']
        
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.EmailField(source="sender.email")
    receiver = serializers.EmailField(source="receiver.email")
    timestamp = serializers.SerializerMethodField()

    def get_timestamp(self, obj):
        # Customize the timestamp format as needed
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'timestamp', 'conversation']
        

