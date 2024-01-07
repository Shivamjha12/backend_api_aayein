from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
import jwt,datetime
from rest_framework import generics
from django.http import JsonResponse
import json
import requests
from django.shortcuts import redirect

google_client_id='724370149000-arj17qs8ha255erpk861tidve3i005rp.apps.googleusercontent.com'
redirect_uri= 'http://127.0.0.1:8000/api-user/v1/auth/google/callback'
google_client_secret='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'

class register(APIView):

    def post(self,request):
        serializers = UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
    

class login(APIView):
    
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('You are not registered on the platform')
        if not user.check_password(password):
            raise AuthenticationFailed('password is incorrect')
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=720),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        # .decode('utf-8')
        response = Response()
        # response.set_cookie(key='jwt',value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        
        return response

class userView(APIView):
    
    def get(self, request,JWTUser):
        token = None
        if JWTUser!='None':
            token = JWTUser
        # request.COOKIES.get('jwt')
        print(type(token),"typeeeeeeeeeeeeeeeeeeeeeeeeee")
        print(token,"Here is the token, -----------sssssssssssss-----s-s--s-s-sssssssss")
        if not token:
            raise AuthenticationFailed('Unauthenticated please login')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated please login')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        print(serializer.data,"--------------------------------------------")
        
        return Response(serializer.data,status=200)

class logout(APIView):
    
    def post(self, request):
        response = Response()
        # response.delete_cookie('jwt')
        response.data = {
            'message':"Successfully Logout"
        }
        return response



# Google Authentication

def google_signin(request):
    google_client_id='724370149000-arj17qs8ha255erpk861tidve3i005rp.apps.googleusercontent.com'
    google_client_secret='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'
    redirect_uri = 'http://127.0.0.1:8000/api-user/v1/auth/google/callback'

    # Redirect the user to Google for authorization
    auth_url = (
        'https://accounts.google.com/o/oauth2/auth'
        f'?client_id={google_client_id}'
        '&response_type=code'
        '&scope=openid profile email'
        f'&redirect_uri={redirect_uri}'
    )

    return redirect(auth_url)
# JsonResponse({'auth_url': auth_url})



def google_callback(request):
    if 'code' in request.GET:
        print(f"Code is in the request,----------------------------------------------------")
        code = request.GET['code']
        token_url = 'https://accounts.google.com/o/oauth2/token'
        token_data = {
            'code': code,
            'client_id': google_client_id,
            'client_secret': google_client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        if 'access_token' in token_json:
            user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f'Bearer {token_json["access_token"]}'}
            
            params = {'fields': 'id,email,verified_email,name,given_name,family_name,picture,locale'}
            
            user_info_response = requests.get(user_info_url, headers=headers, params=params)
            user_info_json = user_info_response.json()

            email = user_info_json.get('email')
            google_id = user_info_json.get('id')
            given_name = user_info_json.get('given_name')
            family_name = user_info_json.get('family_name')
            picture_url = user_info_json.get('picture')
            
            user = User.objects.create(
                email=email,
                name=f'{given_name} {family_name}',
                password=google_id,
                google_id=google_id,
                google_image_url=picture_url,
                is_google=True)
            user.save()
            
            response_data = {
                'message': 'user created successfully.',
                'user_info': {
                    'email': email,
                    'google_id': google_id,
                    'given_name': given_name,
                    'family_name': family_name,
                    'picture_url': picture_url,
                }
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'message': "User not authenticated"})
    return JsonResponse({'message': "User not authenticated"})

# profile creation form

class create_profile(APIView):
    def post(self, request):
        user  = request.POST.get('user')
        phone = request.POST.get('phone')
        image = request.POST.get('image')
        intrests = request.POST.get('intrests')
        try:
            userObject = User.objects.filter(email=user).first()
            userObject.phone = phone
            userObject.image = image
            userObject.intrests = intrests
            userObject.save()
        except:
            return Response({"message":"User not found"})
        return Response({"message":"Profile Created Successfully"})
        