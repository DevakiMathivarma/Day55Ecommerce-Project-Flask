# # app.py
# from flask import Flask, render_template, session, redirect, url_for, jsonify, request,flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import CSRFProtect
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'your-secret-key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
# db = SQLAlchemy(app)
# csrf = CSRFProtect(app)

# # Models
# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     price = db.Column(db.Integer)
#     quantity = db.Column(db.Integer)
#     description = db.Column(db.String(200))
#     image = db.Column(db.String(100))
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
        
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)

# # Routes
# @app.route('/')
# def home():
#     return redirect(url_for('products'))

# @app.route('/products')
# def products():
#     products = Product.query.all()
#     return render_template('products.html', products=products)

# @app.route('/cart/add/<int:product_id>', methods=['POST'])
# def add_to_cart(product_id):
#     if 'user_id' not in session:
#         return jsonify({'message': 'Please login to add to cart'}), 401
#     product = Product.query.get(product_id)
#     if not product:
#         return jsonify({'message': 'Product not found'}), 404

#     cart = session.get('cart', {})
#     cart[str(product_id)] = cart.get(str(product_id), 0) + 1
#     session['cart'] = cart
#     return jsonify({'message': f'{product.name} added to cart'})
# @app.route('/cart/update/<int:product_id>', methods=['POST'])
# def update_cart(product_id):
#     data = request.get_json()
#     new_qty = int(data.get('quantity', 1))

#     cart = session.get('cart', {})
#     cart[str(product_id)] = new_qty
#     session['cart'] = cart

#     # Recalculate total
#     total = 0
#     for pid_str, qty in cart.items():
#         product = Product.query.get(int(pid_str))
#         if product:
#             total += qty * product.price

#     return jsonify({'success': True, 'new_total': total})
# @app.route('/cart')
# def view_cart():
#     cart = session.get('cart', {})
#     cart_items = []
#     total = 0

#     for pid_str, qty in cart.items():
#         product = Product.query.get(int(pid_str))
#         if product:
#             item = {
#                 'id': product.id,
#                  'image': product.image,
#                 'name': product.name,
#                 'price': product.price,
#                 'quantity': qty,
#                 'total_price': qty * product.price
#             }
#             cart_items.append(item)
#             total += item['total_price']

#     return render_template('cart.html', products=cart_items, total=total)

# @app.route('/checkout')
# def checkout():
#     session.pop('cart', None)
#     return "<h2>Thank you for your purchase!</h2><a href='/products'>Continue Shopping</a>"

# @app.route('/load_sample_products')
# def load_sample_products():
#     if Product.query.first():
#         return "Products already loaded."
#     sample_products = [
#         {
#             'id': 1,
#             'name': 'Laptop',
#             'price': 49999,
#             'description': 'High-performance laptop',
#             'image': 'laptop.PNG'
#         },
#         {
#             'id': 2,
#             'name': 'Smartphone',
#             'price': 19999,
#             'description': 'Feature-rich smartphone',
#             'image': 'smartphone.PNG'
#         },
#         {
#             'id': 3,
#             'name': 'Headphones',
#             'price': 2499,
#             'description': 'Noise-cancelling headphones',
#             'image': 'headphones.PNG'
#         },
#         {
#             'id': 4,
#             'name': 'Smartwatch',
#             'price': 9999,
#             'description': 'Fitness tracking smartwatch',
#             'image': 'smartwatch.PNG'
#         },
#         {
#             'id': 5,
#             'name': 'Bluetooth Speaker',
#             'price': 1499,
#             'description': 'Portable speaker',
#             'image': 'bluetooth.PNG'
#         },
#         {
#             'id': 6,
#             'name': 'Keyboard',
#             'price': 699,
#             'description': 'Mechanical keyboard',
#             'image': 'keyboard.PNG'
#         },
#         {
#             'id': 7,
#             'name': 'Monitor',
#             'price': 8999,
#             'description': '24-inch LED monitor',
#             'image': 'monitor.PNG'
#         },
#         {
#             'id': 8,
#             'name': 'Power Bank',
#             'price': 1299,
#             'description': '10000mAh fast-charging',
#             'image': 'powerbank.PNG'
#         },
#         {
#             'id': 9,
#             'name': 'Camera',
#             'price': 29999,
#             'description': 'DSLR Camera',
#             'image': 'camera.PNG'
#         },
#         {
#             'id': 10,
#             'name': 'Router',
#             'price': 1999,
#             'description': 'Dual-band Wi-Fi router',
#             'image': 'router.PNG'
#         },
#     ]
#     for p in sample_products:
#         db.session.add(Product(**p))
#     db.session.commit()
#     return "Sample products added!"
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if User.query.filter_by(username=username).first():
#             flash("Username already exists")
#             return redirect('/register')
#         user = User(username=username)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         flash("Registered successfully. Please login.")
#         return redirect('/login')
#     return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and user.check_password(password):
#             session['user_id'] = user.id
#             flash('Login successful!')
#             return redirect('/products')
#         flash('Invalid username or password.')
#     return render_template('login.html')


# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('Logged out successfully!')
#     return redirect('/products')

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


from flask import Flask, render_template, session, redirect, url_for, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


# MODELS
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(200))
    image = db.Column(db.String(100))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# FORMS
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# ROUTES
@app.route('/')
def home():
    return redirect(url_for('products'))


@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Please login to add to cart'}), 401
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return jsonify({'message': f'{product.name} added to cart'})


@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    data = request.get_json()
    new_qty = int(data.get('quantity', 1))

    cart = session.get('cart', {})
    cart[str(product_id)] = new_qty
    session['cart'] = cart

    # Recalculate total
    total = 0
    for pid_str, qty in cart.items():
        product = Product.query.get(int(pid_str))
        if product:
            total += qty * product.price

    return jsonify({'success': True, 'new_total': total})


@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0

    for pid_str, qty in cart.items():
        product = Product.query.get(int(pid_str))
        if product:
            item = {
                'id': product.id,
                'image': product.image,
                'name': product.name,
                'price': product.price,
                'quantity': qty,
                'total_price': qty * product.price
            }
            cart_items.append(item)
            total += item['total_price']

    return render_template('cart.html', products=cart_items, total=total)


@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return "<h2>Thank you for your purchase!</h2><a href='/products'>Continue Shopping</a>"


@app.route('/load_sample_products')
def load_sample_products():
    if Product.query.first():
        return "Products already loaded."
    sample_products = [
        {'id': 1, 'name': 'Laptop', 'price': 49999, 'description': 'High-performance laptop', 'image': 'laptop.PNG'},
        {'id': 2, 'name': 'Smartphone', 'price': 19999, 'description': 'Feature-rich smartphone', 'image': 'smartphone.PNG'},
        {'id': 3, 'name': 'Headphones', 'price': 2499, 'description': 'Noise-cancelling headphones', 'image': 'headphones.PNG'},
        {'id': 4, 'name': 'Smartwatch', 'price': 9999, 'description': 'Fitness tracking smartwatch', 'image': 'smartwatch.PNG'},
        {'id': 5, 'name': 'Bluetooth Speaker', 'price': 1499, 'description': 'Portable speaker', 'image': 'bluetooth.PNG'},
        {'id': 6, 'name': 'Keyboard', 'price': 699, 'description': 'Mechanical keyboard', 'image': 'keyboard.PNG'},
        {'id': 7, 'name': 'Monitor', 'price': 8999, 'description': '24-inch LED monitor', 'image': 'monitor.PNG'},
        {'id': 8, 'name': 'Power Bank', 'price': 1299, 'description': '10000mAh fast-charging', 'image': 'powerbank.PNG'},
        {'id': 9, 'name': 'Camera', 'price': 29999, 'description': 'DSLR Camera', 'image': 'camera.PNG'},
        {'id': 10, 'name': 'Router', 'price': 1999, 'description': 'Dual-band Wi-Fi router', 'image': 'router.PNG'},
    ]
    for p in sample_products:
        db.session.add(Product(**p))
    db.session.commit()
    return "Sample products added!"


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists")
            return redirect('/register')
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully. Please login.")
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect('/products')
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect('/products')
@app.route('/cart/delete/<int:product_id>', methods=['POST'])
def delete_from_cart(product_id):
    cart = session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    # Recalculate total
    total = 0
    products = []
    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            total += product.price * qty

    return jsonify({'success': True, 'new_total': total})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
