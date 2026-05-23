from django.db import models
from django.conf import settings
from bookings.models import Booking

class CancellationPolicy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    days_before_start = models.IntegerField(help_text="Number of days before start date")
    refund_percentage = models.IntegerField(help_text="Percentage of refund (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.refund_percentage}% before {self.days_before_start} days"

class Payout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payout')
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_transfer_id = models.CharField(max_length=255, blank=True, null=True)
    payout_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payout for {self.booking.id} - {self.amount} ({self.status})"
