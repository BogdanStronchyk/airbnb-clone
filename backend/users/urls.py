from django.urls import path
from .views import login_view, register_view, logout_view, become_host, review_host, profile_view

urlpatterns = [
    path('login/', login_view, name='login_page'),
    path('register/', register_view, name='register_page'),
    path('logout/', logout_view, name='logout_page'),
    path('become-host/', become_host, name='become_host'),
    path('review-host/<int:host_id>/', review_host, name='review_host'),
    path('profile/<int:user_id>/', profile_view, name='profile_view'),
]
