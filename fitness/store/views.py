from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Product, Order, OrderItem, CartItem, Wishlist, MembershipPlan, Payment, Coupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json
import hmac
import hashlib

def store_home(request):
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    
    if category:
        products = Product.objects.filter(category=category)
    elif subcategory:
        products = Product.objects.filter(subcategory=subcategory)
    else:
        products = Product.objects.all()
    
    trending = Product.objects.order_by('-views', '-rating')[:6]
    best_sellers = Product.objects.order_by('-order_count')[:6]
    budget_friendly = Product.objects.filter(discount_price__isnull=False).order_by('price')[:6]
    featured = Product.objects.filter(featured=True)[:6]

    context = {
        'products': products,
        'trending': trending,
        'best_sellers': best_sellers,
        'budget_friendly': budget_friendly,
        'featured': featured,
        'categories': Product.CATEGORIES,
        'current_cat': category,
        'current_sub': subcategory
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        items = []
        total = 0
        for item in cart_items:
            subtotal = (item.product.discount_price if item.product.discount_price else item.product.price) * item.quantity
            total += subtotal
            items.append({
                'product': item.product,
                'quantity': item.quantity,
                'subtotal': subtotal,
                'id': item.id
            })
    else:
        # Fallback to session for guests
        cart_data = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart_data.keys())
        items = []
        total = 0
        for product in products:
            qty = cart_data[str(product.id)]
            subtotal = (product.discount_price if product.discount_price else product.price) * qty
            total += subtotal
            items.append({
                'product': product,
                'quantity': qty,
                'subtotal': subtotal
            })

    tax = round(float(total) * 0.18)
    
    # Check session for applied coupon
    applied_coupon_code = request.session.get('applied_coupon')
    discount_amount = 0
    discount_percent = 0
    if applied_coupon_code:
        try:
            coupon = Coupon.objects.get(code=applied_coupon_code, active=True)
            if coupon.used_count < coupon.usage_limit:
                discount_percent = coupon.discount_percent
                discount_amount = (float(total) * discount_percent) / 100
        except Coupon.DoesNotExist:
            request.session.pop('applied_coupon', None)

    total_with_tax = float(total) + tax - discount_amount
    available_coupons = Coupon.objects.filter(active=True)[:5]
    
    return render(request, 'store/cart.html', {
        'items': items, 
        'total': total,
        'tax': tax,
        'total_with_tax': total_with_tax,
        'available_coupons': available_coupons,
        'applied_coupon': applied_coupon_code,
        'discount_amount': discount_amount,
        'discount_percent': discount_percent
    })

@login_required
def coupons_list(request):
    available_coupons = Coupon.objects.filter(active=True)
    return render(request, 'store/coupons.html', {'available_coupons': available_coupons})

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('store')
        
    total = 0
    items = []
    for item in cart_items:
        subtotal = (item.product.discount_price if item.product.discount_price else item.product.price) * item.quantity
        total += subtotal
        items.append({
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })
    
    tax = round(float(total) * 0.18)
    
    # Session Coupon logic for Checkout
    applied_coupon_code = request.session.get('applied_coupon')
    discount_amount = 0
    if applied_coupon_code:
        try:
            coupon = Coupon.objects.get(code=applied_coupon_code, active=True)
            if coupon.used_count < coupon.usage_limit:
                discount_amount = (float(total) * coupon.discount_percent) / 100
        except Coupon.DoesNotExist:
            request.session.pop('applied_coupon', None)

    total_with_tax = float(total) + tax - discount_amount
    
    return render(request, 'store/checkout.html', {
        'items': items,
        'total': total,
        'tax': tax,
        'total_with_tax': total_with_tax,
        'applied_coupon': applied_coupon_code,
        'discount_amount': discount_amount
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            item.quantity += 1
            item.save()
        cart_count = sum(i.quantity for i in CartItem.objects.filter(user=request.user))
    else:
        cart_data = request.session.get('cart', {})
        cart_data[str(product_id)] = cart_data.get(str(product_id), 0) + 1
        request.session['cart'] = cart_data
        cart_count = sum(cart_data.values())

    msg = "Product added to cart successfully! 🛒"
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': msg, 'cart_count': cart_count})
    
    messages.success(request, msg)
    return redirect('store')

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product_id=product_id).delete()
        cart_count = sum(i.quantity for i in CartItem.objects.filter(user=request.user))
    else:
        cart_data = request.session.get('cart', {})
        if str(product_id) in cart_data:
            del cart_data[str(product_id)]
            request.session['cart'] = cart_data
        cart_count = sum(cart_data.values())

    msg = "Product removed from cart."
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': msg, 'cart_count': cart_count})
        
    messages.success(request, msg)
    return redirect('cart')

def update_cart(request, product_id):
    action = request.POST.get('action')
    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
        if action == 'increment':
            item.quantity += 1
            item.save()
        elif action == 'decrement':
            item.quantity -= 1
            if item.quantity < 1:
                item.delete()
            else:
                item.save()
        cart_count = sum(i.quantity for i in CartItem.objects.filter(user=request.user))
        item_qty = item.quantity if item.id else 0
    else:
        cart_data = request.session.get('cart', {})
        if str(product_id) in cart_data:
            if action == 'increment':
                cart_data[str(product_id)] += 1
            elif action == 'decrement':
                cart_data[str(product_id)] -= 1
                if cart_data[str(product_id)] < 1:
                    del cart_data[str(product_id)]
            request.session['cart'] = cart_data
        cart_count = sum(cart_data.values())
        item_qty = cart_data.get(str(product_id), 0)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'cart_count': cart_count, 'item_qty': item_qty})
    return redirect('cart')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    _, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    msg = "Product added to wishlist." if created else "Product already in wishlist."
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': msg})
    messages.success(request, msg)
    return redirect('store')

