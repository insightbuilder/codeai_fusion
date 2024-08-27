from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# from marshmallow_sqlalchemy import ModelSchema
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# Order Schema
class OrderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Order


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


# Create an Order
@app.route("/order", methods=["POST"])
def add_order():
    product_id = request.json["product_id"]
    quantity = request.json["quantity"]

    # Verify product exists
    product_response = requests.get(f"http://localhost:5001/product/{product_id}")
    if product_response.status_code != 200:
        return jsonify({"message": "Product not found"}), 404

    new_order = Order(product_id=product_id, quantity=quantity)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order), 201


# Get All Orders
@app.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders), 200


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
