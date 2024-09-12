from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("wellcom to trip track backends")


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company ,User
# from .serializers import CompanySerializer,UserSerializer
from .serializers import CompanySerializer, UserSerializer


from django.contrib.auth import authenticate




class CompanyRegisterView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        # user = authenticate(username=email, password=password) 
        if user:
            if hasattr(user, 'company'):
                return Response({"message": "Logged in as company"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Logged in as user"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
