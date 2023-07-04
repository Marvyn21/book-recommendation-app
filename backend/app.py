from flask import Flask, jsonify
from flask_cors import CORS
from models import db, Book

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Routes
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description} for book in books]
    return jsonify(book_list)

# Add more routes as needed

# Create database tables if they don't exist
@app.cli.command()
def create_db():
    with app.app_context():
        db.create_all()
    print('Database tables created')

if __name__ == '__main__':
    app.run(debug=True)