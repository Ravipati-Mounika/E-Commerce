from flask import Blueprint, request, jsonify
from models.db import get_db

products_api = Blueprint("products_api", __name__)


# READ
@products_api.route("/products", methods=["GET"])
def get_products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products").fetchall()

    return jsonify([dict(p) for p in products])


# CREATE
@products_api.route("/products", methods=["POST"])
def add_product():
    data = request.json

    conn = get_db()
    conn.execute(
        "INSERT INTO products(name,price,description) VALUES(?,?,?)",
        (data["name"], data["price"], data["description"])
    )
    conn.commit()

    return jsonify({"message": "Product added"})


# UPDATE
@products_api.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.json

    conn = get_db()
    conn.execute("""
        UPDATE products
        SET name=?, price=?, description=?
        WHERE id=?
    """, (
        data["name"],
        data["price"],
        data["description"],
        id
    ))

    conn.commit()

    return jsonify({"message": "Product updated"})


# DELETE
@products_api.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()

    return jsonify({"message": "Product deleted"})