import os
from flask import Flask
from extensions import db, login_manager, bcrypt
from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super-secret-luxury-hotel-key'
    
    # Absolute path for SQLite DB to ensure it creates in the current folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hotel.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    # Initialize DB and create admin if not exists
    with app.app_context():
        db.create_all()
        from models import User
        if not User.query.filter_by(role='admin').first():
            print("Creating default admin user...")
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin_user = User(username='admin', email='admin@hotel.com', password=hashed_pw, role='admin')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin created: admin@hotel.com / admin123")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
