from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return {'cart': cart }