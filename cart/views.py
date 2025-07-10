from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product

def get_or_create_cart(request):
    """Lấy hoặc tạo giỏ hàng cho user hoặc session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def cart_view(request):
    """Hiển thị giỏ hàng"""
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)

@require_POST
def add_to_cart(request, product_id):
    """Thêm sản phẩm vào giỏ hàng"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
        message = f"Đã cập nhật số lượng {product.name} trong giỏ hàng"
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        message = f"Đã thêm {product.name} vào giỏ hàng"
    
    messages.success(request, message)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price())
        })
    
    return redirect('cart:cart_view')

@require_POST
def update_cart_item(request, item_id):
    """Cập nhật số lượng sản phẩm trong giỏ hàng"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Đã cập nhật số lượng {cart_item.product.name}")
    else:
        cart_item.delete()
        messages.success(request, f"Đã xóa {cart_item.product.name} khỏi giỏ hàng")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price())
        })
    
    return redirect('cart:cart_view')

def remove_from_cart(request, item_id):
    """Xóa sản phẩm khỏi giỏ hàng"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f"Đã xóa {product_name} khỏi giỏ hàng")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.get_total_items(),
            'cart_total_price': float(cart.get_total_price())
        })
    
    return redirect('cart:cart_view')
