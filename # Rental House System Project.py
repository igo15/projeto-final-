# Rental House System Project

# Estrutura inicial do projeto em Python
# Este script organiza os requisitos para um sistema com 3 camadas e suporte a CRUD.

# 1. Estrutura do projeto:
# - Camada de Apresentação (Cliente): Frontend com HTML e CSS
# - Camada de Negócio (Aplicação): Backend em Python usando Flask
# - Camada de Dados: Banco de dados SQLite

# Requisitos de dependências: Flask, SQLAlchemy

# 2. Estrutura do repositório:
# rental_house_project/
# |-- app/
# |   |-- __init__.py
# |   |-- routes.py
# |   |-- models.py
# |-- templates/
# |   |-- base.html
# |   |-- home.html
# |   |-- add_property.html
# |-- static/
# |   |-- styles.css
# |-- database/
# |   |-- rental.db
# |-- run.py
# |-- README.md

# Configuração inicial do backend em Flask:

# Arquivo: app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicialização do app e configuração do banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/rental.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app

# Arquivo: app/models.py
from . import db

class RentalProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(200), nullable=False)

# Arquivo: app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import RentalProperty

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    properties = RentalProperty.query.all()
    return render_template('home.html', properties=properties)

@bp.route('/add', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        location = request.form['location']

        new_property = RentalProperty(title=title, description=description, price=price, location=location)
        db.session.add(new_property)
        db.session.commit()

        return redirect(url_for('routes.home'))

    return render_template('add_property.html')

# Arquivo: run.py
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Templates:
# Arquivo: templates/base.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rental House</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <header>
        <h1>Rental House System</h1>
        <nav>
            <a href="/">Home</a>
            <a href="/add">Add Property</a>
        </nav>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2025 Rental House System</p>
    </footer>
</body>
</html>
"""

# Arquivo: templates/home.html
"""
{% extends 'base.html' %}

{% block content %}
<h2>Available Properties</h2>
<ul>
    {% for property in properties %}
    <li>
        <h3>{{ property.title }}</h3>
        <p>{{ property.description }}</p>
        <p>Price: ${{ property.price }}</p>
        <p>Location: {{ property.location }}</p>
    </li>
    {% endfor %}
</ul>
{% endblock %}
"""

# Arquivo: templates/add_property.html
"""
{% extends 'base.html' %}

{% block content %}
<h2>Add a New Property</h2>
<form method="POST">
    <label for="title">Title:</label>
    <input type="text" id="title" name="title" required>

    <label for="description">Description:</label>
    <textarea id="description" name="description" required></textarea>

    <label for="price">Price:</label>
    <input type="number" id="price" name="price" step="0.01" required>

    <label for="location">Location:</label>
    <input type="text" id="location" name="location" required>

    <button type="submit">Add Property</button>
</form>
{% endblock %}
"""
