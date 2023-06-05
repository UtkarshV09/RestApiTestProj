from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)  # Initialize Flask application

# Configure SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)  # Initialize SQLAlchemy with app's settings


class Drink(db.Model):  # Defines the Drink model for the ORM
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(80), unique=True, nullable=False)  # Drink name must be unique and provided
    description = db.Column(db.String(120))  # Optional drink description

    def __repr__(self) -> str:  # String representation of the Drink object
        return f"{self.name} - {self.description}"


@app.route('/')  # Home route
def index() -> str:
    return 'Hello!'
 

@app.route('/drinks')  # Endpoint to get all drinks
def get_drinks() -> dict:
    try:
        drinks = Drink.query.all()  # Query all drinks from database

        output = []
        for drink in drinks:
            drink_data = {'name': drink.name, 'description': drink.description} # How the output should look like
            output.append(drink_data)

        return {'drinks': output}
    except SQLAlchemyError:
        return {'error': 'Database error occurred'}

@app.route('/drinks/<id>')  # Endpoint to get a drink by id
def get_drink(id: int) -> dict:
    try:
        drink = Drink.query.get_or_404(id)  # Get drink by id or return 404 error
        return {"name": drink.name, "description": drink.description}
    except SQLAlchemyError:
        return {'error': 'Database error occurred'}

@app.route('/drinks', methods=['POST'])  # Endpoint to add a new drink
def add_drink() -> dict:
    try:
        # Create new Drink object and add it to the database
        drink = Drink(name=request.json['name'], description=request.json['description'])
        db.session.add(drink)
        db.session.commit()  # Save changes to the database
        return jsonify({'id': drink.id, 'name': drink.name, 'description': drink.description})
    except SQLAlchemyError:
        return {'error': 'Database error occurred'}

@app.route('/drinks/<id>', methods=['DELETE'])  # Endpoint to delete a drink by id
def delete_drink(id: int) -> dict:
    try:
        drink = Drink.query.get(id)  # Get drink by id
        if drink is None:  # If drink is not found
            return {'error': "not found"}
        db.session.delete(drink)  # Delete the drink
        db.session.commit()  # Save changes to the database
        return jsonify({'message': "yeet!"})  # Return success message
    except SQLAlchemyError:
        return {'error': 'Database error occurred'}
