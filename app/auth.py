from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Candidate
from app import db, user_registration_counter, user_login_counter


def extract_voter_id(email):
    return email.split('@')[0]


def is_valid_email(email):
    return email.endswith('@kristujayanti.com')


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('auth.register'))

        if not is_valid_email(email):
            flash('Email must end with @kristujayanti.com', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))

        voter_id = extract_voter_id(email)
        if User.query.filter((User.email == email) | (User.voter_id == voter_id)).first():
            flash('User already registered', 'danger')
            return redirect(url_for('auth.register'))

        user = User(voter_id=voter_id, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        user_registration_counter.inc()
        flash(f'Registration successful. Voter ID: {voter_id}', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        voter_id = request.form.get('voter_id')
        password = request.form.get('password')

        user = User.query.filter_by(voter_id=voter_id).first()
        if user and user.check_password(password):
            login_user(user)
            user_login_counter.inc()
            return redirect(url_for('auth.vote'))

        flash('Invalid voter ID or password', 'danger')

    return render_template('login.html')


@auth_bp.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
    if current_user.has_voted:
        flash('You have already voted', 'warning')
        return redirect(url_for('auth.results'))

    candidates = Candidate.query.all()
    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        candidate = Candidate.query.get(candidate_id)

        if not candidate:
            flash('Candidate selection is invalid', 'danger')
            return redirect(url_for('auth.vote'))

        candidate.vote_count += 1
        current_user.has_voted = True
        db.session.commit()

        from app import vote_counter
        vote_counter.inc()

        flash('Vote recorded successfully', 'success')
        return redirect(url_for('auth.results'))

    return render_template('vote.html', candidates=candidates)


@auth_bp.route('/results')
@login_required
def results():
    candidates = Candidate.query.all()
    total_votes = sum(c.vote_count for c in candidates)
    return render_template('results.html', candidates=candidates, total_votes=total_votes)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('auth.login'))