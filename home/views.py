import base64
import json
import os
from django.views import View
from rest_framework import viewsets
from .models import Category, Item, Feature, PricingPlan, PricingPlanFolder, Review
from .serializers import CategorySerializer, ItemSerializer, FeatureSerializer, PricingPlanSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from cryptography.fernet import Fernet
from .authentication import cipher
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth.decorators import login_required
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication]  # Bảo mật API bằng token
    # permission_classes = [IsAuthenticated]  # Chỉ cho phép người dùng đã xác thực

class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

class PricingPlanViewSet(viewsets.ModelViewSet):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['get'])
    def review_list(self, request):
        reviews = Review.objects.all()  # Lấy tất cả review từ database
        return render(request, 'pages/review.html', {'reviews': reviews})
    
def index(request):
    return render(request, 'pages/home.html')

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = cipher.encrypt(user.username.encode()).decode()
            return Response({'token': f'Bearer {token}'})
        return Response({'error': 'Invalid Credentials'}, status=400)

class RegisterView(APIView):
    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            token, created = Token.objects.get_or_create(user=user)
            encrypted_token = cipher.encrypt(token.key.encode()).decode()
            return Response({'token': f'Bearer {encrypted_token}'})
        return Response(form.errors, status=400)

class ProductDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, pricing_id):
        pricing_plan = get_object_or_404(PricingPlan, id=pricing_id)
        item = pricing_plan.item

        # Lấy các pricing plan cùng category
        similar_pricing_plans = PricingPlan.objects.filter(category=pricing_plan.category).exclude(id=pricing_id)

        # Lấy đường dẫn folder của pricing plan từ model PricingPlanFolder
        try:
            folder = pricing_plan.image_folder.folder_path  # Sử dụng folder_path từ PricingPlanFolder
        except PricingPlanFolder.DoesNotExist:
            folder = None 

        images = []
        if folder and os.path.exists(folder):  # Kiểm tra sự tồn tại của folder
            try:
                images = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
            except PermissionError:
                images = []

        # Truyền dữ liệu sang template
        return render(request, 'pages/product_detail.html', {
            'item': item,
            'pricing_plan': pricing_plan,
            'images': images,
            'folder_path': folder,  # Truyền folder_path sang template
            'similar_pricing_plans': similar_pricing_plans  # Thêm danh sách pricing plans tương tự
        })

# @login_required
# def account_info(request):
#     user = request.user  # Get the logged-in user
#     return render(request, 'page/account_info.html', {
#         'username': user.username,
#         'email': user.email,
#     })
class LoginPageView(View):
    def get(self, request):
        return render(request, 'pages/login.html') 
class AccountInfoView(APIView):
    def get(self, request):
        # Không cần kiểm tra xác thực
        token = request.GET.get('token', None)
        return render(request, 'pages/account_info.html', {
            'token': token, 
        })

class PricingPlanByCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = PricingPlanSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return PricingPlan.objects.filter(category_id=category_id)

    @action(detail=True, methods=['get'])
    def pricing_plans(self, request, category_id=None):
        pricing_plans = self.get_queryset()
        serializer = self.get_serializer(pricing_plans, many=True)
        return Response(serializer.data)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PhotoViewerView(TemplateView):
    template_name = 'pages/photo_viewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pricing_plan_id = self.request.GET.get('id')
        
        # Lấy folder_path từ PricingPlanFolder
        pricing_plan_folder = get_object_or_404(PricingPlanFolder, pricing_plan_id=pricing_plan_id)
        folder_path = pricing_plan_folder.folder_path
        
        image_name = self.request.GET.get('image')
        current_image_path = None 
        images = [] 

        if folder_path and os.path.exists(folder_path):
            images = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

            # Gán đường dẫn đến hình ảnh hiện tại
            if image_name in images:
                current_image_path = f'/static/{folder_path}/{image_name}'  # Thay đổi theo folder_path
            else:
                current_image_path = '/static/pictures/default.jpg'  # Ảnh mặc định

        # Truyền folder_path và hình ảnh hiện tại vào context
        context['folder_path'] = folder_path 
        context['current_image'] = current_image_path if current_image_path else '/static/pictures/default.jpg'
        context['images'] = [f'/static/{folder_path}/{image}' for image in images]  # Render danh sách hình ảnh
        return context

def search_plans(request):
    query = request.GET.get('plan_name', '')  # Lấy giá trị từ ô nhập 'plan_name'
    results = PricingPlan.objects.filter(plan_name__icontains=query)  # Tìm kiếm không phân biệt chữ hoa

    return render(request, 'pages/home.html', {'pricing_plans': results})

