from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from prometheus_client import Counter

db = SQLAlchemy()
login_manager = LoginManager()

# Prometheus counters
vote_counter = Counter('total_votes', 'Total votes cast')
user_registration_counter = Counter('user_registrations', 'Total user registrations')
user_login_counter = Counter('user_logins', 'Total user logins')
admin_login_counter = Counter('admin_logins', 'Total admin logins')


import os
from pathlib import Path


def create_app():
    base_dir = Path(__file__).resolve().parent.parent
    template_dir = base_dir / 'templates'
    static_dir = base_dir / 'static'
    instance_dir = base_dir / 'instance'

    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir),
        instance_path=str(instance_dir)
    )

    app.config['SECRET_KEY'] = 'your-secret-key-change-me'

    # Ensure instance folder exists for sqlite db
    instance_dir.mkdir(parents=True, exist_ok=True)
    db_file = instance_dir / 'voting_system.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file.as_posix()}"

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import Admin, User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)

        # Seed a default candidate for initial voting test coverage
        from app.models import Candidate
        if not Candidate.query.first():
            default_candidate = Candidate(name='Default Candidate', department='General', position='President')
            db.session.add(default_candidate)

        db.session.commit()

    return app