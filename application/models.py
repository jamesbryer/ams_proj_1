from application import db
from wtforms.validators import ValidationError


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    category = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return ''.join([
            'Product ID: ', str(self.id), '\r\n',
            'Name: ', self.name, '\r\n', self.description
        ])
    
