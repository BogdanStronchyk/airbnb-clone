from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from .models import ServiceCategory, ServiceListing, Availability
from bookings.models import Booking
from datetime import datetime
from .serializers import ServiceCategorySerializer, ServiceListingSerializer, AvailabilitySerializer

from django.db.models import Q

def home_view(request):
    categories = ServiceCategory.objects.all()
    listings = ServiceListing.objects.filter(is_active=True)
    
    category_id = request.GET.get('category')
    if category_id:
        listings = listings.filter(category_id=category_id)
        
    context = {
        'categories': categories,
        'listings': listings,
        'active_category': category_id
    }
    return render(request, 'listings/index.html', context)

def search_view(request):
    categories = ServiceCategory.objects.all()
    listings = ServiceListing.objects.filter(is_active=True)
    
    location_query = request.GET.get('location')
    date_query = request.GET.get('date') # Simplistic date search for MVP
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_id = request.GET.get('category')

    if location_query:
        listings = listings.filter(location__icontains=location_query)
        
    if category_id:
        listings = listings.filter(category_id=category_id)
        
    # Note: Proper date search requires checking Availability model, simplified here
    # For a real implementation, you'd filter out listings booked on that date
        
    if min_price:
        try:
            listings = listings.filter(base_price__gte=float(min_price))
        except ValueError:
            pass
            
    if max_price:
        try:
            listings = listings.filter(base_price__lte=float(max_price))
        except ValueError:
            pass
            
    context = {
        'categories': categories,
        'listings': listings,
        'active_category': category_id,
        'search_location': location_query,
        'search_min_price': min_price,
        'search_max_price': max_price,
    }
    return render(request, 'listings/search.html', context)

import json

def listing_detail(request, pk):
    listing = get_object_or_404(ServiceListing.objects.prefetch_related('bookings__review', 'bookings__customer'), pk=pk)
    # Get future confirmed bookings for this listing to show occupancy
    from django.utils import timezone
    occupied_periods = Booking.objects.filter(
        listing=listing, 
        status='confirmed', 
        end_date__gte=timezone.now().date()
    ).order_by('start_date')
    
    # Prepare disabled dates for Flatpickr
    disabled_dates = []
    for period in occupied_periods:
        disabled_dates.append({
            "from": period.start_date.strftime('%Y-%m-%d'),
            "to": period.end_date.strftime('%Y-%m-%d')
        })
    
    from django.conf import settings
    return render(request, 'listings/detail.html', {
        'listing': listing,
        'occupied_periods': occupied_periods,
        'disabled_dates_json': json.dumps(disabled_dates),
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

from django.db.models import Sum

@login_required(login_url='/api/users/login/')
def host_dashboard(request):
    if not request.user.is_provider:
        messages.error(request, "You must be a host to access this page.")
        return redirect('root_home')
        
    listings = ServiceListing.objects.filter(provider=request.user)
    upcoming_bookings = Booking.objects.filter(
        listing__in=listings, 
        end_date__gte=datetime.now().date()
    ).order_by('start_date')
    
    # Calculate earnings (completed or confirmed bookings)
    earnings = Booking.objects.filter(
        listing__in=listings,
        status__in=['completed', 'confirmed']
    ).aggregate(total=Sum('total_price'))['total'] or 0.00
    
    context = {
        'listings': listings,
        'upcoming_bookings': upcoming_bookings,
        'earnings': earnings
    }
    return render(request, 'listings/host_dashboard.html', context)

from django.core.files.storage import FileSystemStorage

@login_required(login_url='/api/users/login/')
def create_listing(request):
    if not request.user.is_provider:
        messages.error(request, "You must be a host to create a listing.")
        return redirect('root_home')
        
    categories = ServiceCategory.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        base_price = request.POST.get('base_price')
        pricing_type = request.POST.get('pricing_type', 'per_night')
        category_id = request.POST.get('category')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Handle images
        image_urls = []
        if request.FILES.getlist('images'):
            fs = FileSystemStorage()
            for image in request.FILES.getlist('images'):
                filename = fs.save(image.name, image)
                image_urls.append(fs.url(filename))
                
        # Handle specific attributes and parsing map values
        lat = float(latitude) if latitude else None
        lng = float(longitude) if longitude else None
        
        listing = ServiceListing.objects.create(
            provider=request.user,
            title=title,
            description=description,
            location=location,
            base_price=base_price,
            pricing_type=pricing_type,
            category_id=category_id,
            latitude=lat,
            longitude=lng,
            images=image_urls
        )
        messages.success(request, "Listing created successfully!")
        return redirect('host_dashboard')
        
    pricing_types = ServiceListing.PRICING_TYPE_CHOICES
    return render(request, 'listings/create_listing.html', {
        'categories': categories,
        'pricing_types': pricing_types
    })

@login_required(login_url='/api/users/login/')
def edit_listing(request, pk):
    listing = get_object_or_404(ServiceListing, pk=pk, provider=request.user)
    categories = ServiceCategory.objects.all()
    
    if request.method == 'POST':
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.location = request.POST.get('location')
        listing.base_price = request.POST.get('base_price')
        listing.pricing_type = request.POST.get('pricing_type', 'per_night')
        listing.category_id = request.POST.get('category')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        if latitude:
            listing.latitude = float(latitude)
        if longitude:
            listing.longitude = float(longitude)
        
        # Handle new images
        if request.FILES.getlist('images'):
            fs = FileSystemStorage()
            image_urls = list(listing.images) if isinstance(listing.images, list) else []
            for image in request.FILES.getlist('images'):
                filename = fs.save(image.name, image)
                image_urls.append(fs.url(filename))
            listing.images = image_urls
            
        listing.save()
        messages.success(request, "Listing updated successfully!")
        return redirect('host_dashboard')
        
    pricing_types = ServiceListing.PRICING_TYPE_CHOICES
    return render(request, 'listings/edit_listing.html', {
        'listing': listing, 
        'categories': categories,
        'pricing_types': pricing_types
    })

@login_required(login_url='/api/users/login/')
def toggle_listing_status(request, pk):
    if request.method == 'POST':
        listing = get_object_or_404(ServiceListing, pk=pk, provider=request.user)
        listing.is_active = not listing.is_active
        listing.save()
        status = "listed" if listing.is_active else "de-listed"
        messages.success(request, f"Listing successfully {status}.")
    return redirect('host_dashboard')

@login_required(login_url='/api/users/login/')
def approve_booking(request, pk):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=pk, listing__provider=request.user)
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, f"Booking for {booking.listing.title} has been approved.")
    return redirect('host_dashboard')

