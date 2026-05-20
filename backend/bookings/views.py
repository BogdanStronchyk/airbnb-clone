from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer

from django.utils import timezone

@login_required(login_url='/api/users/login/')
def trips_view(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-start_date')
    return render(request, 'bookings/trips.html', {'bookings': bookings, 'now': timezone.now()})

@login_required(login_url='/api/users/login/')
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    # Check if review already exists
    if hasattr(booking, 'review'):
        messages.error(request, "You have already reviewed this booking.")
        return redirect('trips')
        
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    Review.objects.create(
                        booking=booking,
                        reviewer=request.user,
                        rating=rating,
                        comment=comment
                    )
                    messages.success(request, "Review added successfully!")
                    return redirect('listing_detail', pk=booking.listing.id)
                else:
                    messages.error(request, "Rating must be between 1 and 5.")
            except ValueError:
                messages.error(request, "Invalid rating.")
        else:
            messages.error(request, "Please provide both rating and comment.")
            
    return render(request, 'bookings/add_review.html', {'booking': booking})


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_provider:
            return Booking.objects.filter(listing__provider=user)
        return Booking.objects.filter(customer=user)

    def perform_create(self, serializer):
        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        num_days = (end_date - start_date).days
        total_price = listing.base_price * num_days
        serializer.save(customer=self.request.user, total_price=total_price)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
