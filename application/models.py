import re
from application import db
from wtforms.validators import ValidationError
from datetime import datetime


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpeg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    orders = db.relationship('Orders', backref='customer', lazy=True)

    
class PaymentDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardholder_name = db.Column(db.String(30), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiry_date = db.Column(db.String(5), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_name_num = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(30), nullable=False)
    town_city = db.Column(db.String(30), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    user = db.relationship('User', backref='address', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_details = db.relationship('PaymentDetails', backref='order', lazy=True)
    payment_details_id = db.Column(db.Integer, db.ForeignKey('payment_details.id'), nullable=False)
    address = db.relationship('Address', backref='order', lazy=True)
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)

    
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order = db.relationship('Orders', backref='order', lazy=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)
    address = db.relationship('Address', backref='card', foreign_keys=[delivery_address_id])

    
    def set_quantity(self, product_id, quantity):
        cart_item = CartItem.query.filter_by(product_id=product_id, cart_id=self.id).first()
        if cart_item:
            if quantity > 0:
                cart_item.quantity = quantity
                db.session.commit()
            else:
                db.session.delete(cart_item)
                db.session.commit()
    
    def add_item(self, product_id):
        cart_item = CartItem.query.filter_by(product_id=product_id, cart_id=self.id).first()
        if cart_item:
            cart_item.quantity += 1
            db.session.commit()
        else:
            new_cart_item = CartItem(product_id=product_id, quantity=1, cart_id=self.id)
            db.session.add(new_cart_item)
            db.session.commit()
    
    def remove_item(self, product_id):
        cart_item = CartItem.query.filter_by(product_id=product_id, cart_id=self.id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

    def empty_cart(self):
        cart_items = CartItem.query.filter_by(cart_id=self.id).all()
        for item in cart_items:
            db.session.delete(item)
            db.session.commit()
        
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    
class CartDisplay():
    def __init__(self, product_id, name, price, quantity, image) -> None:
        self.id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.image = image


    
class CheckAdmin:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data.lower() == 'admin':
            raise ValidationError(self.message)

class BannedChars:
    def __init__(self, message=None) -> None:
        self.message = message

    def __call__(self, form, field):
        banned_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        for char in banned_chars:
            if char in field.data:
                self.message = "Invalid character in username."
                raise ValidationError(self.message)

class CheckPostcode:

    def __init__(self, message=None) -> None:
        self.message = message
    
    def __call__(self, form, field):
        # Regex for UK postcode
        regex = r"^[A-Za-z]{1,2}\d{1,2}\s?\d[A-Za-z]{2}$"
        if not re.match(regex, field.data):
            raise ValidationError(self.message)
