from django.db import models
from django.db.models import Sum
from api.models import CustomUser

# Create your models here.

class ImageUploded(models.Model):
    image = models.ImageField(upload_to="product_image", null=True, blank=True)
    image = models.URLField()

class Product(models.Model):
    ITEM_CONDITION_CHOICES = (
        ("LIKE_NEW","Like New"),
        ("EXCELLENT","Excellen"),
        ("GOOD","Good"),
        ("FAIR","Fair"),
        ("POOR","Poor")
    )


    CONFIDENCE_CHOICES = (
        ("HIGH","High"),
        ("LOW","Low"),
        ("MEDIUM","Medium")

    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_owner')
    item_name = models.CharField(max_length=150)
    descirption = models.TextField()
    item_collection = models.CharField(max_length=25, choices=ITEM_CONDITION_CHOICES, default="GOOD" )
    defects = models.TextField()
    estimated_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_price_range = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_price_range = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Confidence = models.CharField(max_length=25, choices=CONFIDENCE_CHOICES, default="MEDIUM")
    dalivary_status = models.BooleanField(default=False)
    images = models.ManyToManyField(ImageUploded, related_name="item_images", null=True,blank=True)

    @classmethod
    def get_user_total_estimated_value(cls, user):
        total = cls.objects.filter(user=user).aggregate(total=Sum('estimated_value'))['total'] or 0
        return total
    
    def __str__(self):
        return self.item_name + " " + self.user.email
    
    
class SellerContactInfo(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    pickup_date = models.DateTimeField()
    pickup_address = models.TextField()
    products = models.ManyToManyField(Product, related_name="products_list", null=True, blank=True)
    privecy_policy_status = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " " + self.phone
