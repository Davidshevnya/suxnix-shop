from decimal import Decimal
from django.conf import settings
from shop.models import Good


class Cart(object):
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart


    def add(self, product, quantity, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = int(quantity)
        else:
            self.cart[product_id]['quantity'] += int(quantity)

        self.save()


    def remove(self, product):
    
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True



    def __iter__(self):
        product_ids = self.cart.keys()
        products = Good.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = {
                    'id': product.id,
                    'title': product.name,
                    'url': product.get_absolute_url(),
                    'image_url': product.image.url,


                    }

        for item in self.cart.values():
            
            item['total_price'] = str(Decimal(item['price']) * item['quantity'])
            
            yield item


    def __len__(self):
    #    return sum(i['quantity'] for i in self.cart.values())
        return len(self.cart)


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True




