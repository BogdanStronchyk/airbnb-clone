from django.urls import path
from .views import inbox_view, conversation_view

urlpatterns = [
    path('', inbox_view, name='inbox'),
    path('<int:user_id>/', conversation_view, name='conversation'),
]
