from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user') # 'user' or 'admin'
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
    rooms = db.relationship('Room', backref='hotel', lazy=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    room_type = db.Column(db.String(100), nullable=False) # Standard, Deluxe, Suite
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=True)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False) # Breakfast, Lunch, Dinner
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

class TaxiService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    pricing_per_km = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type = db.Column(db.String(50), nullable=False) # 'hotel', 'room', 'food', 'taxi'
    service_id = db.Column(db.Integer, nullable=False) # ID of the booked item
    details = db.Column(db.Text, nullable=True) # string detailing booking info
    total_price = db.Column(db.Float, nullable=False)
    date_booked = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Confirmed')
