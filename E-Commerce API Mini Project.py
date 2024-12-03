from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import bcrypt
from sqlalchemy import or_

# Initialize the app
app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Finroy1121!@127.0.0.1/ecommerce_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Change this to a real secret key

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(255))

    def __init__(self, name, email, password, address):
        self.name = name
        self.email = email
        self.password = password
        self.address = address

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

# Schemas
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# Schema instances
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create the tables (inside the app context)
with app.app_context():
    db.create_all()

# Customer routes
@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    address = request.json['address']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_customer = Customer(name=name, email=email, password=hashed_password.decode('utf-8'), address=address)

    try:
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer), 201
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, 400

@app.route('/customers', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    customers = Customer.query.paginate(page, per_page, False)
    return customers_schema.jsonify(customers.items)

@app.route('/customers/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.json
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.address = data.get('address', customer.address)

    try:
        db.session.commit()
        return customer_schema.jsonify(customer)
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, 400

@app.route('/customers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, 400

# Product routes
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    try:
        db.session.commit()
        return product_schema.jsonify(product)
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, 400

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, 400

# Main driver function
if __name__ == '__main__':
    app.run(debug=True)
