from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float
import os
from flask_marshmallow import Marshmallow  # Marshmallow is to turn a row from a table into JSON code


# define the flask app
kubrickapi = Flask(__name__)
# config settings for SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
# telling flask (sqlalchemy) where the database file will be stored/accessible to/from
kubrickapi.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'kubes.db')


# configure marshmallow
ma = Marshmallow(kubrickapi)


# initialise our database as a python object
db = SQLAlchemy(kubrickapi)


@kubrickapi.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Successfully Created!')


@kubrickapi.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database has been dropped successfully')


# home page route (endpoint)
@kubrickapi.route('/')  # Decorating an existing function to serve our purpose
def home():
    return jsonify(data='You be at the homepage')


# RESTful API's - well documented in how to use it
# setting a new endpoint /people
# users/consumers of my API must provide a key=value pair
# in the format of:
# p=lastname ie. p=connolly
# cohort = enum('DP', 'DE', 'DM')
@kubrickapi.route('/people', methods=['POST'])
def people():
    name = request.form['p']
    # retrieve records from a database
    peopledata = People.query.filter_by(lname=name).first()
    result = people_schema.dump(peopledata)
    return jsonify(result)
# {} data input is respective eg. /people?p=cconnolly&cohort=DP


@kubrickapi.route('/addpeople', methods=['POST', 'GET'])
def addpeople():
    fn = request.form['firstname']
    ln = request.form['lastname']
    em = request.form['emailaddress']
    # insert the data into the sqlite database
    new_people = People(fname=fn, lname=ln, email=em)  # populating an object, an instance of the class
    db.session.add(new_people)
    db.session.commit()
    # result = successfailure flag
    # if insert successful then return result
    # else return result
    return jsonify(data='People {} added to the database'.format(em))


@kubrickapi.route('/rempeople', methods=['POST', 'GET'])
def rempeople():
    # name = request.args.get('p')
    name = request.form['lastname']
    remperson = People.query.filter_by(lname=name).first()
    if remperson:
        db.session.delete(remperson)
        db.session.commit()
        return jsonify(data='Person with last name {} removed from the database'.format(name))
    else:
        return jsonify(data='Person with last name {} did no exist in the database'.format(name))


# in SQLAlchemy a Model is a table -- we are creating the blueprint for our own table called People
class People(db.Model):  # A model is a table
    __tablename__='people'  # make a table called people
    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    email = Column(String, unique=True)


class PeopleSchema(ma.Schema):
    class Meta:
        fields=('id', 'fname', 'lname', 'email')


people_schema = PeopleSchema()


if __name__ == '__main__':
    kubrickapi.run()
