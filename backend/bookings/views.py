from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking, Review
from .serializers import BookingSerializer, ReviewSerializer

from django.utils import timezone
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
import certifi
stripe.verify_ssl_certs = True
stripe.ca_bundle_path = certifi.where()

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        try:
            booking = Booking.objects.get(stripe_payment_intent_id=payment_intent.id)
            booking.payment_status = 'succeeded'
            booking.status = 'confirmed'
            booking.save()
        except Booking.DoesNotExist:
            pass # Or log the error
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        try:
            booking = Booking.objects.get(stripe_payment_intent_id=payment_intent.id)
            booking.payment_status = 'failed'
            booking.status = 'cancelled'
            booking.save()
        except Booking.DoesNotExist:
            pass

    return HttpResponse(status=200)

@login_required(login_url='/api/users/login/')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if booking.status in ['cancelled', 'completed']:
        messages.error(request, f"Booking cannot be cancelled because its status is {booking.status}.")
        return redirect('trips')

    if booking.payment_status == 'succeeded':
        # Logic to refund based on cancellation policy
        refund_amount = booking.total_price  # Default: full refund
        cancellation_policy = booking.listing.cancellation_policy

        if cancellation_policy:
            days_before_start = (booking.start_date - timezone.now().date()).days
            if days_before_start <= cancellation_policy.days_before_start:
                refund_amount = booking.total_price * (cancellation_policy.refund_percentage / 100)

        # In a real scenario, make a call to Stripe API to process the refund here
        # stripe.Refund.create(payment_intent=booking.stripe_payment_intent_id, amount=int(refund_amount * 100))
        
        if refund_amount > 0:
            booking.payment_status = 'refunded' # or partially_refunded
        else:
             booking.payment_status = 'succeeded' # Keep as succeeded if no refund

    booking.status = 'cancelled'
    booking.save()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('trips')

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        listing = serializer.validated_data['listing']
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        num_days = (end_date - start_date).days
        
        # Simple validation
        if num_days <= 0:
             return Response({"error": "End date must be after start date"}, status=status.HTTP_400_BAD_REQUEST)
             
        total_price = listing.base_price * num_days
        
        # Calculate platform fee and host payout
        platform_fee_percentage = listing.platform_fee_percentage / 100
        platform_fee = total_price * platform_fee_percentage
        host_payout_amount = total_price - platform_fee
        
        try:
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100), # Stripe requires amount in cents
                currency='usd',
                metadata={'integration_check': 'accept_a_payment'},
            )
            
            # Save booking with intent ID
            booking = serializer.save(
                customer=self.request.user, 
                total_price=total_price,
                platform_fee=platform_fee,
                host_payout_amount=host_payout_amount,
                stripe_payment_intent_id=intent.id,
                payment_status='pending'
            )
            
            headers = self.get_success_headers(serializer.data)
            response_data = serializer.data
            response_data['client_secret'] = intent.client_secret
            
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
            
        except stripe.error.AuthenticationError as e:
            print(f"Stripe Authentication Error: {e}")
            return Response({'error': 'Stripe Authentication Failed. Please check your API keys.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Booking creation error: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
