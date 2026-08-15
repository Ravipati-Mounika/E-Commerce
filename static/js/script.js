document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "ShopSphere loaded successfully"
        );

        const alerts =
            document.querySelectorAll(
                ".alert"
            );

        alerts.forEach(function (alert) {

            setTimeout(function () {

                alert.style.opacity = "0";

                setTimeout(function () {
                    alert.remove();
                }, 500);

            }, 3000);

        });

    }
);


/*
    REST API example
*/

async function loadProducts() {

    try {

        const response =
            await fetch("/api/products");

        const products =
            await response.json();

        console.log(
            "Products from REST API:",
            products
        );

    } catch (error) {

        console.error(
            "API Error:",
            error
        );

    }
}