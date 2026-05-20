from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceCategoryViewSet, ServiceListingViewSet, AvailabilityViewSet, 
    home_view, search_view, listing_detail, book_listing,
    host_dashboard, create_listing, edit_listing, toggle_listing_status,
    approve_booking, deny_booking
)

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet)
router.register(r'listings', ServiceListingViewSet)
router.register(r'availability', AvailabilityViewSet)

urlpatterns = [
    path('home/', home_view, name='home'),
    path('search/', search_view, name='search_page'),
    path('listing/<int:pk>/', listing_detail, name='listing_detail'),
    path('listing/<int:pk>/book/', book_listing, name='book_listing'),
    
    # Host URLs
    path('host/dashboard/', host_dashboard, name='host_dashboard'),
    path('host/create-listing/', create_listing, name='create_listing'),
    path('host/edit-listing/<int:pk>/', edit_listing, name='edit_listing'),
    path('host/toggle-listing/<int:pk>/', toggle_listing_status, name='toggle_listing_status'),
    path('host/booking/<int:pk>/approve/', approve_booking, name='approve_booking'),
    path('host/booking/<int:pk>/deny/', deny_booking, name='deny_booking'),
    
    path('', include(router.urls)),
]
