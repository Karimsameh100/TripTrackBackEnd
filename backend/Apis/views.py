from django.shortcuts import render
from django.http import Http404, HttpResponse
from rest_framework import mixins,generics
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from itertools import chain
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
import ssl

def home(request):
    return HttpResponse("wellcom to trip track backends")


from rest_framework import status , viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, BasePermission, AllowAny
from rest_framework.decorators import permission_classes,api_view
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt




from .models import *
from .serializers import *



class CompanyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE']:
           return True
        return False

class CompanyRegisterView(APIView):
    #permission_classes=[CompanyPermissions]
    permission_classes = [AllowAny]
    def get(self,request):
        company=Company.objects.all()
        serializer=CompanySerializer(company,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            # Check if email already exists
            email = serializer.validated_data.get('email')
            if AllUsers.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({"message": "Company registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailView(APIView):
    #permission_classes=[CompanyPermissions]
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            serializer = CompanySerializer(company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            company.delete()
            return Response({"message": "Company deleted successfully"})
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

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
            # Check if email already exists
            email = serializer.validated_data.get('email')
            if AllUsers.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView_pk(APIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_type = self.request.query_params.get('user_type', None)
        if user_type == 'company':
            return Company.objects.all()
        elif user_type == 'admin':
            return Admin.objects.all()
        elif user_type == 'user':
            return User.objects.all()
        # Return all users (User, Company, Admin) by combining querysets
        return list(chain(User.objects.all(), Company.objects.all(), Admin.objects.all()))

    def get_serializer_class(self):
        user_type = self.request.query_params.get('user_type', None)
        if user_type == 'company':
            return CompanySerializer
        elif user_type == 'admin':
            return AdminSerializer
        return UserSerializer  # Default case for regular users
    
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)

# mixin_pk get,put,delete 
class mixinuser_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get_object(self):
        user_type = self.request.query_params.get('user_type', None)
        pk = self.kwargs.get('pk')
        
        if user_type == 'company':
            return Company.objects.get(pk=pk)
        elif user_type == 'admin':
            return Admin.objects.get(pk=pk)
        return User.objects.get(pk=pk)  # Default case for regular users

    def get_serializer_class(self):
        user_type = self.request.query_params.get('user_type', None)
        if user_type == 'company':
            return CompanySerializer
        elif user_type == 'admin':
            return AdminSerializer
        return UserSerializer  # Default case for regular users

    def get(self, request, pk, *args, **kwargs):
        company = self.get_object()
        serializer = self.get_serializer_class()(company)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# /////////////////////////////////////
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Ensure the password is a string
        if not isinstance(password, str):
            return Response({"message": "Password must be a string."}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"Attempting to authenticate: {email}")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Determine if the user is a company or a regular user
            try:
                company = Company.objects.get(allusers_ptr=user)
                user_type = "company"
                serializer = CompanySerializer(company)
                print("Company found:", company)
            except Company.DoesNotExist:
                user_type = "user"
                serializer = UserSerializer(user)

            # Create a JWT token for the authenticated user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "Login successful",
                "user_type": user_type,
                "user_info": serializer.data,
                "token": access_token,
                "username": serializer.data.get('name') 
            }, status=status.HTTP_200_OK)
        
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
        serializer = TripsSerializer(data=request.data, context={'company': request.user.company})
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
         updated_trip = serializer.save()  # Save the updated trip
         return Response(TripsSerializer(updated_trip).data, status=status.HTTP_200_OK)  # Return the updated trip
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
@permission_classes([AllowAny])
def findTrips(request):
    departuerStation = request.GET.get('departuerStation')
    destinationStation = request.GET.get('destinationStation')
    date = request.GET.get('date')

    if not all([departuerStation, destinationStation, date]):
        return Response({'error': 'Missing query parameters'}, status=400)

    trips = Trips.objects.filter(
        departuerStation=departuerStation,
        destinationStation=destinationStation,
        date=date
    )
    serializer = TripsSerializer(trips, many=True)
    return Response(serializer.data)
    
class AddFavoriteView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        trip_id = self.request.data.get('trip_id')
        trip = Trips.objects.get(id=trip_id)
        serializer.save(user=self.request.user, trip=trip)

class ListFavoritesView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
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
    


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking(request):
    if request.method == "GET":
        booking = Booking.objects.all()
        serializer = BookSerializer(booking, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            trip_id = request.data.get('trip_id') 
            trip = Trips.objects.get(id=trip_id)  
            booking = serializer.save(trip=trip)
            booking.user = request.user.user
            booking.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_booking_status(request, pk):
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'status' not in request.data:
        return Response({'error': 'Status field is required'}, status=status.HTTP_400_BAD_REQUEST)

    status_data = {'status': request.data['status']}
    serializer = BookSerializer(booking, data=status_data, partial=True)
    
    if serializer.is_valid():
        serializer.save()

        # Send email based on the status
        if status_data['status'] == 'Accepted':
            subject = "Booking Confirmed"
            body = f"Dear {booking.user.name}, your booking for trip {booking.trip} has been confirmed. Please proceed to payment from accepted trips in your profile."
            send_email(subject, body, booking.user.email)
        elif status_data['status'] == 'Rejected':
            subject = "Booking Rejected"
            body = f"Dear {booking.user.name}, your booking for trip {booking.trip} has been rejected. Please choose another time."
            send_email(subject, body, booking.user.email)
            
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       


def send_email(subject, body, recipient_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = recipient_email

    try:
        # Create an SSL context to ignore certificate verification (not recommended for production)
        context = ssl._create_unverified_context()

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls(context=context)  # Upgrade the connection to secure
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print(f"Error sending email: {e}")
    
from rest_framework.authentication import BaseAuthentication
class JWTAuthentication(BaseAuthentication):
    def get_user_id_from_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            user_id = self.get_user_id_from_token(token)
            if user_id:
                user = User.objects.get(id=user_id)
                return (user, token)
            else:
                return None
        else:
            return None
    
class CurrentUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        user, token = JWTAuthentication().authenticate(request)
        if user:
             return Response({
                'user_id': user.id,
                'email': user.email,
                'username': user.name,
            })
        else:
            return Response({'error': 'Invalid authentication token'}, status=401)
        


# from rest_framework.response import Response
# from rest_framework.views import APIView
# from paypalrestsdk import Payment

# class CreatePaymentView(APIView):
#     def post(self, request):
#         # Get the payment amount and currency from the request
#         amount = request.data.get('amount')
#         currency = request.data.get('currency')

#         # Create a new payment using the paypalrestsdk library
#         payment = Payment({
#             'intent': 'sale',
#             'payer': {
#                 'payment_method': 'paypal'
#             },
#             'transactions': [
#                 {
#                     'amount': {
#                         'total': amount,
#                         'currency': currency
#                     }
#                 }
#             ]
#         })

#         if payment.create():
#             return Response({
#                 'payment_id': payment.id,
#                 'approval_url': payment.links[1].href
#             })
#         else:
#             return Response({'error': 'Error creating payment'}, status=400)
        

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
           trip_id = request.data.get('trip_id')
           booking_id = request.data.get('booking_id')
           trip = Trips.objects.get(id=trip_id)
           booking = Booking.objects.get(id=booking_id)
           payment = serializer.save(trip=trip, booking=booking, user=request.user)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SinglePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Payment.objects.get(id=pk)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        payment = self.get_object(pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    def put(self, request, pk):
        payment = self.get_object(pk)
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        payment = self.get_object(pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)