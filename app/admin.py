from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Candidate, Admin, User
from app import db, admin_login_counter

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            admin_login_counter.inc()
            return redirect(url_for('admin.dashboard'))

        flash('Invalid username or password', 'danger')
    return render_template('admin_login.html')


@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    candidates = Candidate.query.all()
    total_votes = sum(c.vote_count for c in candidates)
    return render_template('admin_dashboard.html', candidates=candidates, total_votes=total_votes, users=User.query.count(), voted_users=User.query.filter_by(has_voted=True).count())


@admin_bp.route('/add_candidate', methods=['POST'])
def add_candidate():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    name = request.form.get('name')
    department = request.form.get('department')
    position = request.form.get('position')

    if not all([name, department, position]):
        flash('All fields required', 'danger')
        return redirect(url_for('admin.dashboard'))

    candidate = Candidate(name=name, department=department, position=position)
    db.session.add(candidate)
    db.session.commit()
    flash('Candidate added', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/update_candidate/<int:candidate_id>', methods=['POST'])
def update_candidate(candidate_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        flash('Candidate not found', 'danger')
        return redirect(url_for('admin.dashboard'))

    candidate.name = request.form.get('name', candidate.name)
    candidate.department = request.form.get('department', candidate.department)
    candidate.position = request.form.get('position', candidate.position)
    db.session.commit()

    flash('Candidate updated', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delete_candidate/<int:candidate_id>', methods=['POST'])
def delete_candidate(candidate_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    candidate = Candidate.query.get(candidate_id)
    if candidate:
        db.session.delete(candidate)
        db.session.commit()
        flash('Candidate deleted', 'success')
    else:
        flash('Candidate not found', 'danger')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/results')
def admin_results():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.admin_login'))

    candidates = Candidate.query.all()
    total_votes = sum(c.vote_count for c in candidates)
    return render_template('results.html', candidates=candidates, total_votes=total_votes, admin=True)


@admin_bp.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Admin logged out', 'success')
    return redirect(url_for('admin.admin_login'))