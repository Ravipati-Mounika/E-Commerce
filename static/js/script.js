fetch("/api/products")
.then(response => response.json())
.then(products => {

    let output = "";

    products.forEach(product => {

        output += `
            <div class="product">
                <h3>${product.name}</h3>

                <p>${product.description}</p>

                <b>₹${product.price}</b>

                <br><br>

                <button onclick="addCart(${product.id})">
                    Add to Cart
                </button>
            </div>
        `;
    });

    document.getElementById("products").innerHTML = output;
});


function addCart(id) {

    let cart = JSON.parse(
        localStorage.getItem("cart")
    ) || [];

    cart.push(id);

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

    alert("Product added to cart");
}