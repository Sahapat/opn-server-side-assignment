from domain.model import Product, Customer
from service.cart import Cart
from service.memory import memoryDbDefault

def main():
    #   Mocking data
    nike_product = Product.create(name='nike air jordan', price=1300.00)
    addidas_product = Product.create(name='Addias Ember', price=2000.50)
    memoryDbDefault.product[nike_product.id] = nike_product
    memoryDbDefault.product[addidas_product.id] = addidas_product

    user1_customer = Customer.create(name='user1')
    memoryDbDefault.customer[user1_customer.id] = user1_customer

    #   Main program
    cart = Cart.create(customer_id=user1_customer.id)
    cart.add(nike_product.id, 2)

    print(cart.is_empty())

if __name__ == '__main__':
    main()