@login_required(login_url='/api/users/login/')
def deny_booking(request, pk):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, pk=pk, listing__provider=request.user)
        reason = request.POST.get('denial_reason', '')
        booking.status = 'cancelled'
        booking.denial_reason = reason
        booking.save()
        messages.success(request, f"Booking for {booking.listing.title} has been denied.")
    return redirect('host_dashboard')

@login_required(login_url='/api/users/login/')
def book_listing(request, pk):
    if request.method == 'POST':
        listing = get_object_or_404(ServiceListing, pk=pk)
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            start_time = datetime.strptime(start_time_str, '%H:%M').time() if start_time_str else None
            end_time = datetime.strptime(end_time_str, '%H:%M').time() if end_time_str else None
            
            num_days = (end_date - start_date).days
            if num_days < 0 or (num_days == 0 and not start_time and not end_time):
                messages.error(request, "Checkout date must be after check-in date.")
                return redirect('listing_detail', pk=pk)
                
            # Basic overlap check (can be improved for time slots)
            overlapping_bookings = Booking.objects.filter(
                listing=listing,
                status='confirmed',
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            if overlapping_bookings.exists():
                messages.error(request, "Sorry, those dates are already booked.")
                return redirect('listing_detail', pk=pk)
                
            # If same day, charge base_price once. Else per day.
            calc_days = num_days if num_days > 0 else 1
            total_price = listing.base_price * calc_days
            
            Booking.objects.create(
                customer=request.user,
                listing=listing,
                start_date=start_date,
                start_time=start_time,
                end_date=end_date,
                end_time=end_time,
                total_price=total_price
            )
            messages.success(request, "Booking requested successfully!")
            return redirect('listing_detail', pk=pk)
            
        except ValueError:
            messages.error(request, "Invalid dates or times provided.")
            return redirect('listing_detail', pk=pk)
            
    return redirect('listing_detail', pk=pk)


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [permissions.AllowAny]

class ServiceListingViewSet(viewsets.ModelViewSet):
    queryset = ServiceListing.objects.filter(is_active=True)
    serializer_class = ServiceListingSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(provider=self.request.user)

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(listing__provider=self.request.user)
