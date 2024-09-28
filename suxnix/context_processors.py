from cart.cart import Cart


def cart(request):
    cart = Cart(request)

    return {
        'cart': list(cart),
        'cart_total_price': cart.get_total_price(),
        'cart_len': len(cart)
    }