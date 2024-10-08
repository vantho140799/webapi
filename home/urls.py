# home/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountInfoView, CategoryViewSet, ItemViewSet, LoginPageView, PhotoViewerView, PricingPlanByCategoryViewSet, ReviewViewSet,   index, FeatureViewSet, PricingPlanViewSet, ProductDetailView, search_plans, subscribe_email
from .views import LoginView, RegisterView

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'pricing', PricingPlanViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'category/(?P<category_id>\d+)/pricing-plans', PricingPlanByCategoryViewSet, basename='pricing-plans-by-category')
urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginPageView.as_view(), name='login_page'),
    path('api/login/', LoginView.as_view(), name='login'),  # Endpoint đăng nhập
    path('api/register/', RegisterView.as_view(), name='register'),  # Endpoint đăng ký
    path('api/', include(router.urls)),  # Các endpoint khác
    path('api/product/<int:pricing_id>/', ProductDetailView.as_view(), name='product_detail_api'),
    path('product/<int:pricing_id>/', ProductDetailView.as_view(), name='product_detail'),
    path('account/', AccountInfoView.as_view(), name='account_info'),
    path('photo-viewer/', PhotoViewerView.as_view(), name='photo_viewer'),
    path('search/', search_plans, name='search_plans'),
    path('reviews/', ReviewViewSet.as_view({'get': 'review_list'}), name='review_list'),
    # path('subscribe/', subscribe_email, name='subscribe_email'),
    path('', subscribe_email, name='index'),  # Trang chủ sử dụng view `subscribe_email`
    path('subscribe/', subscribe_email, name='subscribe_email'),
]
