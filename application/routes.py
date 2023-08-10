from flask import render_template, request, redirect, url_for
from application import app, db
from application.models import Product, Category, User, Order, OrderItem, Cart
from application.forms import SignUpForm

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
    categories = Category.query.all()
    products = Product.query.all()
    return render_template('category.html', title='Categories', categories=categories, products=products)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('/cart.html', title='Cart')

@app.route('/cart/add/<int:id>', methods=['GET', 'POST'])
def add_to_cart(id):
    # find users cart
    current_user = User.query.get(1)
    carts = Cart.query.filter_by(user_id=current_user.id).all()
    # if no cart, create one
    # add product to cart
    # if product already in cart, increase quantity

    return redirect(url_for('cart'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print('validated')
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=form.password.data,
                address=form.address.data,
                postcode=form.postcode.data,
                phone=form.phone.data)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print('not validated')
    return render_template('/signup.html', title='Sign Up', form=form)