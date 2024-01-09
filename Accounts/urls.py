from django.urls import path, include
from .views import *

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('register', register.as_view()),
    path('login', login.as_view()),
    # path('googlesignin',name="googlesignin"),
    path('user/<str:JWTUser>', userView.as_view()),
    path('logout', logout.as_view()),
    path('auth/google/', google_signin, name='google_signin'),
    path('auth/google/callback', google_callback, name='google_callback'),
    # path for profile Creation Form
    path('initprofile', create_profile.as_view(),name="create_profile"),
    path('getUser/<str:userEmail>',getUser.as_view(),name="getUser"),
    
]