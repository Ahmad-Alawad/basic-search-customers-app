from flask_sqlalchemy import SQLAlchemy
# from server import app




db = SQLAlchemy()



class Customer(db.Model):
    """Customers table"""

    __tablename__ = "customer"

    id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///customersappdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    db.session.commit()

