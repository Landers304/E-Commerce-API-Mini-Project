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

    def __repr__(self):
        return f'<Customer {self.name}>'

# Customer schema
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

# Create the tables (inside the app context)
with app.app_context():
    db.create_all()

# Route to add a customer
@app.route('/customers', methods=['POST'])
def add_customer():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    address = request.json['address']

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_customer = Customer(name=name, email=email, password=hashed_password.decode('utf-8'), address=address)

    try:
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer), 201
    except Exception as e:
        db.session.rollback()
        return {'message': f'Error: {str(e)}'}, 400

# Route to authenticate a customer (Login)
@app.route('/login', methods=['POST'])
def login_customer():
    email = request.json['email']
    password = request.json['password']

    customer = Customer.query.filter_by(email=email).first()

    if customer and bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf-8')):
        # Create JWT token
        access_token = create_access_token(identity=customer.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

# Route to get all customers with pagination
@app.route('/customers', methods=['GET'])
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    customers = Customer.query.paginate(page, per_page, False)
    return customers_schema.jsonify(customers.items)

# Route to search customers by name or email
@app.route('/customers/search', methods=['GET'])
def search_customers():
    query = request.args.get('query', '', type=str)
    customers = Customer.query.filter(
        or_(
            Customer.name.ilike(f'%{query}%'),
            Customer.email.ilike(f'%{query}%')
        )
    ).all()
    return customers_schema.jsonify(customers)

# Route to get customer by ID (JWT protected)
@app.route('/customers/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

# Schema instances
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Main driver function
if __name__ == '__main__':
    app.run(debug=True)