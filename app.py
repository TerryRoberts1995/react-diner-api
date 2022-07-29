from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    
    def __init__(self, menu_type, title, price):
        self.menu_type = menu_type
        self.title = title
        self.price = price

class FoodSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "price", "menu_type")

food_schema = FoodSchema()
multiple_food_schema = FoodSchema(many=True)

@app.route("/food/add", methods=["POST"])
def add_food():
    post_data = request.get_json()
    title = post_data.get("title")
    price = post_data.get("price")
    menu_type = post_data.get("type")

    new_record = Food(menu_type, title, price)
    db.session.add(new_record)
    db.session.commit()

    return jsonify("Food item added successfully")

@app.route("/food/get", methods=["GET"])
def get_all_food():
    records = db.session.query(Food).all()
    return jsonify(multiple_food_schema.dump(records))

@app.route("/food/get/<menu_type>", methods=['GET'])
def get_items_by_type(menu_type):
    records = db.session.query(Food).filter(Food.menu_type == menu_type).all()
    return jsonify(multiple_food_schema.dump(records))

if __name__ == "__main__":
    app.run(debug=True)