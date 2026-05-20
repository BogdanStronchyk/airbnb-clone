from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceCategoryViewSet, ServiceListingViewSet, AvailabilityViewSet, home_view, listing_detail, book_listing

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet)
router.register(r'listings', ServiceListingViewSet)
router.register(r'availability', AvailabilityViewSet)

urlpatterns = [
    path('home/', home_view, name='home'),
    path('listing/<int:pk>/', listing_detail, name='listing_detail'),
    path('listing/<int:pk>/book/', book_listing, name='book_listing'),
    path('', include(router.urls)),
]
