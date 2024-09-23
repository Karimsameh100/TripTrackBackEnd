from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        if 'confirm_password' in data and data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data.get('user_type', 'user')
        )
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.user_type = validated_data.get('user_type', instance.user_type)
        
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    ReviewCustomerDetails = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Review = validated_data.get('Review', instance.Review)
        instance.ReviewCustomerRate = validated_data.get('ReviewCustomerRate', instance.ReviewCustomerRate)
        instance.save()
        return instance
    
    
    
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        if 'confirm_password' in data and data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords must match.")
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        admin = Admin( email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            user_type=validated_data.get('user_type', 'admin')
        )
        if password:
            admin.set_password(password)
        admin.save()
        return admin

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUsers
        fields = '__all__'

    
    
class userNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
    

        
class TripsSerializer(serializers.ModelSerializer):
    users=userNameSerializer(source="user" , read_only=True)
    class Meta:
        model = Trips
        fields = '__all__'  # Include all fields of the Trips model

    def create(self, validated_data):
        # Assign the trip to the company from the context (passed through views)
        company = self.context['company']
        validated_data['bus'] = company.bus  # Assign the bus from the company
        trip = Trips.objects.create(**validated_data)
        trip.companies.add(company)  # Add the company to the trip's related companies
        return trip

class CompanySerializer(serializers.ModelSerializer):
    company_trips = TripsSerializer(many=True, read_only=True) 
    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, data):
        if 'confirm_password' in data and data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords must match.")
        return data


   
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        commercial_register = validated_data.pop('commercial_register', None)
        company = Company(
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            commercial_register=commercial_register ,
            work_license=validated_data['work_license'],
            certificates=validated_data['certificates'],
            user_type=validated_data.get('user_type', 'company'),
        )
        if password:
            company.set_password(password)
        company.save()
        return company
       

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class busSeliarizer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"



class FavoriteSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Favorite
        fields = ["user_id", "trip_id"]
        extra_kwargs = {
            "user_id": {"required": True},
            "trip_id": {"required": True},
        }

    def to_representation(self, instance):
        return {
            "favorite_id": instance.id,
            "user_name": instance.user_id.name,
            "trip_date": instance.trip_id.date,
            "trip_avilable_places": instance.trip_id.avilabalPlaces,
            "trip_price": instance.trip_id.price,
            "trip_departure_time": instance.trip_id.departuerTime,
            "trip_departure_station": instance.trip_id.departuerStation,
            "trip_destination_Station": instance.trip_id.destinationStation,
            "trip_destination_Time": instance.trip_id.destinationTime,
        }


class CitySerializer(serializers.ModelSerializer):
    Reviews = ReviewSerializer(many=True, read_only=False)
    companies = CompanySerializer(many=True, read_only=False)

    class Meta:
        model = City
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        