from rest_framework import serializers
from .models import ServiceCategory, ServiceListing, Availability

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'

class ServiceListingSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    provider_name = serializers.ReadOnlyField(source='provider.username')
    availability = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = ServiceListing
        fields = (
            'id', 'provider', 'provider_name', 'category', 'category_name', 
            'title', 'description', 'location', 'base_price', 'currency', 
            'images', 'is_active', 'specific_attributes', 'availability',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'provider', 'created_at', 'updated_at')
