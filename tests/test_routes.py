from application import app, db
from flask_testing import TestCase
from application.models import User, Category, Product, PaymentDetails, Orders, Address, OrderItem, Cart, CartItem, CartDisplay, CheckAdmin, CheckPostcode, BannedChars
from datetime import datetime

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost:3306/flask_test",
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app
    
    def setUp(self):
        db.create_all()
        today = datetime.today()
        db.session.add(User(
            name = "test",
            email = "test@test.com",
            phone = "01234567890",
            password = "test" 
        ))
        db.session.commit()

    def tearDown(self):
        db.session.remove()

class TestModels(TestBase):
    def test_user_model(self):
        #  get the user we created in the setup
        test = User.query.filter_by(name="test").first()
        # Test the user we created in the setup
        self.assertEqual(test.name, "test")

    def test_create_user(self):
        user = User(
            name = "test_2",
            email = "test2@qa.com",
            phone = "01234567890",
            password = "test"
        )
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.name, "test_2")
        #  get the user we created in the setup
        test = User.query.filter_by(name="test").first()
        # Test the user we created in the setup
        response = self.client.post('/login', data=dict(
            email="james@qa.com", 
            password="password"
        ), follow_redirects=True)
        self.assertIn(b'Log Out', response.data)

    def test_login(self):
        #  get the user we created in the setup
        test = User.query.filter_by(name="test").first()
        # Test the user we created in the setup
        response = self.client.post('/login', data=dict(
            email="james@qa.com", 
            password="password"
        ), follow_redirects=True)
        self.assertIn(b'Log Out', response.data)
    
    def test_register(self):

        response = self.client.post('/signup', data=dict(
            name="user_1",
            email="user@qa.com",
            phone="01234567890",
            password="password",
            confirm_password="password"
        ), follow_redirects=True)

        response_2 = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)
        self.assertIn(b'Log Out', response_2.data)
    
    def test_register_name_fail(self):

        response = self.client.post('/signup', data=dict(
            name="user1!",
            email="user@qa.com",
            phone="01234567890",
            password="password",
            confirm_password="password"
        ), follow_redirects=True)

        self.assertIn(b'Invalid character in username.', response.data)

    def test_register_name_admin(self):

        response = self.client.post('/signup', data=dict(
            name="admin",
            email="user234@qa.com",
            phone="01234567890",
            password="password",
            confirm_password="password"
        ), follow_redirects=True)

        self.assertIn(b"Name cannot", response.data)
    
    def test_logout(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com", 
            password="password"
        ), follow_redirects=True)

        response_2 = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Log In', response_2.data)

    

    def test_order_place(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)

        # add an item to the cart
        response_2 = self.client.get('/add/1', follow_redirects=True)
        # place an order
        response_3 = self.client.post('/checkout', data=dict(
            house_name_num="1",
            street="street",
            town_city="city",
            postcode="p04 4de"
        ), follow_redirects=True)

        response_4 = self.client.post('/complete-order', data=dict(
            cardholder_name="test",
            card_number="1234567890123456",
            expiry_date="12/22",
            security_code="123"
        ), follow_redirects=True)
        self.assertIn(b"Heres a rundown of your order", response_4.data)
        # test if payment details were added to the database
        payment_details = PaymentDetails.query.filter_by(cardholder_name="test").first()
        self.assertEqual(payment_details.cardholder_name, "test")

    def test_order_place_existing_payment_details(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)

        # add an item to the cart
        response_2 = self.client.get('/add/1', follow_redirects=True)
        response_2 = self.client.get('/add/2', follow_redirects=True)
        # place an order
        response_3 = self.client.post('/checkout', data=dict(
            house_name_num="1",
            street="street",
            town_city="city",
            postcode="p04 4de"
        ), follow_redirects=True)

        response_4 = self.client.post('/complete-order', data=dict(
            cardholder_name="test",
            card_number="1234567890123456",
            expiry_date="12/22",
            security_code="123"
        ), follow_redirects=True)
        self.assertIn(b"Heres a rundown of your order", response_4.data)
        # test if payment details were added to the database
        payment_details = PaymentDetails.query.filter_by(cardholder_name="test").first()
        self.assertEqual(payment_details.cardholder_name, "test")
    
    def test_invalid_postcode(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)

        # add an item to the cart
        response_2 = self.client.get('/add/1', follow_redirects=True)
        response_2 = self.client.get('/add/2', follow_redirects=True)
        # place an order
        response_3 = self.client.post('/checkout', data=dict(
            house_name_num="1",
            street="street",
            town_city="city",
            postcode="xdfg"
        ), follow_redirects=True)
        self.assertIn(b"Invalid postcode.", response_3.data)

    def test_remove_from_from_cart(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)

        # add an item to the cart
        response_2 = self.client.get('/add/1', follow_redirects=True)
        response_2 = self.client.get('/add/2', follow_redirects=True)
        response_3 = self.client.get('/cart/remove/1', follow_redirects=True)
        # check whether 'iPhone 12 Pro" isn't in the response
        self.assertNotIn(b"iPhone 12 Pro", response_3.data)
    
    def test_empty_cart(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)
        # add an item to the cart
        response_2 = self.client.get('/add/1', follow_redirects=True)
        response_2 = self.client.get('/add/2', follow_redirects=True)
        response_3 = self.client.get('/empty-cart', follow_redirects=True)
        # check whether 'iPhone 12 Pro" isn't in the response
        self.assertIn(b"Your cart is empty!", response_3.data)

    
    def test_contact(self):
        response = self.client.post('/contact', data=dict(
            name="test",
            email="user@qa.com",
            message="test"
        ), follow_redirects=True)
        self.assertIn(b"Thanks for getting in touch", response.data)
        response = self.client.get('/contact', follow_redirects=True)
        self.assertIn(b"Send Message", response.data)

    def test_my_orders(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)
        response_2 = self.client.get('/my-orders', follow_redirects=True)
        self.assertIn(b"Orders for User ID:", response_2.data)
    
    def test_products(self):
        response = self.client.get('/products', follow_redirects=True)
        self.assertIn(b"iPhone 12 Pro", response.data)

    def test_home(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b"Welcome to the QA Store!", response.data)

    def test_product_1(self):
        response = self.client.get('/product/1', follow_redirects=True)
        self.assertIn(b"iPhone 12 Pro", response.data)
    
    def test_category(self):
        response = self.client.get('/category', follow_redirects=True)
        self.assertIn(b"TVs", response.data)
        self.assertIn(b"Phones", response.data)
        self.assertIn(b"Laptops", response.data)

    def test_update_cart(self):
        response = self.client.post('/login', data=dict(
            email="user@qa.com",
            password="password"
        ), follow_redirects=True)
        response_2 = self.client.get('/add/1', follow_redirects=True)
        response_3 = self.client.get('/cart/update/1/24', follow_redirects=True)
        self.assertIn(b"24", response_3.data)
    
    def test_cart_logged_out(self):
        response = self.client.get('/cart', follow_redirects=True)
        self.assertIn(b"Log In", response.data)

    def test_about(self):
        response = self.client.get('/about', follow_redirects=True)
        self.assertIn(b"About Us", response.data)

    def test_add_to_cart_not_logged_in(self):
        response = self.client.get('/add/1', follow_redirects=True)
        self.assertIn(b"Log In", response.data)