from shop.models import Product

class Cart(): 
    def __init__(self, request): 
        self.session = request.session 

        #get the current session key if it is exist
        cart = self.session.get('session_key')

        #if the user is new, no sk! create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} 

        #make sure cart is available in all pages
        self.cart = cart 
    
    def add(self, product, quantity): 
        product_id = str(product.id)
        product_qty = str(quantity)

        #logic
        if product_id in self.cart: 
            pass

        else: 
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True
    
    def cart_total(self): 
        #get prod IDS
        product_ids = self.cart.keys()
        #lookup those keys in prods database mod
        products = Product.objects.filter(id__in=product_ids)
        #get qty
        quantities = self.cart
        #starting counting at 0
        total = 0
        for key, value in quantities.items(): 
            #convert key str into int
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else: 
                        total = total + (product.price * value)

        return total



    def __len__(self):
        return len(self.cart)

    def get_prods(self): 
        #Get ids from cart
        product_ids = self.cart.keys()
        #Use ids to lookup prods in database model
        products = Product.objects.filter(id__in=product_ids)
        #Return those lookup prods
        return products

    def get_quants(self): 
        quantities = self.cart 
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #get cart
        ourcart = self.cart 

        #update dict
        ourcart[product_id] = product_qty

        self.session.modified = True 

        thing = self.cart
        return thing
    
    def delete(self, product): 
        product_id = str(product)
        #Delete from dict
        if product_id in self.cart: 
            del self.cart[product_id]

        self.session.modified = True