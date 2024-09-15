from rest_framework import serializers
from .models import *
from .models import User, Company,Trips,Bus,Booking


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
            user=user,
            user_type='user' 
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
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            commercial_register=validated_data['commercial_register'],
            work_license=validated_data['work_license'],
            certificates=validated_data['certificates'],
        )
        company.set_password(validated_data['password'])  # تشفير كلمة المرور
        company.save()
       
        all_users_entry = AllUsers.objects.create(
            company=company,
            user_type='company' 
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
    
    
    
    
    from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUsers
        fields = '__all__'

    
    
    
    
# ---trips and passenger and schedule

# class PassengerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Passenger
#         fields= ['id','user_name','phone','city','street','SSN','email']

# class PassengerNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Passenger
#         fields = ['user_name']       
        
# class TripSerializer(serializers.ModelSerializer):
#     passengers = PassengerNameSerializer(source='passenger_id', many=True)  # Show only user_name

#     class Meta:
#         model = Trip
#         fields = ['date', 'avilable_places', 'departure_station', 'stop_stations', 'departure_time', 'stop_time', 'price', 'status', 'passengers']

# class SchedualSerializer(serializers.ModelSerializer):
#     passenger_name =  serializers.SerializerMethodField()
#     trip_status =  serializers.SerializerMethodField()
#     class Meta:
#         model = Schedual
#         fields = ['id','passenger_name', 'trip_status'] 

#     def get_passenger_Name(self, obj):
#         return obj.passenger_id.user_name if obj.passenger_id else None 
    
#     def get_trip_status(self, obj):
#         return obj.trip_id.status if obj.trip_id else None 

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
