from flask import Flask, request, jsonify, send_from_directory,g,send_file,Response,render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS, cross_origin
from sqlalchemy import or_,and_
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta,datetime
from dateutil import parser
from functools import wraps 
from jinja2 import Template
from celery_module import make_celery
from mail import send_mail
from flask_caching import Cache
import pandas as pd
import uuid
import io
import os
import csv
import random
import string

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True, "expose_headers": "Authorization",
                             "allow_headers": ["Content-Type", "Authorization"], "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})




app.config['UPLOAD_FOLDER'] = 'uploads'
upload_folder =  app.config['UPLOAD_FOLDER']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'bindu'
app.config.update(
    broker_url='redis://localhost:6379',
    result_backend='redis://localhost:6379',
    CACHE_TYPE='redis',
    CACHE_REDIS_URL='redis://localhost:6379')

celery = make_celery(app)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

db = SQLAlchemy(app)
jwt = JWTManager(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10, monthly_report.s(), name='monthly_report')

@celery.on_after_configure.connect
def setup_daily_reminder(sender, **kwargs):
    sender.add_periodic_task(10, daily_reminder.s(), name='daily_reminder')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

roles_users = db.Table('roles_users',
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_status = db.Column(db.String(),nullable=False,default="Not Active")
    is_approved = db.Column(db.String(), nullable=False, default="Pending")
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    cart = db.relationship('Cart',backref='user',lazy=True)
    order = db.relationship('Order',backref='user',lazy=True)
    last_login = db.Column(db.DateTime(), nullable=True)

    def set_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    def update_inactive_status(self):
        if self.last_login and (datetime.utcnow() - self.last_login).days > 7:
            self.is_status = "Inactive"
            db.session.commit()

class Category(db.Model):
    id = db.Column(db.Integer(),primary_key = True, nullable=False)
    name = db.Column(db.String(50),nullable=False,unique=True)
    products= db.relationship('Product',back_populates='category',lazy=True) 
    is_status = db.Column(db.String(),nullable=False,default="Active")
    changes_pending = db.Column(db.Boolean(), nullable=False, default=False)
    products = db.relationship('Product', back_populates='category', lazy=True)


class CategoryUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    new_name = db.Column(db.String(50), nullable=False)
    new_is_status = db.Column(db.String(),nullable=True)
    action = db.Column(db.String(10), nullable=False) 
    is_approved = db.Column(db.String(), nullable=False, default='Pending')
    category = db.relationship('Category', backref='updates', lazy=True)   
    

class Product(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(250))
    stock = db.Column(db.Integer())
    price_per_unit = db.Column(db.Integer(), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'), nullable=False)
    expiry_date = db.Column(db.Date(), nullable=True) 
    mfg_date = db.Column(db.Date(), nullable=True)  
    sold = db.Column(db.Integer, default=0)
    discount = db.Column(db.Integer, default=0)
    is_status = db.Column(db.String(), nullable=False, default="Active")
    category = db.relationship('Category', back_populates='products', lazy=True)
    unit_of_measurement = db.Column(db.String(), nullable=False, default="Kg")
    


class Cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    total_amount = db.Column(db.Integer())
    product = db.relationship("Product", backref="cart")
    is_status = db.Column(db.String(), nullable=False, default="Not Active")

class Order(db.Model):
    id = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    order_date = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False) 
    total_amount = db.Column(db.Integer())
    order_is_status = db.Column(db.String(50), nullable=False, default="Pending")
    order_product = db.relationship('Orderproduct', backref='order', lazy=True)

    
class Orderproduct(db.Model):
    id = db.Column(db.Integer(),  primary_key=True)
    order_id = db.Column(db.Integer(), db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey('product.id'),  nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    product = db.relationship('Product', backref='orderproduct', lazy=True)


def parse_date(date_str):
    """Parse a date string into a datetime.date object."""
    try:
        parsed_date = parser.parse(date_str).date()
        return parsed_date
    except ValueError:
        raise ValueError(f"Unable to parse date: {date_str}")

def create_and_insert_data():
    # Create all tables in the database
    with app.app_context():
        db.create_all()

        # Add Categories if not already present
        '''
        categories = ['Fruits', 'Snacks', 'Beverages', 'Vegetables']
        for category_name in categories:
            if not Category.query.filter_by(name=category_name).first():
                category = Category(name=category_name, is_status="Active")
                db.session.add(category)
        
        db.session.commit()

        # Fetch all categories from the database
        categories = Category.query.all()

        # Add Products if not already present
        products = products = [
            {'name': 'Apple', 'desc': 'Fresh red apples', 'price_per_unit': 75.00, 'stock': 100, 'unit_of_measurement': 'Kg', 'category': 'Fruits', 'discount': 10},
            {'name': 'Banana', 'desc': 'Ripe yellow bananas', 'price_per_unit': 25.00, 'stock': 200, 'unit_of_measurement': 'Kg', 'category': 'Fruits', 'discount': 5},
            {'name': 'Orange', 'desc': 'Citrusy oranges', 'price_per_unit': 50.00, 'stock': 150, 'unit_of_measurement': 'Kg', 'category': 'Fruits', 'discount': 0},
            {'name': 'Grapes', 'desc': 'Seedless green grapes', 'price_per_unit': 100.00, 'stock': 80, 'unit_of_measurement': 'Kg', 'category': 'Fruits', 'discount': 15},
            {'name': 'Mango', 'desc': 'Sweet mangoes', 'price_per_unit': 90.00, 'stock': 120, 'unit_of_measurement': 'Kg', 'category': 'Fruits', 'discount': 20},
            {'name': 'Potato', 'desc': 'Fresh potatoes', 'price_per_unit': 20.00, 'stock': 250, 'unit_of_measurement': 'Kg', 'category': 'Vegetables', 'discount': 0},
            {'name': 'Tomato', 'desc': 'Red ripe tomatoes', 'price_per_unit': 35.00, 'stock': 180, 'unit_of_measurement': 'Kg', 'category': 'Vegetables', 'discount': 10},
            {'name': 'Carrot', 'desc': 'Crunchy carrots', 'price_per_unit': 60.00, 'stock': 220, 'unit_of_measurement': 'Kg', 'category': 'Vegetables', 'discount': 0},
            {'name': 'Onion', 'desc': 'Fresh onions', 'price_per_unit': 30.00, 'stock': 300, 'unit_of_measurement': 'Kg', 'category': 'Vegetables', 'discount': 5},
            {'name': 'Cucumber', 'desc': 'Green cucumbers', 'price_per_unit': 45.00, 'stock': 200, 'unit_of_measurement': 'Kg', 'category': 'Vegetables', 'discount': 10},
            {'name': 'Chips', 'desc': 'Potato chips', 'price_per_unit': 75.00, 'stock': 500, 'unit_of_measurement': 'Pack', 'category': 'Snacks', 'discount': 15},
            {'name': 'Cookies', 'desc': 'Crunchy chocolate chip cookies', 'price_per_unit': 100.00, 'stock': 350, 'unit_of_measurement': 'Pack', 'category': 'Snacks', 'discount': 0},
            {'name': 'Biscuits', 'desc': 'Assorted biscuits', 'price_per_unit': 50.00, 'stock': 450, 'unit_of_measurement': 'Pack', 'category': 'Snacks', 'discount': 10},
            {'name': 'Pretzels', 'desc': 'Salty pretzels', 'price_per_unit': 65.00, 'stock': 4, 'unit_of_measurement': 'Pack', 'category': 'Snacks', 'discount': 20},
            {'name': 'Candy', 'desc': 'Sugar-coated candy', 'price_per_unit': 40.00, 'stock': 600, 'unit_of_measurement': 'Pack', 'category': 'Snacks', 'discount': 0},
            {'name': 'Soda', 'desc': 'Cold soda drinks', 'price_per_unit': 60.00, 'stock': 500, 'unit_of_measurement': 'Bottle', 'category': 'Beverages', 'discount': 0},
            {'name': 'Juice', 'desc': 'Fresh fruit juice', 'price_per_unit': 90.00, 'stock': 0, 'unit_of_measurement': 'Bottle', 'category': 'Beverages', 'discount': 10},
            {'name': 'Tea', 'desc': 'Herbal tea', 'price_per_unit': 125.00, 'stock': 150, 'unit_of_measurement': 'Box', 'category': 'Beverages', 'discount': 5},
            {'name': 'Coffee', 'desc': 'Ground coffee beans', 'price_per_unit': 150.00, 'stock': 100, 'unit_of_measurement': 'Pack', 'category': 'Beverages', 'discount': 0},
            {'name': 'Lemonade', 'desc': 'Fresh lemonade', 'price_per_unit': 75.00, 'stock': 200, 'unit_of_measurement': 'Bottle', 'category': 'Beverages', 'discount': 15},
            {'name': 'Water', 'desc': 'Bottled drinking water', 'price_per_unit': 30.00, 'stock': 1000, 'unit_of_measurement': 'Bottle', 'category': 'Beverages', 'discount': 0},
            {'name': 'Coconut Water', 'desc': 'Natural coconut water', 'price_per_unit': 110.00, 'stock': 180, 'unit_of_measurement': 'Bottle', 'category': 'Beverages', 'discount': 10},
        ]


        # Assign products to categories
        for product_data in products:
            category_name = product_data['category']
            category = Category.query.filter_by(name=category_name).first()
            
            product = Product(
                name=product_data['name'],
                desc=product_data['desc'],
                price_per_unit=product_data['price_per_unit'],
                stock=product_data['stock'],
                unit_of_measurement=product_data['unit_of_measurement'],
                category_id=category.id,
                is_status="Active"
            )
            db.session.add(product)

        db.session.commit()
'''





def role_required(required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(name=current_user).first()
            user_roles = [role.name for role in user.roles]
            if not any(role in user_roles for role in required_roles):
                return jsonify({'message': f'Access denied. One of {required_roles} roles required.'}), 403
            g.user_id = user.id
            return fn(*args, **kwargs)
        return wrapper
    return decorator


manager_required = role_required(['manager'])
admin_required = role_required(['admin'])


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role_name = data.get('role')
        print(role_name)
        if not name or not email or not password or not role_name:
            return jsonify({'error': 'Incomplete data provided'}), 400

        existing_user = User.query.filter_by(name=name).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            return jsonify({'error': 'name already exists'}), 409
        if existing_email:
            return jsonify({'error': 'Email already exists'}), 409

        role = Role.query.filter_by(name=role_name).first()
        print(role)
        if not role:
            role = Role(name=role_name)
            db.session.add(role)

        new_user = User( name=name, email=email, password=password)
        if role_name == 'manager':
            new_user.is_status = 'Not Active'
            new_user.is_approved = 'Pending'
        else:
            new_user.is_status = 'Active'
            new_user.is_approved = 'Approved'
        new_user.roles.append(role)

        db.session.add(new_user)
        db.session.commit()  
        return jsonify({'message': 'User created successfully'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        name = data.get('name')
        password = data.get('password')

        if not name or not password:
            return jsonify({'error': 'Incomplete data provided'}), 400

        user = User.query.filter_by(name=name, password=password, is_status='Active',is_approved='Approved').first()
        print(user)
        db.session.commit()
        if user:
            expires_delta = timedelta(hours=2)

            access_token = create_access_token(identity=name, expires_delta=expires_delta)
            return jsonify({
                
                'name': user.name,
                'role': user.roles[0].name if user.roles else 'No Role',
                'access_token': access_token
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials or user is not active'}), 401

    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}),500


def add_sample_data():
    with app.app_context():
        admin_role = Role.query.filter_by(name='admin').first()

        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)

        manager_role = Role.query.filter_by(name='manager').first()
        if not manager_role:
            manager_role = Role(name='manager')
            db.session.add(manager_role)

        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)

        admin_user = User.query.filter_by(name='admin').first()
        if not admin_user:
            admin_user = User(name='admin', email='admin@example.com', password='a',is_status='Active',is_approved='Approved')
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)
        db.session.commit()

@app.route('/admin/users',methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users= User.query.all()
    user_list = []
    for user in users:
        if user.is_approved=="Approved":
            user_data={
                "id":user.id,
                "name":user.name,
                "email":user.email,
                "role":user.roles [0].name if user.roles else "No Role",
            }
            user_list.append(user_data)
    return jsonify(user_list)

@app.route('/admin/users/request',methods=['GET'])
@jwt_required()
@admin_required
def get_users_request():
    users= User.query.all()
    user_list = []
    for user in users:
        if user.is_approved=="Pending":
            user_data={
                "id":user.id,
                
                "name":user.name,
                "email":user.email,
                "role":user.roles [0].name if user.roles else "No Role",
            }
            user_list.append(user_data)
    return jsonify(user_list)


@app.route('/user/approved', methods=['PATCH'])
@jwt_required()
@admin_required
def user_approved():
    try:
        data = request.get_json()
        user_id = data.get('user_id') 
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        user.is_approved = "Approved"
        user.is_status = "Active"
        db.session.commit()

        return jsonify({'message': 'User approved successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500




@app.route('/user/reject', methods=['PATCH'])
@jwt_required()
@admin_required
def user_rejected():
    try:
        data = request.get_json()
        user_id = data.get('user_id') 
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400

        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User approved successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500



@cache.memoize(timeout=60)
@app.route('/admin/categories', methods=['GET'])
@jwt_required()
@admin_required

def get_categories():
    try:
        categories = Category.query.all()
        categories_list = []
        for category in categories:
            category_data = {
                "id": category.id,
                "name": category.name,
                'is_status': category.is_status, 
                'changes_pending': category.changes_pending,
            }
            categories_list.append(category_data)
        return jsonify(categories_list), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500


        

@app.route('/admin/approval-requests', methods=['GET'])
@jwt_required()
@admin_required
def get_approval_requests():
    try:
        approval_requests = CategoryUpdate.query.all()
        requests_list = []

        for request in approval_requests:
            request_data = {
                'id': request.id,
                'new_name': request.new_name,
                'action': request.action,
                'is_approved': request.is_approved,
            }
            requests_list.append(request_data)

        return jsonify(requests_list), 200

    except Exception as e:
        print(f"Error fetching approval requests: {e}")
        return jsonify({'error': f'An unexpected error occurred while fetching approval requests: {str(e)}'}), 500


@app.route('/admin/accept_approval/<int:id>', methods=['PATCH'])
@jwt_required()
@admin_required
def accept_approval(id):
    try:
        category_update = CategoryUpdate.query.get(id)

        if not category_update:
            return jsonify({'error': 'Category update not found'}), 404

        if category_update.is_approved == 'completed':
            return jsonify({'message': 'Approval has already been completed'}), 400

        if category_update.action in ['enable', 'disable']:
            new_status = 'Active' if category_update.action == 'enable' else 'Inactive'
            category_update.is_approved = 'completed'

            category = Category.query.filter_by(id=category_update.category_id).first()

            if category:
                category.is_status = new_status
                db.session.commit()

        elif category_update.action == 'add':
            category_update.is_approved = 'completed'
            category = Category(
                    name=category_update.new_name,
                    is_status='Active', 
                )
            db.session.add(category)
            db.session.commit()
         

        elif category_update.action == 'edit':
            category = Category.query.filter_by(id=category_update.category_id).first()
            print(category)
            if category:
                print(category.name)
                print(category_update.new_name)
                category.name = category_update.new_name 
                category_update.is_approved = 'completed'
                db.session.commit()
            
        else:
            return jsonify({'error': 'Invalid action'}), 400
        return jsonify({'message':'Request approved Successfully'})


    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/admin/reject_approval/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def reject_approval(id):
    try:
        category_update = CategoryUpdate.query.get(id)
        print(f"Attempting to reject approval for ID: {id}")
        if not category_update:
            return jsonify({'error': 'Category update not found'}), 404

        if category_update.is_approved == 'completed':
            return jsonify({'message': 'Rejection cannot be performed. Approval has already been completed'}), 400
        category_update.is_approved = 'rejected'
        db.session.commit()

        return jsonify({'message': 'Rejection completed successfully'}), 200

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


@app.route('/admin/category', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    data = request.get_json()
    category_name = data.get('name')
    existing_category = Category.query.filter_by(name=category_name).first()
    if existing_category:
        return jsonify({'error':'Category already exists'})

    new_category = Category(name=category_name,is_status='Active')
    db.session.add(new_category)
    db.session.commit()
    cache.delete_memoized(get_categories)

    return jsonify({'message': 'Category created successfully','id': new_category.id })

@app.route('/admin/categories/<int:category_id>', methods=['PUT', 'GET', 'PATCH'])
@jwt_required()
@admin_required
def update_category(category_id):
    try:
        current_user_name = get_jwt_identity()

        if request.method == 'GET':
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Category not found'})
            return jsonify({
                'id': category.id,
                'name': category.name,
            })

        elif request.method == 'PUT':
            data = request.get_json()
            new_name = data.get('name')

            category = Category.query.get(category_id)

            if not category:
                return jsonify({'error': 'Category not found'})

            category.name = new_name
            category.changes_pending = False
            db.session.commit()

            return jsonify({'message': 'Category updated successfully'})

        elif request.method == 'PATCH':
            data = request.get_json()
            action = data.get('action') 

            category = Category.query.get(category_id)
    
            if not category:
                return jsonify({'error': 'Category not found'}), 404

            if action == 'enable':
                category.is_status = 'Active'
                Product.query.filter_by(category_id=category.id).update({'is_status': 'Active'})
            elif action == 'disable':
                category.is_status = 'Inactive'
                Product.query.filter_by(category_id=category.id).update({'is_status': 'Inactive'})
            else:
                return jsonify({'error': 'Invalid action'}), 400

            db.session.commit()

            return jsonify({'message': f'Category {action}d successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/admin/products/<int:category_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_products_by_category(category_id):
    try:
        products = Product.query.filter_by(category_id=category_id).all()
        product_list = []
        for product in products:
            product_list.append({
                'product_id': product.id,'name': product.name,'desc': product.desc,'stock': product.stock,
                'price_per_unit': product.price_per_unit,'category': product.category.name,'category_id': product.category_id,'exp': product.expiry_date,
                'mfg': product.mfg_date,'sold': product.sold,
                'is_status': product.is_status,'discount':product.discount})
        return jsonify(product_list), 200
    
    except Exception as e:
        error_message = f"Error retrieving products by category: {e}"
        return jsonify({'error': error_message}), 500




@app.route('/manager/products', methods=['GET'])
@jwt_required()
@manager_required
def get_products():
    try:
        products = Product.query.all()
        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'desc': product.desc,
                'stock': product.stock,
                'price_per_unit': product.price_per_unit,
                'category_id': product.category_id,
                'expiry_date': product.expiry_date,
                'mfg_date': product.mfg_date,
                'sold': product.sold,
                'is_status': product.is_status,
                'unit_of_measurement': product.unit_of_measurement,
                'discount':product.discount
            }
            product_list.append(product_data)
        return jsonify(product_list), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/manager/products/<int:product_id>', methods=['GET','PATCH'])
@jwt_required()
@manager_required
def enable_disable_product(product_id):
    if request.method == 'GET':
        try:
            product = Product.query.get(product_id)

            if not product:
                return jsonify({'error': 'Product not found'}), 404

            product_data = {
                'product_id': product.id,
                'name': product.name,
                'desc': product.desc,
                'stock': product.stock,
                'price_per_unit': product.price_per_unit,
                'category_id': product.category_id,
                'expiry_date': product.expiry_date,
                'mfg_date': product.mfg_date,
                'is_status': product.is_status,
                'unit_of_measurement': product.unit_of_measurement,
                'discount':product.discount
            }

            return jsonify(product_data), 200

        except Exception as e:
            print(e)
            return jsonify({'error': 'An unexpected error occurred'}), 500

    elif request.method == 'PATCH':
        try:
            
            data = request.get_json()
            action = data.get('action') 

            product = Product.query.get(product_id)

            if not product:
                return jsonify({'error': 'Product not found'}), 404

            if action == 'Active':
                product.is_status = 'Active'
            elif action == "Inactive":
                product.is_status = 'Inactive'
            else:
                return jsonify({'error': 'Invalid action'}), 400

            db.session.commit()

            return jsonify({'message': f'Product {action}d successfully'}), 200

        except Exception as e:
            print(e)
            return jsonify({'error': 'An unexpected error occurred'}), 500



@app.route('/manager/product_create', methods=['POST'])
@jwt_required()
@manager_required
def add_product():
    try:
        data = request.get_json()
        print(data)
        name = data.get('name')
        discount = (data.get('discount'))
        desc = data.get('desc')
        stock = (data.get('stock'))
        price_per_unit = (data.get('price_per_unit'))
        category_id = data.get('category_id')
        expiry_date =  (data.get('expiry_date'))
        mfg_date =  (data.get('mfg_date'))
        unit = data.get('unit')
        print(expiry_date )
        print(name)
        if not name:
            return jsonify({'message': 'Name is required'}), 400

        
        stock = int(stock) if stock is not None else None
        price_per_unit = int(price_per_unit) if price_per_unit is not None else None
        if expiry_date!="":
            expiry_date = parse_date(expiry_date) 
        else :
            expiry_date=None
        if mfg_date!="":
        
            mfg_date = parse_date(mfg_date) 
        else :
            mfg_date=None


        existing_product = Product.query.filter(Product.name.ilike(name)).first()

        print('existing_product')
        if existing_product:
            return jsonify({'message': 'Product with the same name already exists'}), 400
            flash('product with same name exits')
        
        new_item = Product(name=name, unit_of_measurement=unit,
            is_status='Active', desc=desc, stock=stock, price_per_unit=price_per_unit,
            category_id=category_id, expiry_date=expiry_date, mfg_date=mfg_date,discount = discount)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201

    except ValueError:
        return jsonify({'message': 'Invalid data format. Check the data types.'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error adding product: {str(e)}'}), 500

@app.route('/manager/edit_products/<int:id>', methods=['PUT'])
@jwt_required()
@manager_required
def update_product(id):
    try:
        data = request.get_json()
        product = Product.query.get(id)
        print(f"Received data: {data}")
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product.name = data.get('name', product.name)
        product.desc = data.get('desc', product.desc)
        product.stock = data.get('stock', product.stock)
        product.discount = data.get('name', product.discount)
        product.price_per_unit = data.get('price_per_unit', product.price_per_unit)
        product.category_id = data.get('category_id', product.category_id)
        product.sold = data.get('sold', product.sold)
        product.is_status = data.get('is_status', product.is_status)
        product.unit_of_measurement = data.get('unit_of_measurement', product.unit_of_measurement)

        db.session.commit()

        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        print(e)
        return jsonify({'error': 'An unexpected error occurred'}), 500



@app.route('/manager/add_category', methods=['POST'])
@jwt_required()
@manager_required
def manager_add_category():
    try:
        new_name = request.form.get('name')
        print(new_name)
        if not new_name:
            return jsonify({'message': 'Name required'}), 400
        existing_category = Category.query.filter(Category.name.ilike(new_name)).first()
        if existing_category:
            return jsonify({'message': 'Category name already exists'}), 400
        else:
            category_update = CategoryUpdate(
                new_name=new_name,
                new_is_status='Active',
                action='add',
                is_approved='Pending'
            )

            db.session.add(category_update)
            db.session.commit()

            return jsonify({'message': 'Category added. Awaiting admin approval.'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/manager/categories', methods=['GET'])
@jwt_required()
@manager_required
def manager_get_categories():
    try:
        categories = Category.query.all()
        categories_list = []
        for category in categories:
            categories_list.append({
                'id': category.id,'name': category.name,
                'is_status': category.is_status,'changes_pending': category.changes_pending})
        return jsonify(categories_list)
    
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/manager/categories/<int:category_id>', methods=['GET'])
@jwt_required()
@manager_required
def manager_get_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'message': 'Category not found'}), 404

        category_details = {
            'id': category.id,'name': category.name,'is_status': category.is_status,
            'changes_pending': category.changes_pending,'approved': 'Pending' if category.changes_pending else 'Approved',
            }
        return jsonify(category_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/manager/edit_category/<int:category_id>', methods=['PUT'])
@jwt_required()
@manager_required
def manager_edit_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'message': 'Category not found'}), 404
        new_name = request.form.get('name')
        
        if not new_name or new_name == category.name:
            return jsonify({'message': 'No changes made or same name as before'}), 200
    
        else:
            category_update = CategoryUpdate(category_id=category_id,
            new_name=new_name,new_is_status=category.is_status,
            action='edit',is_approved='Pending')      
            db.session.add(category_update)
            category.changes_pending = True
            db.session.commit()
        return jsonify({'message': 'Category updated. Awaiting admin approval.'}), 200

    except Exception as e:
        db.session.rollback() 
        return jsonify({'error': str(e)}), 500


@app.route('/manager/update_category/<int:category_id>', methods=['PATCH'])
@jwt_required() 
@manager_required
def manager_update_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        action = request.json.get('action')
        if not action or action not in ['enable', 'disable']:
            return jsonify({'error': 'Invalid action. Use "approve" or "reject".'}), 400
        category_update = CategoryUpdate(category=category,
            new_name=category.name,
            action=action,is_approved='Pending')
        db.session.add(category_update)
        category.changes_pending = True  
        db.session.commit()
        return jsonify({'message': f'Category {action}d. Awaiting admin approval.'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating category: {str(e)}'}), 500


@app.route('/user/products', methods=['GET'])
def user_products():
    try:
        products = Product.query.all()
        products_list = []

        for product in products:
            if product.is_status == "Active":
                product_data = {
                    'product_id': product.id,
                    'name': product.name,
                    'desc': product.desc,
                    'stock': product.stock,
                    'price_per_unit': product.price_per_unit,
                    'category': product.category.name if product.category else None,
                    'exp': product.expiry_date,
                    'mfg': product.mfg_date,
                    'sold': product.sold,
                    'is_status': product.is_status,
                    'category_id': product.category_id,
                    'unit_of_measurement': product.unit_of_measurement
                }
                products_list.append(product_data)

        return jsonify(products_list), 200

    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({'error': f'An unexpected error occurred while fetching products: {str(e)}'}), 500

@app.route('/user/search_products', methods=['POST'])

def search_products():
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        searchterm = data.get('searchterm')
        print(f"Received data: {searchterm}")
        
        if not searchterm:
            return jsonify({'message': 'No item searched'}), 400
        else:
            print(f"Searching for term: {searchterm}") 
            Products = Product.query.filter(
                or_(
                    Product.name.ilike(f'%{searchterm}%'),  # Search by name
                    Product.price_per_unit.ilike(f'%{searchterm}%'),  # Or search by category
                    Product.category.has(Category.name.ilike(f'%{searchterm}%'))    #can't use product.category.name as in backpopulate without fetching product we can't use this 
                )
            ).all()
            if not Products:
                return jsonify({'message': 'No items matched'}), 404
            else:
                result = []
                for product in Products:
                    result.append({
                        'id': product.id,
                        'name': product.name,
                        'price_per_unit':product.price_per_unit,
                        'unit_of_measurement':product.unit_of_measurement,
                        'stock':product.stock,
                        'category_id': product.category.id
                    })
                return jsonify({'result': result})

    except Exception as e:
        print(f"Error searching products: {str(e)}")
        return jsonify({'error': 'Error searching products'}), 500



@app.route('/user/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    try:
        current_user_name = get_jwt_identity()

        if current_user_name is None:
            return jsonify({'error': 'Invalid name from JWT token'}), 401

        user = User.query.filter_by(name=current_user_name).first()
        print(user.id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        print(type(quantity))
        product = Product.query.get(product_id)
        print(product)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        cart = Cart.query.filter_by(product_id=product_id,user_id=user.id).first()
        print(cart)
        if product.stock>0 :
            if cart and cart.user_id==user.id and cart.product_id == product_id:
                cart.quantity = cart.quantity + int(quantity)
                total_amount=int(product.price_per_unit)*int(quantity)

                print(quantity)
                print(product.stock)
                print('Updating existing cart quantity:', cart.quantity)
                db.session.commit()
            else:
                cart_item = Cart(
                    user_id=int(user.id),
                    product_id=product.id,
                    quantity=int(quantity),
                    total_amount=int(product.price_per_unit)*int(quantity),
                    price=int(product.price_per_unit),
                    is_status='Not Active'
                )
                db.session.add(cart_item)
                db.session.commit()  
                print('Adding new cart item to the database')

        return jsonify({'message': 'Item added to cart successfully'}), 200

    except Exception as e:
        print(f"Error adding item to cart: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
 

@app.route('/user/cart', methods=['GET'])
@jwt_required()
def get_user_cart():
    try:
        current_user_name = get_jwt_identity()
        if current_user_name is None:
            return jsonify({'error': 'Invalid name from JWT token'}), 401
        user = User.query.filter_by(name=current_user_name).first()
        print(user)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        cart_items = Cart.query.filter(Cart.user_id == user.id).all()
        print(cart_items)
        cart_data = []
        for cart_item in cart_items:
            product = Product.query.filter(Product.id == cart_item.product_id).first()
            print(product.stock>=cart_item.quantity)
            if product :
                cart_data.append({
                    'id': cart_item.id,
                    'product': {'id': product.id, 'name': product.name, 'stock': product.stock,},
                    'quantity': cart_item.quantity,
                    'price': cart_item.price,
                    'total_amount': cart_item.total_amount
                })

        print(f"Cart Data: {cart_data}")

        return jsonify(cart_data), 200

    except Exception as e:
        print(f"Error fetching cart items: {e}")
        return jsonify({'error': f'An unexpected error occurred while fetching cart items: {str(e)}'}), 500

@app.route('/user/remove', methods=['DELETE'])
@jwt_required()
def remove_cart():
    try:
        current_user_name = get_jwt_identity()

        if current_user_name is None:
            return jsonify({'error': 'Invalid name from JWT token'}), 401
        user = User.query.filter_by(name=current_user_name).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        product_id = data.get('product_id')
        product=Product.query.get(product_id)
        cart_item = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()
        if not cart_item: 
            return jsonify({'error': 'Product not found in the cart'}), 404
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({'message': 'Product removed from the cart successfully'}), 200
    except Exception as e:
        print(f"Error removing product from the cart: {e}")
        return jsonify({'error': f'An unexpected error occurred while removing product from the cart: {str(e)}'}), 500

@app.route('/user/buy_all', methods=['POST'])
@jwt_required()
def buy_all():
    try:
        current_user_name = get_jwt_identity()
        if current_user_name is None:
            return jsonify({'error': 'Invalid name from JWT token'}), 401
        user = User.query.filter_by(name=current_user_name).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        cart = Cart.query.filter_by(user_id=user.id).all()
        order_date = datetime.now()

        for cart_product in cart:
            product = Product.query.get(cart_product.product_id)
            if product.stock > 0 and product.stock >= cart_product.quantity:
                order = Order(
                    order_date=order_date,
                    user_id=cart_product.user_id,
                    total_amount=cart_product.total_amount,
                    order_is_status='Completed'
                )

                product.stock -= cart_product.quantity

                
                db.session.add(order)
                db.session.flush()
                order_product = Orderproduct(
                    order_id=order.id,
                    product_id=cart_product.product_id,
                    quantity=cart_product.quantity,
                    price=cart_product.price
                )
                db.session.add(order_product)
            db.session.delete(cart_product)   

        db.session.commit()

        return jsonify({'message': 'Items purchased successfully'}), 200

    except Exception as e:
        print(f"Error buying items: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/user/buy', methods=['POST'])
@jwt_required()
def buy():
    try:
        current_user_name = get_jwt_identity()
        if current_user_name is None:
            return jsonify({'error': 'Invalid name from JWT token'}), 401
        
        data = request.get_json()
        
        product_id = data.get('product_id')
        print(product_id)

        user = User.query.filter_by(name=current_user_name).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        order_date = datetime.now()
        product = Product.query.filter_by(id=product_id).first()
        print(product)
        cart = Cart.query.filter_by(user_id=user.id,product_id=product.id).first()
        print(cart)
        if product.stock > 0 and product.stock >= cart.quantity:
            order = Order(
                order_date=order_date,
                user_id=cart.user_id,
                total_amount=cart.total_amount,
                order_is_status='Completed'
            )

            product.stock -= cart.quantity
            db.session.add(order)
            db.session.flush()
            order_product = Orderproduct(
                order_id=order.id,
                product_id=cart.product_id,
                quantity=cart.quantity,
                price=cart.price
            )
            db.session.add(order_product)
                
        db.session.delete(cart)
        db.session.commit()

        return jsonify({'message': 'Items purchased successfully'}), 200

    except Exception as e:
        print(f"Error buying items: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/user/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    current_user_name = get_jwt_identity()
    print(current_user_name)
    user = User.query.filter_by(name=current_user_name).first()
    print(user)
    user_orders = Order.query.filter_by(user_id=user.id).all()
    print(user_orders)
    orders_data = []

    for order in user_orders:
        order_data = {
            'id': order.id,
            'order_date': order.order_date.strftime('%Y-%m-%d'),
            'total_amount': order.total_amount,
            'order_is_status': order.order_is_status,
            'order_product': [{
                'id': order_product.id,
                'product': {
                    'id': order_product.product.id,
                    'name': order_product.product.name,
                    'desc': order_product.product.desc,
                    'price_per_unit': order_product.product.price_per_unit,
                },
                'quantity': order_product.quantity,
                'price': order_product.price,
            } for order_product in order.order_product],
        }
        orders_data.append(order_data)

    return jsonify(orders_data)


@celery.task()
def generate_csv():
    try:
        with app.app_context():
            products = Product.query.all()
            filename = 'products.csv'
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Description", "Manufacture", "Expiry", "Rate Per Unit", "Stock Remaining", "Units Sold", "Status"])
                for product in products:
                    writer.writerow([product.name, product.desc, product.mfg_date, product.expiry_date, product.price_per_unit, product.stock, product.sold, product.is_status])
            return filename
    except Exception as e:
        return jsonify({'error': f'Error generating csv: {str(e)}'}), 500


@app.route('/manager/generate_monthly_report', methods=['GET'])
@jwt_required()
def download_csv():
    try:
        task = generate_csv.delay()
        task.wait()
        response=send_file(task.result,as_attachment=True)
        return(response)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500


def get_inactive_users():
    time_24_hours_ago = datetime.now() - timedelta(hours=24)
    inactive_users = User.query.join(User.roles).filter(
        and_(
            Role.name == 'user',
            or_(
                User.last_login.is_(None),
                User.last_login < time_24_hours_ago,
                ~User.order.any()
                ))).all() 
    return inactive_users


@celery.task(name = 'daily_reminder')
def daily_reminder():
    users = get_inactive_users()
    with app.app_context():
        for user in users:
            sub = "Reminder 🔔"
            body = "Dear User, You have not purchased anything today.Please visit our store"
            send_mail(user.email, sub, body)


@app.template_filter('get_product_name')
def get_product_name(product_id):
    product = Product.query.get(product_id)
    return product.name if product else ''


def generate_report(user):
    now = datetime.utcnow()
    one_month_ago = now - timedelta(days=30)
    orders = Order.query.filter(Order.user_id == user.id, Order.order_date >= one_month_ago).all()
    total_spent = sum(order.total_amount for order in orders)
    print(total_spent)
    template_string = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Monthly Report</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 20px;
                }
                h1 {
                    color: #333;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }
                .order-items-table {
                    margin-top: 10px;
                }
                .recipients {
                    margin-top: 20px;
                }
                .thank-you-note {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Hi {{ user.name }} !!</h1>
            <h3>Here is your monthly report.</h3>
            <div class="recipients">
                <h2>Recipients:</h2>
                <ul>
                    <li>{{ user.email }}</li>
                    <!-- Add more recipients if needed -->
                </ul>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Order Date</th>
                        <th>Total Amount</th>
                        <th>Order Items</th>
                    </tr>
                </thead>
                <tbody>{% set total_spent = 0 %}
                    {% for order in orders %}
                        <tr>
                            <td>{{ order.id }}</td>
                            <td>{{ order.order_date }}</td>
                            <td>{{ order.total_amount }}</td>
                            <td>
                                <table class="order-items-table">
                                    <thead>
                                        <tr>
                                            <th>product Name</th>
                                            <th>Quantity</th>
                                            <th>Price</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for product in order.order_product %}
                                            <tr>
                                                <td>{{ product.product.name }}</td>
                                                <td>{{ product.quantity }}</td>
                                                <td>{{ product.price }}</td>
                                            </tr>
                                           
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
            <div class="thank-you-note">
                <p>Total amount spent this month: {{ spent }}</p>
                <p>Thank you for your continued support!</p>
            </div>
        </body>
        </html>
        """
    template = Template(template_string)
    html_content = template.render(user=user, orders=orders, spent=total_spent)
    return html_content


@celery.task(name='monthly_report')
def monthly_report():
    users = User.query.join(User.roles).filter(and_(Role.name == 'user')).all()
    with app.app_context():
        for user in users:
            try:
                sub = "Monthly Report"
                body = generate_report(user)
                send_mail(user.email, sub, body)
            except Exception as e:
                app.logger.error(f"Error sending monthly report for user {user.id}: {e}")

if __name__ == '__main__':
    create_and_insert_data()
    add_sample_data()

    app.run(debug=True)
