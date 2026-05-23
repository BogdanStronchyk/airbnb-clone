from django.db import models
from django.conf import settings
from listings.models import ServiceListing

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(ServiceListing, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField()
    end_time = models.TimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    host_payout_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    denial_reason = models.TextField(blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='pending') # pending, succeeded, failed, refunded
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.username} - {self.listing.title} ({self.start_date})"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.PositiveSmallIntegerField() # 1-5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.booking.listing.title} by {self.reviewer.username}"
