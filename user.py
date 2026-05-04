from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models import Hotel, Room, FoodItem, TaxiService, Booking
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Ensure user role
@user_bp.before_request
@login_required
def check_user():
    if current_user.role != 'user':
        flash("Access Denied", "danger")
        return redirect(url_for('admin.dashboard'))

@user_bp.route('/dashboard')
def dashboard():
    return render_template('user/dashboard.html')

@user_bp.route('/hotels', methods=['GET', 'POST'])
def hotels():
    hotels = Hotel.query.all()
    if request.method == 'POST':
        hotel_id = request.form.get('hotel_id')
        hotel = Hotel.query.get(hotel_id)
        if hotel:
            booking = Booking(
                user_id=current_user.id,
                service_type='hotel',
                service_id=hotel.id,
                details=f"Booked hotel {hotel.name}",
                total_price=hotel.price
            )
            db.session.add(booking)
            db.session.commit()
            flash(f'Successfully booked {hotel.name}!', 'success')
            return redirect(url_for('user.history'))
    return render_template('user/hotels.html', hotels=hotels)

@user_bp.route('/rooms', methods=['GET', 'POST'])
def rooms():
    rooms = Room.query.filter_by(availability=True).all()
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        room = Room.query.get(room_id)
        if room:
            room.availability = False
            booking = Booking(
                user_id=current_user.id,
                service_type='room',
                service_id=room.id,
                details=f"Booked room type: {room.room_type}",
                total_price=room.price
            )
            db.session.add(booking)
            db.session.commit()
            flash(f'Successfully booked room!', 'success')
            return redirect(url_for('user.history'))
    return render_template('user/rooms.html', rooms=rooms)

@user_bp.route('/food', methods=['GET', 'POST'])
def food():
    foods = FoodItem.query.all()
    if request.method == 'POST':
        food_id = request.form.get('food_id')
        food = FoodItem.query.get(food_id)
        if food:
            booking = Booking(
                user_id=current_user.id,
                service_type='food',
                service_id=food.id,
                details=f"Ordered food: {food.name}",
                total_price=food.price
            )
            db.session.add(booking)
            db.session.commit()
            flash(f'Successfully ordered {food.name}!', 'success')
            return redirect(url_for('user.history'))
    return render_template('user/food.html', foods=foods)

@user_bp.route('/taxi', methods=['GET', 'POST'])
def taxi():
    taxis = TaxiService.query.all()
    if request.method == 'POST':
        taxi_id = request.form.get('taxi_id')
        distance = request.form.get('distance', type=float)
        taxi = TaxiService.query.get(taxi_id)
        if taxi and distance:
            total = taxi.pricing_per_km * distance
            booking = Booking(
                user_id=current_user.id,
                service_type='taxi',
                service_id=taxi.id,
                details=f"Booked taxi {taxi.vehicle_type} for {distance}km",
                total_price=total
            )
            db.session.add(booking)
            db.session.commit()
            flash(f'Taxi booked! Estimated fare: ${total:.2f}', 'success')
            return redirect(url_for('user.history'))
            
    return render_template('user/taxi.html', taxis=taxis)

@user_bp.route('/history')
def history():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.date_booked.desc()).all()
    return render_template('user/history.html', bookings=bookings)
