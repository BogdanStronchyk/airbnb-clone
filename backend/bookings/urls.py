from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, ReviewViewSet, trips_view, add_review, stripe_webhook, cancel_booking

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('trips/', trips_view, name='trips'),
    path('review/<int:booking_id>/', add_review, name='add_review'),
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('', include(router.urls)),
]
