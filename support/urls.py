from django.urls import path
from .views import SupportPageView, SupportAPIView

urlpatterns = [
    path('', SupportPageView.as_view(), name='support_page'),  # cho web
    path('api/support/', SupportAPIView.as_view(), name='support_api'),  # cho API
]
