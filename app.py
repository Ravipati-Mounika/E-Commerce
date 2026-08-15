from flask import Flask, render_template
from flask_cors import CORS
from models.db import init_db
from routes.auth import auth
from api.products import products_api

app = Flask(__name__)
app.secret_key = "secret123"

CORS(app)

init_db()

app.register_blueprint(auth)
app.register_blueprint(products_api, url_prefix="/api")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/orders")
def orders():
    return render_template("orders.html")

if __name__ == "__main__":
    app.run(debug=True)