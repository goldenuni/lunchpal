from rest_framework import serializers
from lunchpal.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'cuisine']


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'items', 'date', 'created_at', 'votes', 'price']
        read_only_fields = ['created_at', 'votes']

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)
