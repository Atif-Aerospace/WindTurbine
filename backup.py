from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/aircadia')
def aaa():
    return "Hello, AirCADia!"



@app.route('/aaa/<name>/<location>')
def createUser(name, location):
    user = User(name = name, location = location)
    db.session.add(user)
    db.session.commit()
    return '<h1>Added New User</h1>'


@app.route('/bbb/<name>')
def GetUser(name):
    user = User.query.filter_by(name = name).first()
    return f'<h1>The user is located in: {user.location}</h1>'

@app.route('/ccc/<name>')
def delete_user(name):
    user = User.query.filter_by(name = name).first()
    db.session.delete(user)
    db.session.commit()
    return f'<h1>The user is located in: {user.location}</h1>'

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(50))
#     location = db.Column(db.String(50))
#     #date_created = db.Column(db.DateTime, dafault = datetime.now)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    #location = db.Column(db.String(50))
    #date_created = db.Column(db.DateTime, dafault = datetime.now)
    #inputs = db.relationship('Data', backref='owner')
    products = db.relationship("Product", secondary="orders")

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    #type = db.Column(db.String(50))
    #date_created = db.Column(db.DateTime, dafault = datetime.now)
    users = db.relationship("User", secondary="orders")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    data_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    model = db.relationship(User, backref=db.backref("orders", cascade="all, delete-orphan"))
    data = db.relationship(Product, backref=db.backref("orders", cascade="all, delete-orphan"))

if __name__ == '__main__':
    app.run(debug=True, port=5000)