@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, "Product removed from wishlist.")
    return redirect('wishlist')

def order_success(request):
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    if 'cart' in request.session:
        del request.session['cart']
    return render(request, 'store/order-success.html')


# ─── Membership & Razorpay Payment Views ────────────────────────────────────

MEMBERSHIP_PRICES = {
    'premium': 99900,   # in paise (₹999)
    'elite': 199900,    # in paise (₹1999)
}

@login_required
def membership_page(request):
    """Old membership page redirected to index sections."""
    return redirect('/#membership-plans')


@login_required
def buy_membership(request, pk):
    plan = get_object_or_404(MembershipPlan, pk=pk)
    return render(request, 'store/buy_membership.html', {
        'plan': plan,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

@login_required
def create_razorpay_order(request):
    """Create a Razorpay order and return order_id + key to frontend."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    plan_id = request.POST.get('plan_id')
    if not plan_id:
        return JsonResponse({'error': 'Plan ID is required'}, status=400)
    
    plan = get_object_or_404(MembershipPlan, id=plan_id)
    amount_paise = int(plan.price * 100)

    # Bypass Razorpay call if using placeholder keys
    if settings.RAZORPAY_KEY_ID == 'rzp_test_YourKeyId':
        mock_order_id = f"mock_{request.user.id}_{plan.id}"
        Payment.objects.create(
            user=request.user,
            razorpay_order_id=mock_order_id,
            amount=plan.price,
            plan=plan.name,
            membership=plan,
            status='created',
        )
        return JsonResponse({
            'order_id': mock_order_id,
            'amount': amount_paise,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID,
            'name': request.user.username,
            'email': request.user.email,
            'plan_name': plan.name,
            'is_mock': True
        })

    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_data = {
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
            'notes': {
                'user_id': str(request.user.id),
                'plan_id': str(plan.id),
            }
        }
        razorpay_order = client.order.create(data=order_data)

        # Save payment record with status=created
        payment = Payment.objects.create(
            user=request.user,
            razorpay_order_id=razorpay_order['id'],
            amount=plan.price,
            plan=plan.name,
            membership=plan,
            status='created',
        )

        return JsonResponse({
            'order_id': razorpay_order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID,
            'name': request.user.username,
            'email': request.user.email,
            'plan_name': plan.name,
            'is_mock': False
        })
    except Exception as e:
        import logging
        logging.getLogger('fitx.payments').error(f"Razorpay order creation failed: {e}")
        return JsonResponse({'error': "Payment Gateway configuration error. Please update Razorpay keys in settings.", 'details': str(e)}, status=500)


@csrf_exempt
@login_required
def payment_success(request):
    """Verify Razorpay signature and update payment + membership."""
    if request.method != 'POST':
        return redirect('membership')

    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')

    import logging
    logger = logging.getLogger('fitx.payments')
    logger.info(f"Payment callback: order={razorpay_order_id}, payment={razorpay_payment_id}")

    payment = Payment.objects.filter(razorpay_order_id=razorpay_order_id, user=request.user).first()

    is_valid = False
    if settings.RAZORPAY_KEY_ID == 'rzp_test_YourKeyId' and str(razorpay_order_id).startswith('mock_'):
        is_valid = True
    else:
        # Verify signature
        key_secret = settings.RAZORPAY_KEY_SECRET.encode('utf-8')
        msg = f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8')
        expected_sig = hmac.HMAC(key_secret, msg, hashlib.sha256).hexdigest()
        is_valid = hmac.compare_digest(expected_sig, razorpay_signature)

    if is_valid:
        # Signature valid → mark success
        if payment:
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'success'
            payment.save()
            # Upgrade user membership
            # Use SubscriptionService for proper lifecycle management
            try:
                from .services import SubscriptionService
                if payment.membership:
                    SubscriptionService.activate_subscription(request.user, payment.membership, payment)
                else:
                    request.user.membership_type = payment.plan
                    request.user.save()
            except Exception:
                request.user.membership_type = payment.membership.plan_type if payment.membership else payment.plan
                request.user.save()
            logger.info(f"Payment SUCCESS — user={request.user.username} upgraded to {request.user.membership_type}")

        messages.success(request, '🎉 Payment successful! Your membership has been upgraded.')
        return redirect('payment_complete')
    else:
        if payment:
            payment.status = 'failed'
            payment.save()
        print(f"[Payment] SIGNATURE MISMATCH for order={razorpay_order_id}")
        messages.error(request, '⚠️ Payment verification failed. Please contact support.')
        return redirect('payment_failed')


@login_required
def payment_complete(request):
    """Payment success landing page."""
    latest = Payment.objects.filter(user=request.user, status='success').order_by('-created_at').first()
    return render(request, 'store/payment_complete.html', {'payment': latest})


@login_required
def payment_failed(request):
    """Payment failure landing page."""
    return render(request, 'store/payment_failed.html')


@login_required
def my_orders(request):
    """Display user's orders with status tracking."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'status_colors': {
            'pending': '#FFA500',      # Orange
            'shipped': '#3498DB',      # Blue
            'delivered': '#27AE60',    # Green
            'cancelled': '#E74C3C',    # Red
        }
    }
    return render(request, 'store/my_orders.html', context)

