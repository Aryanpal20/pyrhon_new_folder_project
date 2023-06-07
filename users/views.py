from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

# Create your views here.

class UserRegister(APIView):
    def post(self,request):
        user_data = request.data
        user_data['username'] = user_data['email']
        user_data['password'] = make_password(user_data['password'])
        user = UserSerializers(data=user_data)
        if user.is_valid(raise_exception=True):
            user.save()
            return Response({"Message":"User register successful"},status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class GetAllUser(APIView):
    def get(self, request, pk=None):
        params = self.request.query_params
        if params.get('pk') :
            user = User.objects.get(pk=params.get('pk'))
            serializer = UserSerializers(user)
        else:
            user = User.objects.all()   
            serializer = UserSerializers(user, many=True)
        return Response (serializer.data) 
    
    def delete(self, request, pk=None):
        params = self.request.query_params
        user = get_object_or_404(User, pk=params.get('pk'))
        user.delete()
        return Response({"Message":"user Deleted Successfully."},status=status.HTTP_200_OK)

# class GetAllUser(APIView):
#     def get(self, request, pk=None):
#         if pk:
#             user = User.objects.get(pk=pk)
#             serializer = UserSerializers(user)
#         else:
#             user = User.objects.all()   
#             serializer = UserSerializers(user, many=True)
#         return Response (serializer.data) 
    
#     def delete(self, request, pk=None):
#         user = get_object_or_404(User, pk=pk)
#         user.delete()
#         return Response({"Message":"user Deleted Successfully."},status=status.HTTP_200_OK)
    


class UserLogin(APIView):

    def post(self,request):
        data = request.data
        user = User.objects.get(email=data['username'])
        if user is not None:
            checkpwd = check_password(data['password'], user.password)
            if checkpwd :
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return Response({'token': token})
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        