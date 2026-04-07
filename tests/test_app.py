import pytest
import os
import tempfile
from app import create_app, db
from app.models import User, Admin, Candidate


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.engine.dispose()
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class TestUserModel:
    def test_password_hashing(self, app):
        with app.app_context():
            user = User(voter_id='test123', email='test@kristujayanti.com')
            user.set_password('password123')
            assert user.check_password('password123')
            assert not user.check_password('wrongpassword')

    def test_user_creation(self, app):
        with app.app_context():
            user = User(voter_id='test123', email='test@kristujayanti.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(voter_id='test123').first()
            assert retrieved_user is not None
            assert retrieved_user.email == 'test@kristujayanti.com'
            assert retrieved_user.has_voted == False


class TestAdminModel:
    def test_admin_password_hashing(self, app):
        with app.app_context():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            assert admin.check_password('admin123')
            assert not admin.check_password('wrongpassword')

    def test_admin_creation(self, app):
        with app.app_context():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

            retrieved_admin = Admin.query.filter_by(username='admin').first()
            assert retrieved_admin is not None
            assert retrieved_admin.check_password('admin123')


class TestCandidateModel:
    def test_candidate_creation(self, app):
        with app.app_context():
            candidate = Candidate(
                name='John Doe',
                department='Computer Science',
                position='President',
                vote_count=0
            )
            db.session.add(candidate)
            db.session.commit()

            retrieved_candidate = Candidate.query.filter_by(name='John Doe').first()
            assert retrieved_candidate is not None
            assert retrieved_candidate.department == 'Computer Science'
            assert retrieved_candidate.vote_count == 0

    def test_vote_increment(self, app):
        with app.app_context():
            candidate = Candidate(
                name='Jane Smith',
                department='Engineering',
                position='Vice President'
            )
            db.session.add(candidate)
            db.session.commit()

            candidate.vote_count += 1
            db.session.commit()

            retrieved_candidate = Candidate.query.filter_by(name='Jane Smith').first()
            assert retrieved_candidate.vote_count == 1


class TestRoutes:
    def test_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.headers['Location']

    def test_register_page(self, client):
        response = client.get('/register')
        assert response.status_code == 200
        assert b'register' in response.data.lower()

    def test_admin_login_page(self, client):
        response = client.get('/admin/login')
        assert response.status_code == 200
        assert b'admin' in response.data.lower()

    def test_invalid_route(self, client):
        response = client.get('/nonexistent')
        assert response.status_code == 404