@login_required
def apply_coupon(request):
    """API endpoint to validate and apply a coupon."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed.'}, status=405)
    
    code = request.POST.get('coupon_code', '').upper().strip()
    try:
        coupon = Coupon.objects.get(code=code, active=True)
        if coupon.used_count >= coupon.usage_limit:
            return JsonResponse({'status': 'error', 'message': 'Coupon limit reached.'})
        
        # Save to session
        request.session['applied_coupon'] = code
        
        return JsonResponse({
            'status': 'success', 
            'message': f'Coupon {code} applied successfully!',
            'discount_percent': coupon.discount_percent
        })
    except Coupon.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid coupon code.'})

@login_required
def place_order(request):
    """Process the checkout and create a real Order."""
    if request.method != 'POST':
        return redirect('checkout')
    
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)

    try:
        # Get POST data
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        coupon_code = request.POST.get('coupon_code', '').upper().strip()
        
        # Calculate subtotal
        subtotal = 0
        for item in cart_items:
            price = item.product.discount_price if item.product.discount_price else item.product.price
            subtotal += price * item.quantity
        
        # Calculate Discount
        discount_amount = Decimal('0')
        coupon_obj = None
        if coupon_code:
            try:
                coupon_obj = Coupon.objects.get(code=coupon_code, active=True)
                if coupon_obj.used_count < coupon_obj.usage_limit:
                    discount_amount = (subtotal * Decimal(str(coupon_obj.discount_percent))) / Decimal('100')
                    coupon_obj.used_count += 1
                    coupon_obj.save()
            except Coupon.DoesNotExist:
                pass

        tax = subtotal * Decimal('0.18')
        final_total = subtotal + tax - discount_amount

        # Create the Order
        order = Order.objects.create(
            user=request.user,
            final_price=final_total,
            discount=discount_amount,
            coupon=coupon_obj,
            status='pending'
        )

        # Create OrderItems
        for item in cart_items:
            price = item.product.discount_price if item.product.discount_price else item.product.price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=price
            )

        # Clear cart and coupon session
        cart_items.delete()
        request.session.pop('applied_coupon', None)
        
        return JsonResponse({'status': 'success', 'order_id': order.id})
    except Exception as e:
        import logging
        logging.getLogger('django').error(f"Order placement failed: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
