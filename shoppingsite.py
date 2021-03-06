"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    basket = []
    cart = session.setdefault("cart", {})
    order_total = 0

    # for each melon in the shopping cart, add its info to the 'basket'
    # list which will get passed to the cart page
    for melon_id in cart:
        melon = melons.get_by_id(int(melon_id))
        quantity = cart[melon_id]
        price = melon.price
        total = quantity * price
        name = melon.common_name

        basket.append((name, quantity, price, total))
        order_total += total


    # TODO: format shopping cart number in cart.html
    # TODO: fix a/an problem in flashed messages

    return render_template("cart.html", cart=basket, order_total=order_total)


@app.route("/add_to_cart/<id1>")
def add_to_cart(id1):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """


    id1 = str(id1)

    # get cart from session or create it if it doesn't already exist
    cart = session.setdefault("cart", {})
    print cart

    # add 1 to the quantity of melons of type <id> (which will be 0 if we
    # haven't yet put any of that kind of melon into the cart)
    cart[id1] = cart.setdefault(id1, 0) + 1
    print cart

    # add a confirmation message to the "flash" messages buffer
    melon_type = melons.get_by_id(int(id1)).common_name.lower()
    print melon_type
    flash_message = "Successfully added a {type} melon to your cart."
    flash(flash_message.format(type=melon_type))

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
