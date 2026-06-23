def cart_context(request):
    from main.views import get_cart_details
    details = get_cart_details(request)
    return {
        'cart_count': details['total_count'],
        'cart_total': details['total_amount']
    }
