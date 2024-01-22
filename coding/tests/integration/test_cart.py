import unittest
from unittest.mock import Mock
from domain.model import Product, Customer
from service.cart import (
    Cart,
    MemoryDb,
    ProductNotFound,
    CustomerNotFound
)

class TestCart(unittest.TestCase):
    def setUp(self):
        # Mocking the dependencies
        nike_product = Product.create(name='nike air jordan', price=1300.00)
        addidas_product = Product.create(name='Addias Ember', price=2000.50)
        user1_customer = Customer.create(name='user1')

        self.customer_ids = [user1_customer.id]
        self.product_ids = [nike_product.id, addidas_product.id]

        self.mock_memory_db = MemoryDb()
        self.mock_memory_db.product[nike_product.id] = nike_product
        self.mock_memory_db.product[addidas_product.id] = addidas_product
        self.mock_memory_db.customer[user1_customer.id] = user1_customer
    
    def get_default_cart(self):
        return Cart.create(self.customer_ids[0], db=self.mock_memory_db)

    def test_create_cart_normal(self):
        customer_id = self.customer_ids[0]

        # Act
        cart = Cart.create(customer_id, db=self.mock_memory_db)

        # Assert
        self.assertIsInstance(cart, Cart)
        self.assertEqual(cart.cart.customer_id, customer_id)
        self.assertEqual(len(cart.cart.cart_products), 0)
        self.assertEqual(len(cart.cart.promotions), 0)
        self.assertIn(cart.cart.id, self.mock_memory_db.cart)

    def test_create_cart_raise(self):
        customer_id = 'abc'

        with self.assertRaises(CustomerNotFound) as context:
            # Act
            Cart.create(customer_id, db=self.mock_memory_db)

    def test_cart_add(self):
        cart = self.get_default_cart()

        # Act
        product_id = self.product_ids[0]
        cart.add(product_id=self.product_ids[0], quantity=5)
        
        cart_product = list(filter(lambda c: c.product_id == product_id, cart.cart.cart_products))
        self.assertEqual(len(cart_product), 1)
        self.assertEqual(cart_product[0].quantity, 5)

    def test_cart_update(self):
        cart = self.get_default_cart()

        # Act
        product1_id = self.product_ids[0]
        product2_id = self.product_ids[1]
        cart.add(product_id=product1_id, quantity=5)
        cart.add(product_id=product2_id, quantity=3)
        cart.update(product_id=product1_id, quantity=3)

        cart_product1 = list(filter(lambda c: c.product_id == product1_id, cart.cart.cart_products))
        cart_product2 = list(filter(lambda c: c.product_id == product1_id, cart.cart.cart_products))
        
        self.assertEqual(len(cart_product1), 1)
        self.assertEqual(cart_product1[0].quantity, 3)
        self.assertEqual(len(cart_product2), 1)
        self.assertEqual(cart_product2[0].quantity, 3)

    def test_cart_remove(self):
        cart = self.get_default_cart()

        # Ack
        product1_id = self.product_ids[0]
        product2_id = self.product_ids[1]
        cart.add(product_id=product1_id, quantity=5)
        cart.add(product_id=product2_id, quantity=3)
        cart.remove(product_id=product1_id)

        cart_product1 = list(filter(lambda c: c.product_id == product1_id, cart.cart.cart_products))
        cart_product2 = list(filter(lambda c: c.product_id == product1_id, cart.cart.cart_products))

        self.assertEqual(len(cart_product1), 0)
        self.assertEqual(len(cart_product2), 1)
        self.assertEqual(cart_product2[0].quantity, 3)
    
    def test_cart_has(self):
        cart = self.get_default_cart()

        # Ack
        product1_id = self.product_ids[0]
        product2_id = self.product_ids[1]
        cart.add(product_id=product1_id, quantity=5)

        self.assertTrue(cart.has(product_id=product1_id))
        self.assertFalse(cart.has(product_id=product2_id))

    def test_cart_isEmpty(self):
        cart = self.get_default_cart()

        # Ack
        self.assertTrue(cart.isEmpty())
        product1_id = self.product_ids[0]
        cart.add(product_id=product1_id, quantity=5)
        self.assertFalse(cart.isEmpty())

    def test_cart_destroy(self):
        cart = self.get_default_cart()

        # Ack
        product1_id = self.product_ids[0]
        cart.add(product_id=product1_id, quantity=5)
        cart.destroy()
        self.assertIsNone(cart.cart)
    

if __name__ == '__main__':
    unittest.main()
