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


    
