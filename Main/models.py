from django.db import models
from Accounts.models import *
# Create your models here.

class goldCoin(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.user) + " " + str(self.coins)

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_users')

    class Meta:
        # Ensure each user can have only one friendship record with another user
        unique_together = ['user', 'friend']

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
    
