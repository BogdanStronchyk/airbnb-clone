from rest_framework import serializers
from .models import Booking, Review
from listings.serializers import ServiceListingSerializer

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.ReadOnlyField(source='reviewer.username')

    class Meta:
        model = Review
        fields = ('id', 'booking', 'reviewer', 'reviewer_name', 'rating', 'comment', 'created_at')
        read_only_fields = ('id', 'reviewer', 'created_at')

class BookingSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    listing_details = ServiceListingSerializer(source='listing', read_only=True)
    review = ReviewSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'customer', 'customer_name', 'listing', 'listing_details',
            'start_date', 'end_date', 'start_time', 'end_time', 'total_price', 'status', 'review',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'customer', 'total_price', 'status', 'created_at', 'updated_at')
