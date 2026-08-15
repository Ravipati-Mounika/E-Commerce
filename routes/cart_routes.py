from flask import Blueprint, redirect, url_for, session, render_template, request, flash
from models import db
from models.cart import Cart
from models.product import Product

cart_routes = Blueprint(
    "cart",
    __name__
)


@cart_routes.route("/cart")
def cart():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    items = Cart.query.filter_by(
        user_id=session["user_id"]
    ).all()

    cart_items = []

    total = 0

    for item in items:

        product = Product.query.get(
            item.product_id
        )

        if product:

            subtotal = (
                product.price *
                item.quantity
            )

            total += subtotal

            cart_items.append({
                "item": item,
                "product": product,
                "subtotal": subtotal
            })

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


@cart_routes.route(
    "/cart/add/<int:product_id>",
    methods=["POST"]
)
def add_to_cart(product_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    product = Product.query.get_or_404(
        product_id
    )

    item = Cart.query.filter_by(
        user_id=session["user_id"],
        product_id=product_id
    ).first()

    if item:

        item.quantity += 1

    else:

        item = Cart(
            user_id=session["user_id"],
            product_id=product_id,
            quantity=1
        )

        db.session.add(item)

    db.session.commit()

    flash(
        f"{product.name} added to cart!"
    )

    return redirect(
        request.referrer or
        url_for("products.product_list")
    )


@cart_routes.route(
    "/cart/update/<int:item_id>",
    methods=["POST"]
)
def update_cart(item_id):

    item = Cart.query.get_or_404(
        item_id
    )

    quantity = int(
        request.form["quantity"]
    )

    if quantity <= 0:

        db.session.delete(item)

    else:

        item.quantity = quantity

    db.session.commit()

    return redirect(
        url_for("cart.cart")
    )


@cart_routes.route(
    "/cart/delete/<int:item_id>"
)
def delete_cart(item_id):

    item = Cart.query.get_or_404(
        item_id
    )

    db.session.delete(item)

    db.session.commit()

    return redirect(
        url_for("cart.cart")
    )