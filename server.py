from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Customer


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/search')
def search():
    """Search."""
    # import pdb; pdb.set_trace()
    # 1. get form inputs (fname, lname)
    fname = request.args.get('fname')
    lname = request.args.get('lname')

    # 2. Search DB using SQLAlchemy for fname and lname (Table name is customerts)
    try:
        customer = db.session.query(Customer).filter(Customer.fname==fname).filter(Customer.lname==lname).one()
    except:
        flash("Customer not found!!!")
        return redirect('/')

    # 3. Display search results
    return render_template("search_results.html", customer=customer)


@app.route('/add-customer')
def add_customer():
    """Display Add Customer Form"""
    
    return render_template("add_customer.html")

@app.route('/process_adding_customer')
def add_customer_to_db():
    """Add customer to DB."""
    f_name = request.args.get('fname')
    l_name = request.args.get('lname')
    zip_code = request.args.get('zipcode')

    # To add this customer to db:
    # 1. Create the customer
    customer = Customer(fname=f_name, lname=l_name, zipcode=zip_code)

    # 2. Add this customer to session
    db.session.add(customer)

    # 3. Commit the changes
    db.session.commit()

    # 4. Display a flash message to confirm adding
    flash("Customer was addded successfully!!!")

    return redirect("/")

if __name__ == "__main__":
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug  

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5001, host='0.0.0.0')