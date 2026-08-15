from flask import Blueprint, jsonify, request
from models import db
from models.product import Product
from models.user import User

api = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@api.route("/products", methods=["GET"])
def get_products():

    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "category": p.category,
            "stock": p.stock,
            "image": p.image
        }
        for p in products
    ])


@api.route(
    "/products/<int:id>",
    methods=["GET"]
)
def get_product(id):

    product = Product.query.get_or_404(id)

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "image": product.image
    })


@api.route(
    "/products",
    methods=["POST"]
)
def create_product():

    data = request.get_json()

    product = Product(
        name=data["name"],
        description=data.get(
            "description",
            ""
        ),
        price=float(data["price"]),
        category=data.get(
            "category",
            "General"
        ),
        stock=int(
            data.get("stock", 0)
        ),
        image=data.get(
            "image",
            "default.jpg"
        )
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created",
        "id": product.id
    }), 201


@api.route(
    "/products/<int:id>",
    methods=["PUT"]
)
def update_product(id):

    product = Product.query.get_or_404(id)

    data = request.get_json()

    product.name = data.get(
        "name",
        product.name
    )

    product.description = data.get(
        "description",
        product.description
    )

    product.price = data.get(
        "price",
        product.price
    )

    product.category = data.get(
        "category",
        product.category
    )

    product.stock = data.get(
        "stock",
        product.stock
    )

    db.session.commit()

    return jsonify({
        "message": "Product updated"
    })


@api.route(
    "/products/<int:id>",
    methods=["DELETE"]
)
def delete_product(id):

    product = Product.query.get_or_404(id)

    db.session.delete(product)

    db.session.commit()

    return jsonify({
        "message": "Product deleted"
    })


@api.route(
    "/users",
    methods=["GET"]
)
def users():

    users = User.query.all()

    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
        for user in users
    ])