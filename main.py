# Post == Create
# Get == Read
# Put == Update
# Delete == Delete

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create Databse
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel.db"
db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float(), nullable=False)

    def to_dict(self):
        return {
            "id" : self.id,
            "destination" : self.destination,
            "country" : self.country,
            "rating" : self.rating
        }
    
with app.app_context():
    db.create_all()

# Crate Routes   
# https://www.alperseyman.io/
@app.route('/')
@app.route('/home')
def home_page():
    
    return jsonify({"message":"Welcome to the Travel API"})


# https://www.alperseyman.io/destinations
@app.route('/destinations', methods=["GET"])
def destinations_page():
    
    destinations = Destination.query.all()

    destinations_list = [destination.to_dict() for destination in destinations]

    return jsonify(destinations_list)

# GET -- read
# https://www.alperseyman.io/destinations/2 --> (id)
@app.route('/destinations/<int:destination_id>', methods=["GET"])
def get_destination(destination_id):
    
    destination = Destination.query.get(destination_id)

    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not found!"}), 404

# POST -- craate
@app.route('/destinations', methods=["POST"])
def add_destination():

    data = request.get_json() # convert JSON to python dict.

    destination = Destination(destination=data["destination"], country=data["country"], rating=data["rating"])

    db.session.add(destination)
    db.session.commit()

    return jsonify(destination.to_dict()), 201


# PUT -- update
@app.route('/destinations/<int:destination_id>', methods=["PUT"])
def update_destination(destination_id):
    
    data = request.get_json() # conver JSON to python dict.

    destination = Destination.query.get(destination_id)

    if destination:
        destination.destination = data["destination"]
        destination.country = data["country"]
        destination.rating = data["rating"]

        db.session.commit()
        return jsonify(destination.to_dict()), 201
    
    return jsonify({"error": "Destination not found!"}), 401

# DELETE -- delete
@app.route('/destinations/<int:destination_id>', methods=["DELETE"])
def delete_destination(destination_id):
    
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()

        return jsonify({"message":"Destination was deleted!.."})
    
    return jsonify({"error":"Destination not found!"})

if __name__ == "__main__":
    app.run(debug=True)