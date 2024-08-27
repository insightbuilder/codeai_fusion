from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)


# Product Schema
class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Create a Product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    price = request.json["price"]

    new_product = Product(name=name, price=price)
    try:
        db.session.add(new_product)
        db.session.commit()
    except IntegrityError:
        return jsonify({"message": "Product already exists"}), 400

    return product_schema.jsonify(new_product), 201


# Get All Products
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products), 200


# Get Single Product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return product_schema.jsonify(product), 200
    else:
        return jsonify({"message": "Product not found"}), 404


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5001)
