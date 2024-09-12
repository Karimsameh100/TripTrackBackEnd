# from rest_framework import serializers
# from .models import Company

# # class CompanySerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Company
# #         fields = ['name', 'email', 'phone_number', 'password', 'confirm_password', 'commercial_register', 'work_license', 'certificates']

# #     def validate(self, data):
# #         if data['password'] != data['confirm_password']:
# #             raise serializers.ValidationError("Passwords must match.")
# #         return data



# # from rest_framework import serializers
# # from .models import User

# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = ['name', 'phone_number', 'email', 'password', 'confirm_password']

# #     def validate(self, data):
# #         if data['password'] != data['confirm_password']:
# #             raise serializers.ValidationError("Passwords must match.")
# #         return data
# from rest_framework import serializers
# from .models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['name', 'phone_number', 'email', 'password', 'confirm_password']

#     # تأكد من أن كلمتي المرور متطابقتان
#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords must match.")
#         return data
    
    
# from rest_framework import serializers
# from .models import Company

# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = ['name', 'email', 'phone_number', 'password', 'confirm_password', 'commercial_register', 'work_license', 'certificates']

#     def validate(self, data):
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords must match.")
#         return data


#     # استخدام set_password لتشفير كلمة المرور
#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             name=validated_data['name'],
#             phone_number=validated_data['phone_number'],
#         )
#         user.set_password(validated_data['password'])  # تشفير كلمة المرور
#         user.save()
#         return user
# ==============================================






from rest_framework import serializers
from .models import User, Company


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
        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone_number', 'password', 'confirm_password', 'commercial_register', 'work_license', 'certificates']

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
        return company
