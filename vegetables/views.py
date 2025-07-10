from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .models import Category, Vegetable, Cart, CartItem, Order, OrderItem


def home(request):
    """Trang chủ hiển thị rau nổi bật và danh mục"""
    featured_vegetables = Vegetable.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.all()[:8]
    latest_vegetables = Vegetable.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    context = {
        'featured_vegetables': featured_vegetables,
        'categories': categories,
        'latest_vegetables': latest_vegetables,
    }
    return render(request, 'vegetables/home.html', context)


def vegetable_list(request):
    """Danh sách tất cả rau củ"""
    vegetables = Vegetable.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    # Lọc theo danh mục
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        vegetables = vegetables.filter(category=category)
    
    # Tìm kiếm
    search_query = request.GET.get('q')
    if search_query:
        vegetables = vegetables.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'vegetables': vegetables,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'vegetables/vegetable_list.html', context)


def vegetable_detail(request, slug):
    """Chi tiết rau củ"""
    vegetable = get_object_or_404(Vegetable, slug=slug, is_available=True)
    related_vegetables = Vegetable.objects.filter(
        category=vegetable.category, 
        is_available=True
    ).exclude(id=vegetable.id)[:4]
    
    context = {
        'vegetable': vegetable,
        'related_vegetables': related_vegetables,
    }
    return render(request, 'vegetables/vegetable_detail.html', context)


def category_detail(request, slug):
    """Chi tiết danh mục"""
    category = get_object_or_404(Category, slug=slug)
    vegetables = Vegetable.objects.filter(category=category, is_available=True)
    
    context = {
        'category': category,
        'vegetables': vegetables,
    }
    return render(request, 'vegetables/category_detail.html', context)


def get_cart(request):
    """Lấy hoặc tạo giỏ hàng"""
    if not request.session.session_key:
        request.session.create()
    
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_detail(request):
    """Chi tiết giỏ hàng"""
    cart = get_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'vegetables/cart.html', context)


@require_POST
def add_to_cart(request, vegetable_id):
    """Thêm rau vào giỏ hàng"""
    vegetable = get_object_or_404(Vegetable, id=vegetable_id, is_available=True)
    cart = get_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        vegetable=vegetable,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'Đã thêm {vegetable.name} vào giỏ hàng!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Đã thêm {vegetable.name} vào giỏ hàng!',
            'cart_total_items': cart.get_total_items()
        })
    
    return redirect('vegetables:cart_detail')


@require_POST
def update_cart_item(request, item_id):
    """Cập nhật số lượng sản phẩm trong giỏ hàng"""
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price())
        })
    
    return redirect('vegetables:cart_detail')


@require_POST
def remove_from_cart(request, item_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price())
        })
    
    return redirect('vegetables:cart_detail')


def checkout(request):
    """Trang thanh toán"""
    cart = get_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('vegetables:cart_detail')
    
    if request.method == 'POST':
        # Tạo đơn hàng
        order = Order.objects.create(
            customer_name=request.POST['customer_name'],
            customer_phone=request.POST['customer_phone'],
            customer_email=request.POST.get('customer_email', ''),
            delivery_address=request.POST['delivery_address'],
            total_amount=cart.get_total_price(),
            notes=request.POST.get('notes', '')
        )
        
        # Tạo các item trong đơn hàng
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                vegetable=cart_item.vegetable,
                quantity=cart_item.quantity,
                price=cart_item.vegetable.price
            )
        
        # Xóa giỏ hàng
        cart.items.all().delete()
        
        messages.success(request, f'Đặt hàng thành công! Mã đơn hàng: #{order.id}')
        return redirect('vegetables:order_success', order_id=order.id)
    
    context = {
        'cart': cart,
    }
    return render(request, 'vegetables/checkout.html', context)


def order_success(request, order_id):
    """Trang đặt hàng thành công"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
    }
    return render(request, 'vegetables/order_success.html', context)
