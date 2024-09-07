from decimal import Decimal
from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('CART', None)
        if cart is None:
            cart = self.session['CART'] = {}
        self.cart = cart
        
        
    def add(self, product, quantity=1, override_quantity=False):
        """
        A method to add a product to cart
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'image':str(product.image.first()), 'quantity': 0}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        self.save()
        
        
    def save(self):
        self.session.modified = True
        
    def remove(self, product):
        """
        A method to remove a product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    
    def __iter__(self):
        """
        A method to iterate the cart items
        """
        product_ids = self.cart.keys()
        
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        print("this is the original cart before override", cart)
        
        
        for product in products:
            cart[str(product.id)]['product'] = product
            print("this is cart after override",cart)
            print(product)
            
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])    
            
            item['total_price'] = item['price'] * item['quantity']
            print("this is the item", item['total_price'], item)
            
            yield item
            
    def get_total_price(self):
        return sum(item['total_price'] for item in self.cart.values())
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())   
    
    def clear(self):
        del self.session['CART']
        self.save()
    
    
            
            
                
        
            
        
        
                
                    
                