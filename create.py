from app import app
from application import db, bcrypt
from application.models import Product, Category, User, Order, OrderItem
from datetime import datetime


with app.app_context():
    db.drop_all()
    db.create_all()

    from application.models import Product
    phones = Category(name='Phones')
    laptops = Category(name='Laptops')
    tvs = Category(name='TVs')
    db.session.add(phones)
    db.session.add(laptops)
    db.session.add(tvs)
    db.session.commit()

    phone_1 = Product(name='iPhone 12 Pro', price=500, image="iphone_12_pro.jpg", description='A nice phone', category_id=1)
    phone_2 = Product(name='Samsung Galaxy S20', price=400, image="samsung_galaxy_s20.jpg", description='A nice phone', category_id=1)
    phone_3 = Product(name='Google Pixel 5', price=300, image="google_pixel_5.jpg", description='A nice phone', category_id=1)
    phone_4 = Product(name='OnePlus 8T', price=200, image="oneplus_8t.jpg", description='A nice phone', category_id=1)
    phone_5 = Product(name='Huawei P40 Pro', price=100, image="huawei_p40_pro.jpg", description='A nice phone', category_id=1)
    db.session.add(phone_1)
    db.session.add(phone_2)
    db.session.add(phone_3)
    db.session.add(phone_4)
    db.session.add(phone_5)
    db.session.commit()

    laptop_1 = Product(name='MacBook Pro', price=500, description='A nice laptop', category_id=2)
    laptop_2 = Product(name='Dell XPS 13', price=400, description='A nice laptop', category_id=2)
    laptop_3 = Product(name='Lenovo ThinkPad X1 Carbon', price=300, description='A nice laptop', category_id=2)
    laptop_4 = Product(name='HP Envy 13', price=200, description='A nice laptop', category_id=2)
    laptop_5 = Product(name='Microsoft Surface Laptop 3', price=100, description='A nice laptop', category_id=2)
    db.session.add(laptop_1)
    db.session.add(laptop_2)
    db.session.add(laptop_3)
    db.session.add(laptop_4)
    db.session.add(laptop_5)
    db.session.commit()
    
    tv_1 = Product(name='Samsung Q90 QLED TV', price=500, description='A nice TV', category_id=3)
    tv_2 = Product(name='LG CX OLED TV', price=400, description='A nice TV', category_id=3)
    tv_3 = Product(name='Samsung Q80T QLED TV', price=300, description='A nice TV', category_id=3)
    tv_4 = Product(name='Sony Bravia A8H OLED TV', price=200, description='A nice TV', category_id=3)
    tv_5 = Product(name='TCL 6-Series QLED TV', price=100, description='A nice TV', category_id=3)
    db.session.add(tv_1)
    db.session.add(tv_2)
    db.session.add(tv_3)
    db.session.add(tv_4)
    db.session.add(tv_5)
    db.session.commit()





