from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from Accounts.models import User
from .serializers import *



class AddGoldCoins(APIView):
    def post(self, request, user_id):
        try:
            user = User.objects.filter(email=user_id).first()
            gold_coins = goldCoin.objects.get(user=user)
            userd = User.objects.filter(email=user_id)
            # Loop through each field in the User model
            print(  len(str(user.name))  ,"nameeeeeee",user.image,"imageeeeee")
            if len(str(user.name))>1 and gold_coins.isname == False:
                gold_coins.isname = True
                gold_coins.coins += 10
                
            if len(str(user.image))>1 and gold_coins.isimage == False:
                gold_coins.isimage = True
                gold_coins.coins += 10
                
            if len(str(user.email))>1 and gold_coins.isemail == False:
                gold_coins.isemail = True
                gold_coins.coins += 10
                
            if len(str(user.phone))>1 and gold_coins.isphone == False:
                gold_coins.isphone = True
                gold_coins.coins += 10
                
            if len(str(user.intrests))>1 and gold_coins.isintrests == False:
                gold_coins.isintrests = True
                gold_coins.coins += 10
                
            if len(str(user.age))>=1 and gold_coins.isage == False:
                gold_coins.isage = True
                gold_coins.coins += 10
                
            if len(str(user.gender))>1 and gold_coins.isgender == False:
                gold_coins.isgender = True
                gold_coins.coins += 10
                
            gold_coins.save()
            
            return Response({"message": "Gold coins added successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except goldCoin.DoesNotExist:
            return Response({"message": "Gold coins not found for the user"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class addFriend(APIView):
    
    def post(self, request):
        current_user = request.data.get('current_user')
        friendmail = request.data.get('friendmail')
        
        try:
            user = User.objects.filter(email=current_user).first()
            if user is None:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            friendmailObj = User.objects.filter(email=friendmail).first()
            if friendmailObj is None:
                return Response({"message": "Friend not found"}, status=status.HTTP_404_NOT_FOUND)
            
            friendConn = Friend.objects.create(user=user, friend=friendmailObj)
            friendConn.save()
            
            return Response({"message": "Friend added successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class getFriends(APIView):
    
    def get(self, request, currentuser):
        try:
            user = User.objects.get(email=currentuser)
            friends = Friend.objects.filter(user=user)
            print(friends)
            friendList = []
            friendObj = []
            for i in friends:
                friendList.append(i.friend)
            for i in friendList:
                userObj = User.objects.filter(email=i).first()
                friendObj.append(userObj)
            print("--------------Here--------------------",friendObj)
            if not friends.exists():
                return Response({"message": "Friends not found"}, status=status.HTTP_404_NOT_FOUND)
            
            friend_serializer = FriendSerializer(friendObj, many=True)
            return Response({"friends": friend_serializer.data}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SendMessage(APIView):
    
    def post(self, request, sender_id, receiver_id):
        
        try:
            sender = User.objects.filter(email=sender_id).first()
            receiver = User.objects.filter(email=receiver_id).first()

            content = request.data.get('content')

            if not content:
                return Response({"message": "Message content cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a unique conversation identifier based on user IDs
            conversation = f"{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"

            message = Message.objects.create(sender=sender, receiver=receiver, content=content, conversation=conversation)
            serializer = MessageSerializer(message)
            return Response({"message": "Message sent successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# views.py
class GetChatHistory(APIView):

    def get(self, request, user_id_1, user_id_2):
        try:
            # Create a unique conversation identifier based on user IDs
            conversation = f"{min(user_id_1, user_id_2)}_{max(user_id_1, user_id_2)}"

            messages = Message.objects.filter(conversation=conversation)
            serializer = MessageSerializer(messages, many=True)
            return Response({"messages": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class getUserCoins(APIView):
    
    def get(self, request, user):
        coins = goldCoin.objects.filter(user__email=user).first()
        serializer = GoldCoinSerializer(coins)
        return Response({"coins": serializer.data})
        




