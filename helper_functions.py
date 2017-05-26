from model import Customer, connect_to_db
from server import app

connect_to_db(app)


def some_fun():
    print "hi"


    
def get_all_customers():
    """Access DB and get a list of all customers objects"""

    all_customers = Customer.query.all()
    return all_customers