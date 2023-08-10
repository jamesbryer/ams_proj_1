from application import db
from wtforms.validators import ValidationError
from datetime import datetime

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return ''.join([
            'Category ID: ', str(self.id), '\r\n',
            'Name: ', self.name
        ])

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpeg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)


    def __repr__(self):
        return ''.join([
            'Product ID: ', str(self.id), '\r\n',
            'Name: ', self.name, '\r\n', self.description
        ])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n',
            'Email: ', self.email, '\r\n', self.name
        ])
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __repr__(self):
        return ''.join([
            'Order ID: ', str(self.id), '\r\n',
            'User ID: ', str(self.user_id), '\r\n', str(self.date)
        ])
    
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

    def __repr__(self):
        return ''.join([
            'OrderItem ID: ', str(self.id), '\r\n',
            'Order ID: ', str(self.order_id), '\r\n', str(self.quantity)
        ])

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return ''.join([
            'Cart ID: ', str(self.id), '\r\n',
            'Product ID: ', str(self.product_id)
        ])
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    def __repr__(self):
        return ''.join([
            'CartItem ID: ', str(self.id), '\r\n',
            'Cart ID: ', str(self.cart_id), '\r\n', str(self.quantity)
        ])
    
class WishList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return ''.join([
            'WishList ID: ', str(self.id), '\r\n',
            'Product ID: ', str(self.product_id)
        ])
    
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
                raise ValidationError(self.message)
