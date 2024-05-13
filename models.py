from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from uuid import uuid4

# SQLAlchemy instance for PostgreSQL database
db = SQLAlchemy()


def get_uuid():
    return uuid4().hex

# Model for User Authentication using SQLite database
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_driver = db.Column(db.Boolean, default=False)
    is_passenger = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, is_admin=False, is_driver=False, is_passenger=False):
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_driver = is_driver
        self.is_passenger = is_passenger

# Model for bus registration and management using PostgreSQL database
class Bus(db.Model):
    __tablename__ = "buses"
    id = db.Column(db.Integer, primary_key=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(255), nullable=False)
    time_of_travel = db.Column(db.DateTime, nullable=False)
    driver_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    driver = relationship("User", back_populates="buses")

    def __init__(self, number_of_seats, cost_per_seat, route, time_of_travel, driver_id):
        self.number_of_seats = number_of_seats
        self.cost_per_seat = cost_per_seat
        self.route = route
        self.time_of_travel = time_of_travel
        self.driver_id = driver_id

User.buses = relationship("Bus", back_populates="driver")

# Model for seat booking and management using PostgreSQL database
class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    passenger = relationship("User", back_populates="bookings")
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    bus = relationship("Bus", back_populates="bookings")
    seat_number = db.Column(db.Integer, nullable=False)

    def __init__(self, passenger_id, bus_id, seat_number):
        self.passenger_id = passenger_id
        self.bus_id = bus_id
        self.seat_number = seat_number

User.bookings = relationship("Booking", back_populates="passenger")
Bus.bookings = relationship("Booking", back_populates="bus")

# Model for price management using PostgreSQL database
class Price(db.Model):
    __tablename__ = "prices"
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)
    bus = relationship("Bus", back_populates="prices")
    route = db.Column(db.String(255), nullable=False)
    price_per_seat = db.Column(db.Float, nullable=False)

    def __init__(self, bus_id, route, price_per_seat):
        self.bus_id = bus_id
        self.route = route
        self.price_per_seat = price_per_seat

Bus.prices = relationship("Price", back_populates="bus")
