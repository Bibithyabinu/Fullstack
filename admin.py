from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from models import Hotel, Room, FoodItem, TaxiService, Booking, User
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Ensure admin role
@admin_bp.before_request
@login_required
def check_admin():
    if current_user.role != 'admin':
        flash("Access Denied", "danger")
        return redirect(url_for('user.dashboard'))

@admin_bp.route('/dashboard')
def dashboard():
    users_count = User.query.filter_by(role='user').count()
    bookings_count = Booking.query.count()
    hotels_count = Hotel.query.count()
    revenue = db.session.query(db.func.sum(Booking.total_price)).scalar() or 0.0
    
    return render_template('admin/dashboard.html', 
                          users_count=users_count, 
                          bookings_count=bookings_count, 
                          hotels_count=hotels_count,
                          revenue=revenue)

@admin_bp.route('/hotels', methods=['GET', 'POST'])
def manage_hotels():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        location = request.form.get('location')
        price = request.form.get('price', type=float)
        image_url = request.form.get('image_url')
        
        hotel = Hotel(name=name, description=description, location=location, price=price, image_url=image_url)
        db.session.add(hotel)
        db.session.commit()
        flash('Hotel added successfully', 'success')
        return redirect(url_for('admin.manage_hotels'))
        
    hotels = Hotel.query.all()
    return render_template('admin/manage_hotels.html', hotels=hotels)

@admin_bp.route('/hotels/delete/<int:id>')
def delete_hotel(id):
    hotel = Hotel.query.get_or_404(id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted', 'success')
    return redirect(url_for('admin.manage_hotels'))

@admin_bp.route('/rooms', methods=['GET', 'POST'])
def manage_rooms():
    if request.method == 'POST':
        hotel_id = request.form.get('hotel_id', type=int)
        room_type = request.form.get('room_type')
        price = request.form.get('price', type=float)
        capacity = request.form.get('capacity', type=int)
        
        room = Room(hotel_id=hotel_id, room_type=room_type, price=price, capacity=capacity)
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully', 'success')
        return redirect(url_for('admin.manage_rooms'))
        
    rooms = Room.query.all()
    hotels = Hotel.query.all()
    return render_template('admin/manage_rooms.html', rooms=rooms, hotels=hotels)

@admin_bp.route('/rooms/delete/<int:id>')
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('Room deleted', 'success')
    return redirect(url_for('admin.manage_rooms'))

@admin_bp.route('/food', methods=['GET', 'POST'])
def manage_food():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        price = request.form.get('price', type=float)
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        
        food = FoodItem(name=name, category=category, price=price, description=description, image_url=image_url)
        db.session.add(food)
        db.session.commit()
        flash('Food item added successfully', 'success')
        return redirect(url_for('admin.manage_food'))
        
    foods = FoodItem.query.all()
    return render_template('admin/manage_food.html', foods=foods)

@admin_bp.route('/food/delete/<int:id>')
def delete_food(id):
    food = FoodItem.query.get_or_404(id)
    db.session.delete(food)
    db.session.commit()
    flash('Food deleted', 'success')
    return redirect(url_for('admin.manage_food'))

@admin_bp.route('/taxi', methods=['GET', 'POST'])
def manage_taxi():
    if request.method == 'POST':
        vehicle_type = request.form.get('vehicle_type')
        description = request.form.get('description')
        pricing_per_km = request.form.get('pricing_per_km', type=float)
        
        taxi = TaxiService(vehicle_type=vehicle_type, description=description, pricing_per_km=pricing_per_km)
        db.session.add(taxi)
        db.session.commit()
        flash('Taxi service added successfully', 'success')
        return redirect(url_for('admin.manage_taxi'))
        
    taxis = TaxiService.query.all()
    return render_template('admin/manage_taxi.html', taxis=taxis)

@admin_bp.route('/taxi/delete/<int:id>')
def delete_taxi(id):
    taxi = TaxiService.query.get_or_404(id)
    db.session.delete(taxi)
    db.session.commit()
    flash('Taxi deleted', 'success')
    return redirect(url_for('admin.manage_taxi'))

@admin_bp.route('/bookings')
def view_bookings():
    bookings = Booking.query.order_by(Booking.date_booked.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings)
