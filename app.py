from flask import Flask
from config import Config
from models import db

from routes.auth_routes import auth
from routes.product_routes import products
from routes.cart_routes import cart_routes
from routes.order_routes import orders

from api.api_routes import api


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(products)
    app.register_blueprint(cart_routes)
    app.register_blueprint(orders)

    app.register_blueprint(api)

    with app.app_context():

        from models.user import User
        from models.product import Product
        from models.cart import Cart
        from models.order import Order, OrderItem

        db.create_all()

        create_admin()

        create_products()

    return app


def create_admin():

    from models.user import User

    admin = User.query.filter_by(
        email="admin@ecommerce.com"
    ).first()

    if not admin:

        admin = User(
            name="Admin",
            email="admin@ecommerce.com",
            role="admin"
        )

        admin.set_password(
            "admin123"
        )

        db.session.add(admin)

        db.session.commit()


def create_products():

    from models.product import Product

    if Product.query.count() > 0:
        return

    sample_products = [

        Product(
            name="Premium Headphones",
            description="Wireless noise cancelling headphones.",
            price=2999,
            category="Electronics",
            stock=25,
            image="headphones.jpg"
        ),

        Product(
            name="Smart Watch",
            description="Fitness tracking smart watch.",
            price=2499,
            category="Electronics",
            stock=30,
            image="watch.jpg"
        ),

        Product(
            name="Running Shoes",
            description="Comfortable sports running shoes.",
            price=1999,
            category="Fashion",
            stock=40,
            image="shoes.jpg"
        ),

        Product(
            name="Laptop Backpack",
            description="Water resistant laptop backpack.",
            price=1299,
            category="Accessories",
            stock=20,
            image="bag.jpg"
        ),

        Product(
            name="Bluetooth Speaker",
            description="Portable high quality Bluetooth speaker.",
            price=1599,
            category="Electronics",
            stock=35,
            image="speaker.jpg"
        ),

        Product(
            name="Casual T-Shirt",
            description="Premium cotton casual T-shirt.",
            price=699,
            category="Fashion",
            stock=50,
            image="shirt.jpg"
        )

    ]

    db.session.add_all(
        sample_products
    )

    db.session.commit()


app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True
    )