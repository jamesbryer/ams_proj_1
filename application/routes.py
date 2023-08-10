from flask import render_template, request, redirect, url_for
from application import app, db
from application.models import Product, Category, User, Order, OrderItem
from application import bcrypt

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')

@app.route('/products', methods=['GET', 'POST'])
def products():
    products = Product.query.all()
    categories = Category.query.all()
    for product in products:
        print(product)
    return render_template('products.html', title='Products', products=products)

@app.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):
    product = Product.query.get(id)
    category = Category.query.get(product.category_id)
    return render_template('product.html', title='Product', product=product, category=category)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')

@app.route('/category', methods=['GET', 'POST'])
def contact():
    return render_template('category.html', title='Categories')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('/cart.html', title='Cart')