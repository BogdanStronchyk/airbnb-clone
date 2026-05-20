from django.contrib import admin
from django.urls import path, include
from listings.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='root_home'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/services/', include('listings.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('messages/', include('messaging.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
