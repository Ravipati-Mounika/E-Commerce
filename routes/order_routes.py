from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from models import db
from models.cart import Cart
from models.product import Product
from models.order import Order, OrderItem

orders = Blueprint(
    "orders",
    __name__
)


@orders.route("/checkout")
def checkout():

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
        "checkout.html",
        cart_items=cart_items,
        total=total
    )


@orders.route(
    "/place-order",
    methods=["POST"]
)
def place_order():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    items = Cart.query.filter_by(
        user_id=session["user_id"]
    ).all()

    if not items:

        flash("Your cart is empty")

        return redirect(
            url_for("cart.cart")
        )

    total = 0

    for item in items:

        product = Product.query.get(
            item.product_id
        )

        total += (
            product.price *
            item.quantity
        )

    payment = request.form.get(
        "payment",
        "Cash on Delivery"
    )

    order = Order(
        user_id=session["user_id"],
        total=total,
        payment_method=payment,
        status="Placed"
    )

    db.session.add(order)

    db.session.flush()

    for item in items:

        product = Product.query.get(
            item.product_id
        )

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            price=product.price,
            quantity=item.quantity
        )

        db.session.add(order_item)

        product.stock = max(
            0,
            product.stock - item.quantity
        )

        db.session.delete(item)

    db.session.commit()

    flash(
        "Order placed successfully!"
    )

    return redirect(
        url_for("orders.order_history")
    )


@orders.route("/orders")
def order_history():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_orders = Order.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "orders.html",
        orders=user_orders
    )