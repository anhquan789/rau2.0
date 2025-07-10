// Main JavaScript for Vegetable Store

document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart count
    updateCartCount();
    
    // Handle add to cart forms
    handleAddToCartForms();
    
    // Handle smooth scrolling
    initSmoothScrolling();
    
    // Handle mobile menu
    initMobileMenu();
});

// Update cart count in navbar
function updateCartCount() {
    // This would be implemented with AJAX to get real cart count
    // For now, we'll use a placeholder
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        // Get cart count from session or localStorage
        const cartCount = getCartCount();
        cartCountElement.textContent = cartCount;
        
        if (cartCount > 0) {
            cartCountElement.style.display = 'inline';
        } else {
            cartCountElement.style.display = 'none';
        }
    }
}

// Get cart count from localStorage or session
function getCartCount() {
    // This is a placeholder - in reality you'd get this from the server
    return localStorage.getItem('cart_count') || 0;
}

// Handle add to cart forms with AJAX
function handleAddToCartForms() {
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            
            // Show loading state
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang thêm...';
            submitButton.disabled = true;
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message
                    showToast('success', data.message);
                    
                    // Update cart count
                    updateCartCountFromResponse(data.cart_total_items);
                    
                    // Reset button
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                } else {
                    showToast('error', 'Có lỗi xảy ra. Vui lòng thử lại.');
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('error', 'Có lỗi xảy ra. Vui lòng thử lại.');
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            });
        });
    });
}

// Update cart count from AJAX response
function updateCartCountFromResponse(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
        if (count > 0) {
            cartCountElement.style.display = 'inline';
        } else {
            cartCountElement.style.display = 'none';
        }
        
        // Store in localStorage
        localStorage.setItem('cart_count', count);
    }
}

// Show toast notifications
function showToast(type, message) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show toast-notification`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 400px;
    `;
    
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 3000);
}

// Initialize smooth scrolling
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize mobile menu behavior
function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                        toggle: false
                    });
                    bsCollapse.hide();
                }
            });
        });
    }
}

// Search functionality
function initSearch() {
    const searchForm = document.querySelector('form[action*="product_list"]');
    const searchInput = searchForm?.querySelector('input[name="search"]');
    
    if (searchInput) {
        // Add search suggestions (placeholder for future implementation)
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            if (query.length > 2) {
                // Here you could implement search suggestions
                console.log('Searching for:', query);
            }
        });
    }
}

// Quantity controls for product detail page
function initQuantityControls() {
    const quantityInputs = document.querySelectorAll('input[type="number"]');
    
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || 999;
            let value = parseInt(this.value);
            
            if (value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
    });
}

// Image lazy loading
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

// Utility function to show loading spinner
function showLoading(element) {
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang tải...';
    element.disabled = true;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initSearch();
    initQuantityControls();
    initLazyLoading();
});
