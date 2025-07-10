from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Hình ảnh")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Danh mục")
    description = models.TextField(verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá (VNĐ)")
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh")
    stock = models.IntegerField(default=0, verbose_name="Số lượng tồn kho")
    unit = models.CharField(max_length=20, default="kg", verbose_name="Đơn vị")
    is_available = models.BooleanField(default=True, verbose_name="Còn hàng")
    is_featured = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_price_display(self):
        return f"{self.price:,.0f} VNĐ/{self.unit}"
