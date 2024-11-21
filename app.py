from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Ініціалізація додатку
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'  # Підключення до бази даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Вимкнення слідкування за змінами

db = SQLAlchemy(app)


# Створення моделі Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)


# Створення таблиці в базі даних, якщо вона ще не існує
with app.app_context():
    db.create_all()


# Маршрут для створення продукту
@app.route('/product', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully'}), 201


# Маршрут для отримання продукту за id
@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})


# Маршрут для оновлення продукту за id
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)

    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully'})


# Маршрут для видалення продукту за id
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)