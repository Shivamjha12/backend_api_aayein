from django.db import models
from Accounts.models import *
# Create your models here.

class goldCoin(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    isname = models.BooleanField(default=False)
    isimage = models.BooleanField(default=False)
    isemail = models.BooleanField(default=False)
    isphone = models.BooleanField(default=False)
    isintrests = models.BooleanField(default=False)
    isage = models.BooleanField(default=False)
    isgender = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.user) + " " + str(self.coins)

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_users')

    class Meta:
        # Ensure each user can have only one friendship record with another user
        unique_together = ['user', 'friend']

    def __str__(self):
        return f"{self.user.name} is friend of {self.friend.name}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username} - {self.timestamp}"
    
    
