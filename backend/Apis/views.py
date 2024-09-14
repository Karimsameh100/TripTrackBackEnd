from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework import mixins,generics

def home(request):
    return HttpResponse("wellcom to trip track backends")


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.decorators import permission_classes,api_view
from rest_framework import permissions

from .models import Company ,User,Trips,Bus,Booking
# from .serializers import CompanySerializer,UserSerializer
from .serializers import *
from .serializers import CompanySerializer, UserSerializer,TripSerializer,BookSerializer,busSeliarizer


from django.contrib.auth import authenticate

class CompanyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.has_perm('companies.change_company') or request.user.has_perm('companies.add_company')
        return False

class CompanyRegisterView(APIView):
    permission_classes=[CompanyPermissions]
    def get(self,request):
        company=Company.objects.all()
        serializer=CompanySerializer(company,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Company registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.permissions import BasePermission

class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.has_perm('auth.change_user') or request.user.has_perm('auth.add_user')
        return False

class UserRegisterView(APIView):
    permission_classes = [UserPermissions]
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
    permission_classes = [UserPermissions]
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
# ///////////////////////////////////////////////////////
#mixins get,post
class Mixinuser_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

# mixin_pk get,put,delete 
class mixinuser_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    def get(self,request,pk):
        return self.retrieve(request)
    
    def put(self,request,pk):
        return self.update(request)
    
    def delete(self,request,pk):
        return self.destroy(request)
# /////////////////////////////////////
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
    

class ReviewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.has_perm('reviews.change_review') or request.user.has_perm('reviews.add_review')
        return False
    

class ReviewListCreateView(APIView):
    permission_classes = [ReviewPermissions]

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
    permission_classes = [ReviewPermissions]
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
    
    
    
# trips and schedule ------------
# from django.shortcuts import render
# from rest_framework import viewsets # type: ignore
# from .models import * 
# from .serializers import *
# # Create your views here.

# class PassengerViewSet(viewsets.ModelViewSet):
#     queryset=Passenger.objects.all()
#     serializer_class=PassengerSerializer
    
     

# class TripViewSet(viewsets.ModelViewSet):
#     queryset=Trip.objects.all()
#     serializer_class=TripSerializer   

# class SchedualViewSet(viewsets.ModelViewSet):
#     queryset=Schedual.objects.all()
#     serializer_class=SchedualSerializer  

from rest_framework.permissions import BasePermission

class TripPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.has_perm('trips.change_trip') or request.user.has_perm('trips.add_trip')
        return False


@api_view(['GET','POST'])
@permission_classes([TripPermissions])
def trips(request):
    if request.method == "GET":
        trips = Trips.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
@permission_classes([TripPermissions])
def trip(request, pk):
    try:
        trip = Trips.objects.get(pk=pk)
    except Trips.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = TripSerializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

        

    
    



