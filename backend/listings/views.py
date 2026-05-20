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

def listing_detail(request, pk):
    listing = get_object_or_404(ServiceListing, pk=pk)
    return render(request, 'listings/detail.html', {'listing': listing})

@login_required(login_url='/api/users/login/')
def book_listing(request, pk):
    if request.method == 'POST':
        listing = get_object_or_404(ServiceListing, pk=pk)
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            num_days = (end_date - start_date).days
            if num_days <= 0:
                messages.error(request, "Checkout date must be after check-in date.")
                return redirect('listing_detail', pk=pk)
                
            total_price = listing.base_price * num_days
            
            Booking.objects.create(
                customer=request.user,
                listing=listing,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price
            )
            messages.success(request, "Booking requested successfully!")
            return redirect('listing_detail', pk=pk)
            
        except ValueError:
            messages.error(request, "Invalid dates provided.")
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
