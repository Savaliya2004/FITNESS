from .models import CartItem

def cart_count(request):
    if request.user.is_authenticated:
        total_count = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    else:
        cart = request.session.get('cart', {})
        total_count = sum(cart.values()) if cart else 0
    return {'cart_count': total_count}
