from flask import Flask, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from functools import wraps
from models import User, Book, Review


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_recommendations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Add your own secret key here
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based sessions
CORS(app)
Session(app)


# Decorator for protecting routes that require authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message='Unauthorized'), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message='Username already exists')
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(message='User registered successfully')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['user_id'] = user.id  # Store the user ID in the session
        return jsonify(message='User logged in successfully')
    
    return jsonify(message='Invalid username or password')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # Remove the user ID from the session
    return jsonify(message='User logged out successfully')


@app.route('/books', methods=['GET'])
@login_required
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description
        }
        book_list.append(book_data)
    
    return jsonify(books=book_list)


@app.route('/books', methods=['POST'])
@login_required
def create_book():
    data = request.get_json()
    title = data['title']
    author = data['author']
    description = data['description']
    
    new_book = Book(title=title, author=author, description=description)
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify(message='Book created successfully')


@app.route('/books/<book_id>', methods=['PUT'])
@login_required
def update_book(book_id):
    data = request.get_json()
    title = data['title']
    author = data['author']
    description = data['description']
    
    book = Book.query.get(book_id)
    if book:
        book.title = title
        book.author = author
        book.description = description
        db.session.commit()
        
        return jsonify(message='Book updated successfully')
    
    return jsonify(message='Book not found')


@app.route('/books/<book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        
        return jsonify(message='Book deleted successfully')
    
    return jsonify(message='Book not found')


@app.route('/books/<book_id>/reviews', methods=['POST'])
@login_required
def add_review(book_id):
    data = request.get_json()
    rating = data['rating']
    comment = data['comment']
    
    book = Book.query.get(book_id)
    if book:
        new_review = Review(rating=rating, comment=comment, book_id=book.id)
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify(message='Review added successfully')
    
    return jsonify(message='Book not found')

@app.route('/books/<book_id>/reviews', methods=['GET'])
@login_required
def get_reviews(book_id):
    book = Book.query.get(book_id)
    if book:
        reviews = Review.query.filter_by(book_id=book.id).all()
        review_list = []
        for review in reviews:
            review_data = {
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment
            }
            review_list.append(review_data)
        
        return jsonify(reviews=review_list)
    
    return jsonify(message='Book not found')

if __name__ == '__main__':
    app.run(debug=True)