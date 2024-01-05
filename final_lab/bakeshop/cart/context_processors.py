from .cart import Cart 

#create context processor so the cart can work all pages 
def cart(request): 
    #return the default data from the cart 
    return {'cart' : Cart(request)}