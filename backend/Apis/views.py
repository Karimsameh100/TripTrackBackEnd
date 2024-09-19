from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework import mixins,generics
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return HttpResponse("wellcom to trip track backends")


from rest_framework import status , viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, BasePermission, AllowAny
from rest_framework.decorators import permission_classes,api_view
from rest_framework import permissions

from .models import *
from .serializers import *
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


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.has_perm('auth.change_user') or request.user.has_perm('auth.add_user')
        return False
    
class UserRegisterView(APIView):
    # permission_classes = [UserPermissions]---------------------
    permission_classes = [AllowAny]
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
    

class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
            if request.user.is_anonymous:  # Check if the user is anonymous
                return False
            return request.user.is_admin  # Check if the user is an Admin
        return False
    
class AdminView(APIView):
    permission_classes = [AdminPermissions]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def get(self, request):
        admins = self.queryset.all()
        serializer = self.serializer_class(admins, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminView_pk(APIView):
    permission_classes = [AdminPermissions]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

    def get_object(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except Admin.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        admin = self.get_object(pk)
        serializer = self.serializer_class(admin)
        return Response(serializer.data)

    def put(self, request, pk):
        admin = self.get_object(pk)
        serializer = self.serializer_class(admin, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        admin = self.get_object(pk)
        admin.delete()
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
    permission_classes = [AllowAny] 
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
     
    
        if user:
            if hasattr(user, 'company'):
                return Response({"message": "Logged in as company", "user_type": "company"}, status=status.HTTP_200_OK)
            elif hasattr(user, 'admin'):
                return Response({"message": "Logged in as admin", "user_type": "admin"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Logged in as user", "user_type": "user"}, status=status.HTTP_200_OK)
        
        return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)




class AllUsersView(APIView):
    permission_classes = [AllowAny]  # استخدم AllowAny مؤقتًا للتأكد من أن المشكلة ليست في الصلاحيات

    def get(self, request):
        user_type = request.query_params.get('user_type', None)
        if user_type:
            all_users = AllUsers.objects.filter(user_type=user_type)
        else:
            all_users = AllUsers.objects.all()

        serializer = AllUsersSerializer(all_users, many=True)
        return Response(serializer.data)



class ReviewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.has_perm('reviews.change_review') or request.user.has_perm('reviews.add_review')
        return False
    

class ReviewListCreateView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]
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
    

# from django.contrib.auth import authenticate

# class TripPermissions(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         elif request.method in ['POST', 'PUT', 'DELETE']:
#             username = request.data.get('username')
#             password = request.data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 return user.has_perm('trips.change_trip') or user.has_perm('trips.add_trip')
#             return False
#         return False

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def trips(request):
    if request.method == "GET":
        trips = Trips.objects.all()
        serializer = TripsSerializer(trips, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = TripsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT','DELETE'])
@permission_classes([AllowAny])
def trip(request, pk):
    try:
        trip = Trips.objects.get(pk=pk)
    except Trips.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = TripsSerializer(trip)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = TripsSerializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status= status.HTTP_205_RESET_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

    
class FavoriteListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    
    
class CityView(APIView):
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return City.objects.all()

    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except City.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            city = self.get_object(pk)
            serializer = CitySerializer(city)
            return Response(serializer.data)
        else:
            cities = self.get_queryset()
            serializer = CitySerializer(cities, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        city = self.get_object(pk)
        serializer = CitySerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        city = self.get_object(pk)
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



