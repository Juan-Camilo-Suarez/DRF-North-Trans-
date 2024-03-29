from rest_framework import serializers

from api.models import (
    ApplicationRegister,
    ApplicationsTransport,
    DriverProfile,
    ClientProfile,
    User,
    Car,
)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email", "role")


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = UserSerializer()


class ClientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        validated_data["user_id"] = validated_data["user_id"].id
        return super(ClientProfileSerializer, self).create(validated_data)

    class Meta:
        model = ClientProfile
        fields = ("city", "phone", "user", "user_id")


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ("id", "number", "model", "capacity", "photo")


class DriverProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    Car = CarSerializer()

    class Meta:
        model = DriverProfile
        fields = ("city", "phone", "Car", "user")


class ApplicationsTransportSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    client_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=ClientProfile.objects.all()
    )
    driver_profile_id = serializers.PrimaryKeyRelatedField(
        queryset=DriverProfile.objects.all()
    )

    def create(self, validated_data):
        validated_data["client_profile_id"] = validated_data["client_profile_id"].id
        validated_data["driver_profile_id"] = validated_data["driver_profile_id"].id
        return super(ApplicationsTransportSerializer, self).create(validated_data)

    class Meta:
        model = ApplicationsTransport
        fields = (
            # "client_profile",
            "client_profile_id",
            # "driver_profile",
            "driver_profile_id",
            "status",
            "create_at",
            "commentary",
            "photo",
            "invoice",
        )


class ApplicationsRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationRegister
        fields = ("id", "name", "city", "email", "phone", "user_position")
