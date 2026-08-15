from flask import Blueprint, render_template, request
from models.product import Product

products = Blueprint(
    "products",
    __name__
)


@products.route("/")
def home():

    products_list = Product.query.limit(8).all()

    return render_template(
        "home.html",
        products=products_list
    )


@products.route("/products")
def product_list():

    search = request.args.get(
        "search",
        ""
    )

    category = request.args.get(
        "category",
        ""
    )

    query = Product.query

    if search:

        query = query.filter(
            Product.name.ilike(
                f"%{search}%"
            )
        )

    if category:

        query = query.filter_by(
            category=category
        )

    product_list = query.all()

    categories = db_categories()

    return render_template(
        "products.html",
        products=product_list,
        categories=categories
    )


@products.route("/product/<int:id>")
def product_details(id):

    product = Product.query.get_or_404(id)

    return render_template(
        "product_details.html",
        product=product
    )


def db_categories():

    categories = Product.query.with_entities(
        Product.category
    ).distinct().all()

    return [
        c[0]
        for c in categories
    ]