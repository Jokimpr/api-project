from flask import Blueprint, redirect, url_for, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@main_bp.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
