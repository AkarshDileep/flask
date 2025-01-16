from functools import wraps
import json
from flask import Flask, flash, request, render_template, redirect, session, url_for, jsonify
from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open('data.json', 'r') as f:
    data = json.load(f)  # Correctly load the JSON
    users = data['users']  # Access the "users" key in the JSON
    products = data['products']  # Access the "products" key in the JSON

def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

# Save data to JSON file
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

address = ""

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/home')
def home():
    return render_template('home.html',products=products)

@app.route('/product/<int:id>', methods=['GET', 'POST'])
def product(id):
    for product in products:
        if product['id'] == id:
            return render_template('product.html', product=product)
    return "Product not found"
    
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Iterate through the list of user dictionaries
        for user in users:
            if user['username'] == username and user['password'] == password:
                address=user['address']
                phone=user['phone']
                return redirect(url_for('home'))

        return "Invalid credentials"  # Handle invalid login

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    data = load_data()  # Load the current data from the file
    users = data['users']  # Access the products list

    if request.method == 'POST':
        phone = int(request.form['phone'])
        address = request.form['address']
        if phone in users:
            return "User already exists"
        new_user = {
            "username": request.form['username'],
            "password": request.form['password'],
            "address": address,
            "phone": phone
        }

        
        users.append(new_user)

        
        data['users'] = users
        save_data(data)
        return redirect(url_for('login'))
    return render_template('sign.html')








@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    # Initialize cart in session if it doesn't exist
    if "cart" not in session:
        session["cart"] = []
    
    # Add product to cart
    session["cart"].append(id)
    session.modified = True
    return redirect(url_for("view_cart"))



@app.route("/cart")
def view_cart():
    cart_items = []
    total_price = 0

    if "cart" in session:
        # Get product details for each product ID in the cart
        for product_id in session["cart"]:
            
            cart_items.append(product_id)
                

    return render_template("cart.html", cart_items=cart_items, total_price=total_price,products=products)
@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)  # Clear cart
    return redirect(url_for("view_cart"))



@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    data = load_data()  # Load the current data from the file
    products = data['products']  # Access the products list

    if request.method == 'POST':
        # Get form data
        new_product = {
            "id": int(request.form['id']),
            "name": request.form['name'],
            "price": float(request.form['price']),
            "img": request.form['img'],
            "description": request.form['description'],
            "category": int(request.form['category'])
        }

        # Append the new product to the products list
        products.append(new_product)

        # Save the updated data back to the file
        data['products'] = products
        save_data(data)

        return redirect(url_for('home'))

    return render_template('add.html')
@app.route('/order', methods=['GET', 'POST'])
def order():
        if request.method == 'POST':
            phonee=""
            data = load_data()
            users = data['users']            
            phone = request.form['phone']
            for user in users:
                phonee = request.form['phone']
                if phonee == phone:
                    
                    address=user['address']
                    return render_template('order.html',address=address, phone=phone)

                return user['phone']
        return render_template('order.html')

if __name__ == '__main__':
    app.run(debug=True)