from django.shortcuts import render
from django.http import Http404, HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("wellcom to trip track backends")


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Company ,User
# from .serializers import CompanySerializer,UserSerializer
from .serializers import *


from django.contrib.auth import authenticate




class CompanyRegisterView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserRegisterView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView_pk(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise  Http404
        
    def get(self,request,pk):
       user=self.get_object(pk)
       serializer=UserSerializer(user)
       return Response(serializer.data)    
    
    def put(self,request,pk):
        user=self.get_object(pk)
        serializer=UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)
    
    def delete(self,request,pk):
        user=self.get_object(pk)
        user.delete()
        return Response(status=204)


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
    

class ReviewListCreateView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None

    def get(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        review.delete()
        return Response({'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)