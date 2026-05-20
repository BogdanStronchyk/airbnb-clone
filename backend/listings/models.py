from django.db import models
from django.conf import settings

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True) # Icon name for frontend

    class Meta:
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name

class ServiceListing(models.Model):
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name='listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    PRICING_TYPE_CHOICES = [
        ('per_night', 'Per Night'),
        ('per_hour', 'Per Hour'),
        ('per_ride', 'Per Ride'),
        ('per_person', 'Per Person'),
        ('per_session', 'Per Session'),
        ('flat_rate', 'Flat Rate'),
    ]
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPE_CHOICES, default='per_night')
    currency = models.CharField(max_length=3, default='USD')
    images = models.JSONField(default=list, blank=True) # List of image URLs
    is_active = models.BooleanField(default=True)
    
    # Flexible attributes for regional/seasonal customization
    # e.g., {"difficulty": "expert", "season": "winter", "has_equipment_rental": true}
    specific_attributes = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Availability(models.Model):
    listing = models.ForeignKey(ServiceListing, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "Availabilities"
