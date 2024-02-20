from shop.models import Good


class LatestProducts(object):
    def __init__(self, request):
        self.session = request.session
        
        latest_products = self.session.get("latest_products")
        if not latest_products:
            latest_products = self.session["latest_products"] = []
        
        self.latest_products = latest_products

        
    def add(self, product):
        if product.id not in [i['id'] for i in self.latest_products]:
            product = {"id": product.id, "title": product.name,
                       "url": product.get_absolute_url(),
                       "image_url": product.image.url,
                       "price": str(product.price)}
            if len(self.latest_products) >= 3:
                del self.latest_products[-1]

                self.latest_products.insert(0, product)

            else:
                self.latest_products.append(product)

            self.save()



    def save(self):
        self.session['latest_products'] = self.latest_products
        self.session.modified = True

    def get(self):
        return self.latest_products

    
