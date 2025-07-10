from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category

def home(request):
    """Trang chủ hiển thị sản phẩm nổi bật"""
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.all()[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)

def product_list(request):
    """Danh sách tất cả sản phẩm"""
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Lọc theo danh mục
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Tìm kiếm
    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)
    
    # Phân trang
    paginator = Paginator(products, 12)  # 12 sản phẩm mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_id,
        'search_query': search,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, product_id):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_available=True
    ).exclude(id=product_id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

def category_detail(request, category_id):
    """Sản phẩm theo danh mục"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, is_available=True)
    
    # Phân trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'products/category_detail.html', context)
