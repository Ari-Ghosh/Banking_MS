from bank import db
from datetime import datetime
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy import text, event
import hashlib
from bank import app
from uuid import uuid4

class Customer(db.Model):
    """
        Represents the 'customers' table in the database.
        Contains customer information such as ID, SSN, name, age, address, state, city, and timestamps for creation and update.
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    address = db.Column(db.String(255))
    state = db.Column(db.Integer)
    city = db.Column(db.Integer)
    created_at = db.Column(TIMESTAMP(), nullable=False)
    updated_at = db.Column(TIMESTAMP(), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, ssn_id, name, age, address, state, city, created_at):
        self.ssn_id = ssn_id
        self.name = name
        self.age = age
        self.address = address
        self.state = state
        self.city = city
        self.created_at = created_at


class Country(db.Model):
    """
        Represents the 'countries' table.
        Stores information about countries, including ID, sortname, name, and phone code.
    """
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    sortname = db.Column(db.String(3))
    name = db.Column(db.String(150))
    phonecode = db.Column(db.Integer)

class State(db.Model):
    """
        Represents the 'states' table.
        Contains information about states or provinces within a country, with columns for ID, name, and a foreign key reference to the 'countries' table.
    """
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))


class City(db.Model):
    """
        Represents the 'cities' table.
        Stores data about cities, including ID, name, and a foreign key reference to the 'states' table.
    """
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))

class CustomerStatus(db.Model):
    """ 
        Represents the 'customer_status' table.
        Records the status of customers with columns for ID, customer ID, SSN ID, a status flag, a message, and a timestamp for updates.
    """
    __tablename__ = 'customer_status'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    ssn_id = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=True)
    message = db.Column(db.String(255))
    updated_at = db.Column(TIMESTAMP(), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, customer_id, ssn_id, message):
        self.customer_id = customer_id
        self.ssn_id = ssn_id
        self.message = message

class Account(db.Model):
    """
        Represents the 'accounts' table.
        Stores information about customer accounts, including ID, customer ID, account type, amount, lock status, and timestamps for creation and updates.
    """
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    account_type = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(TIMESTAMP(), nullable=False)
    updated_at = db.Column(TIMESTAMP(), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, customer_id, account_type, amount, created_at):
        self.customer_id = customer_id
        self.account_type = account_type
        self.amount = amount
        self.created_at = created_at

class AccountStatus(db.Model):
    """
        Represents the 'account_status' table.
        Records the status of accounts with columns for ID, account ID, customer ID, account type, a status flag, a message, and a timestamp for updates.
    """
    __tablename__ = 'account_status'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    account_type = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=True)
    message = db.Column(db.String(255))
    updated_at = db.Column(TIMESTAMP(), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, account_id, customer_id, account_type, message):
        self.customer_id = customer_id
        self.account_id = account_id
        self.account_type = account_type
        self.message = message

class TransactionControl(db.Model):
    """
        Represents the 'transactions_control' table.
        Manages transaction control with columns for ID, a transaction ID (generated using a timestamp and UUID), account ID, description, amount, and a timestamp for creation.
    """

    __tablename__ = 'transactions_control'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100))
    account_id = db.Column(db.Integer)
    description = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    created_at = db.Column(TIMESTAMP(), nullable=False)

    def __init__(self, account_id, description, amount, created_at):
        self.account_id = account_id
        self.transaction_id = self.get_transaction_id()
        self.description = description
        self.amount = amount
        self.created_at = created_at

    def get_transaction_id(self):
        transaction_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        return transaction_id

class UserRegistration(db.Model):
    """
        Represents the 'user_registrations' table.
        Stores user registration information, including ID, username, hashed password, a status flag, and timestamps for creation and updates.
        It also contains a method for hashing passwords.
    """

    __tablename__ = 'user_registrations'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(TIMESTAMP(), nullable=False)
    updated_at = db.Column(TIMESTAMP(), nullable=False,
                        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self, username, password, created_at):
        self.username = username
        self.password = password
        self.created_at = created_at

    def __str__(self):
        return self.username

    @staticmethod
    def hashing(password):
        salt = app.config.get('SALT', '')
        db_password = password + salt
        hash = hashlib.md5(db_password.encode())
        hashing_password = hash.hexdigest()
        return hashing_password

# Event listeners
def set_auto_increment(target, connection, **kw):
    table_name = target.fullname
    connection.execute(text(f"ALTER TABLE {table_name} AUTO_INCREMENT = 300000000;"))

event.listen(Customer.__table__, "after_create", set_auto_increment)
event.listen(Account.__table__, "after_create", set_auto_increment)