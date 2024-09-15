from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'password', 'confirm_password']

   
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])  
        user.save()
         # إعشان لو ضفنا يوزر جديد يضيفه ف ال AllUsers
        all_users_entry = AllUsers.objects.create(
            user_type='user',  # Only specify the user_type
            email=user.email,
            name=user.name,
            phone_number=user.phone_number,
            password=user.password,  # Already hashed
            confirm_password=user.password
        )
        all_users_entry.save()
        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone_number', 'password', 'confirm_password', 'commercial_register', 'work_license', 'certificates','trip','bus']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords must match.")
        return data

   
    def create(self, validated_data):
        company = Company(
            commercial_register=validated_data['commercial_register'],
            work_license=validated_data['work_license'],
            certificates=validated_data['certificates'],
        )
        company.set_password(validated_data['password'])  # تشفير كلمة المرور
        company.save()
       
        all_users_entry = AllUsers.objects.create(
            user_type='company',
            email=company.email,
            name=company.name,
            phone_number=company.phone_number,
            password=company.password,  # Already hashed
            confirm_password=company.password  # This can be removed if not needed
        )
        all_users_entry.save()
        return company

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'comment', 'rate']
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance
    
    
    
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUsers
        fields = '__all__'

    
    
class userNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]
    
class TripSerializer(serializers.ModelSerializer):
    users=userNameSerializer(source="user_id" , many=True)
    class Meta:
        model = Trips
        fields = "__all__"

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
    class Meta:
        model = City
        fields = '__all__'