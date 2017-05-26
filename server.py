from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Customer
# from helper_functions import get_all_customers



def get_all_customers():
    """Access DB and get a list of all customers objects"""

    all_customers = Customer.query.all()
    return all_customers



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""


    customers_list = get_all_customers()
    return render_template("homepage.html", customers=customers_list)

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


@app.route('/all_customers.json')
def get_all_customers_view():
    """Return all customers in json object"""

    all_customers = get_all_customers()
    customers_list = []
    for customer in all_customers:
        customer_dict = {'fname':customer.fname , 'lname':customer.lname}
        customers_list.append(customer_dict)
    return jsonify(customers_list)

if __name__ == "__main__":
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug  

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5001, host='0.0.0.0')