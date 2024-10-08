from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name
class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class PricingPlan(models.Model):
    plan_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='pricing_plans', null=True)
    image = models.ImageField(upload_to='pictures/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='pricing_plans') 
    # group_id = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.plan_name
class Review(models.Model):
    product_name = models.CharField(max_length=255)  # Tên sản phẩm
    amazon_link = models.URLField()  # Liên kết sản phẩm Amazon
class PricingPlanFolder(models.Model):
    pricing_plan = models.OneToOneField(PricingPlan, on_delete=models.CASCADE, related_name='image_folder')
    folder_path = models.CharField(max_length=255)  # Lưu trữ đường dẫn của folder chứa hình ảnh

    def __str__(self):
        return f'Folder for {self.pricing_plan.plan_name}'
# class Support(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo

#     def __str__(self):
#         return self.name

    
