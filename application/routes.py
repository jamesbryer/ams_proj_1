from flask import render_template, request, redirect, url_for, session
from application import app, db
from application.models import Product, Category, User, Orders, OrderItem, Cart, CartItem, CartDisplay, PaymentDetails, Address
from application.forms import SignUpForm, LoginForm, PaymentForm, AddressForm
from flask_bcrypt import Bcrypt
from application import bcrypt
from datetime import datetime

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
    # if session id exists, find cart
    if 'user_id' in session:
        cart = Cart.query.filter_by(user_id=session['user_id']).first()
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        cart_products = []
        for item in cart_items:
            product = Product.query.get(item.product_id)
            item = CartDisplay(product.id, product.name, product.price, item.quantity, product.image)
            cart_products.append(item)
        return render_template('/cart.html', title='Cart', products=cart_products)
    else:
        return redirect(url_for('login'))

@app.route('/cart/update/<int:id>/<int:quantity>', methods=['GET', 'POST'])
def update_cart(id, quantity):
    if 'user_id' in session:
        # find users cart
        cart = Cart.query.filter_by(user_id=session['user_id']).first()
        # add product to cart
        cart.set_quantity(id, quantity)
        return redirect(url_for('cart'))

@app.route('/add/<int:id>', methods=['GET', 'POST'])
def add_to_cart(id):
    if 'user_id' in session:
        # find users cart
        cart = Cart.query.filter_by(user_id=session['user_id']).first()
        # add product to cart
        cart.add_item(id)
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('login'))

@app.route('/cart/remove/<int:id>', methods=['GET', 'POST'])
def remove_from_cart(id):
    # find users cart
    cart = Cart.query.filter_by(user_id=session['user_id']).first()
    # remove product from cart
    cart.remove_item(id)
    return redirect(url_for('cart'))

@app.route('/empty-cart', methods=['GET', 'POST'])
def empty_cart():
    # find users cart
    cart = Cart.query.filter_by(user_id=session['user_id']).first()
    # remove product from cart
    cart.empty_cart()
    return redirect(url_for('cart'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print('validated')
            user = User(
                name = form.name.data,
                email = form.email.data,
                password = bcrypt.generate_password_hash(form.password.data),
                address = form.address.data,
                postcode = form.postcode.data,
                phone = form.phone.data)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print('not validated')
    return render_template('/signup.html', title='Sign Up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print('post')
        if form.validate_on_submit():
            print('validated')
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                print('user found')
                # create session variable for user_id
                session['user_id'] = user.id
                # check if user has a cart
                cart = Cart.query.filter_by(user_id=user.id).first()
                if cart:
                    print('cart found')
                else:
                    print('cart not found')
                    cart = Cart(user_id=user.id)
                    db.session.add(cart)
                    db.session.commit()
                return redirect(url_for('home'))
            else:
                print('user not found')
        else:
            print('not validated')
    return render_template('/login.html', title='Login', form=form)

@app.route('/logout')
def clear_variable():
    session.pop('user_id', None)  # Remove 'user_id' from session
    print("Session variable cleared!")
    return redirect(url_for('home'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = Cart.query.filter_by(user_id=session['user_id']).first()
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    # if there are items in the cart
    if cart_items:
        form = AddressForm()
        if 'user_id' not in session:
            return redirect(url_for('login'))
        # if method is post
        if request.method == 'POST':
            # if form is valid
            if form.validate_on_submit():
                # check if address already exists
                if not Address.query.filter_by(user_id=session['user_id'], house_name_num=request.form["house_name_num"], street=request.form["street"]).first():
                    address = Address(user_id=session['user_id'], house_name_num=request.form["house_name_num"], street=request.form["street"], town_city=request.form["town_city"], postcode=request.form["postcode"])
                    db.session.add(address)
                    db.session.commit()
                address = Address.query.filter_by(user_id=session['user_id'], house_name_num=request.form["house_name_num"], street=request.form["street"]).first()
                # cart = Cart.query.filter_by(user_id=session['user_id']).first()
                db.session.add(cart)
                db.session.commit()
                cart.delivery_address_id = address.id
                db.session.add(address)
                db.session.commit()
                return redirect(url_for('complete_order'))
    else:
        return redirect(url_for('home'))
        

    cart = Cart.query.filter_by(user_id=session['user_id']).first()
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    cart_products = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        item = CartDisplay(product.id, product.name, product.price, item.quantity, product.image)
        cart_products.append(item)
    addresses = Address.query.filter_by(user_id=session['user_id']).all()
    return render_template('/checkout.html', title='Checkout', addresses=addresses, products=cart_products, form=form)

@app.route('/complete-order', methods=['GET', 'POST'])
def complete_order():
    cart = Cart.query.filter_by(user_id=session['user_id']).first()
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    # if there are items in the cart and user is logged in
    if 'user_id' in session and cart_items:
        # if form has been submitted
        if request.method == 'POST':
            print('post')
            # check if payment details already exist
            if PaymentDetails.query.filter_by(user_id=session['user_id'], card_number=request.form['card_number']).first():
                payment_details = PaymentDetails.query.filter_by(user_id=session['user_id'], card_number=request.form['card_number']).first()
            else:
                payment_details = PaymentDetails(
                    user_id = session['user_id'],
                    cardholder_name = request.form['cardholder_name'],
                    card_number = request.form['card_number'],
                    expiry_date = request.form['expiry_date'],
                    cvv = request.form['security_code'])
            db.session.add(payment_details)
            db.session.commit()
            # create order
            # cart = Cart.query.filter_by(user_id=session['user_id']).first()
            payment_details_id = PaymentDetails.query.filter_by(user_id=session['user_id'], card_number=request.form['card_number']).first().id
            # cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            order = Orders(user_id=session['user_id'], date=datetime.now(), payment_details_id=payment_details_id, delivery_address_id=cart.delivery_address_id)
            db.session.add(order)
            db.session.commit()
            # get the order id from the order just created
            order_id = Orders.query.filter_by(user_id=session['user_id'], payment_details_id=payment_details_id).first().id
            print(order_id)
            db.session.add(order)
            for item in cart_items:
                order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
                db.session.add(order_item)

            db.session.commit()
            cart.empty_cart()
            return redirect(url_for('home'))
        

        # # find users cart
        # cart = Cart.query.filter_by(user_id=session['user_id']).first()
        # cart_items = CartItem.query.filter_by(cart_id=cart.id).all()

        # if method isn't post - load page
        cart_products = []
        # search payment_details table for user_id - sent to form for autofill option
        payment_details = PaymentDetails.query.filter_by(user_id=session['user_id']).all()
        # create from
        payment_form = PaymentForm()
        # create list of Cart Display objects to pass to template - combines product and cart item
        for item in cart_items:
            product = Product.query.get(item.product_id)
            item = CartDisplay(product.id, product.name, product.price, item.quantity, product.image)
            cart_products.append(item)
        return render_template('/complete-order.html', title='Checkout', products=cart_products, form=payment_form, payment_details=payment_details)
    
    
    else:
        return redirect(url_for('home'))