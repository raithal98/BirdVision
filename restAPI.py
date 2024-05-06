from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = ''  # Change this to add a secure secret key
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price
        }

# Schemas
class ProductSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String(validate=validate.Length(max=200))
    price = fields.Float(required=True)

class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=1, max=50))
    password = fields.String(required=True, validate=validate.Length(min=6))

product_schema = ProductSchema()
user_schema = UserSchema()

# Create the database and tables
with app.app_context():
    db.create_all()

# Authentication and User Management
@app.route('/register', methods=['POST'])
def register():
    try:
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Invalid data', 'errors': err.messages}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    try:
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Invalid data', 'errors': err.messages}), 400

    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200

# Product Endpoints
@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    limit = request.args.get('limit', default=10, type=int)
    skip = request.args.get('skip', default=0, type=int)

    products = Product.query.offset(skip).limit(limit).all()
    return jsonify([product.to_dict() for product in products]), 200

@app.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({'message': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Invalid data', 'errors': err.messages}), 400

    new_product = Product(title=data['title'], description=data.get('description', ''), price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    try:
        data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify({'message': 'Invalid data', 'errors': err.messages}), 400

    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    product.title = data['title']
    product.description = data.get('description', product.description)
    product.price = data['price']

    db.session.commit()
    return jsonify(product.to_dict()), 200

@app.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

# Default error handler for 404 errors
@app.errorhandler(404)
def not_found(e):
    return jsonify({'message': 'Resource not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
