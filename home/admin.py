from django.contrib import admin
from .models import Category,  PricingPlan, Review, PricingPlanFolder

# Đăng ký mô hình vào admin
admin.site.register(Category)
# admin.site.register(Item)
# admin.site.register(Feature)
admin.site.register(PricingPlan)
admin.site.register(Review)
admin.site.register(PricingPlanFolder)
