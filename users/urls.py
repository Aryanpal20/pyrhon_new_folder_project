from django.urls import path
from .views import UserRegister,GetAllUser,UserLogin

urlpatterns = [ 
    path('register/', UserRegister.as_view(), name='Register'),
    # path('get_user/<int:pk>', GetAllUser.as_view(), name='Get_User'),
    path('get_user/', GetAllUser.as_view(), name='Get_User'),
    path('login/', UserLogin.as_view(), name='Login'),
]
