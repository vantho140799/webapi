from django.urls import path
from . import views  # Import các views tương ứng

urlpatterns = [
    path('social/', views.profile_view, name='profile'),
    ]