"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for, jsonify, send_from_directory, request, get_flashed_messages, flash, Response
from flask_login import current_user, login_required
from .forms import LoginForm, SignupForm, SearchForm
from .models import db, User
from . import login_manager
from .servarr_connectors import  *
from .servarr_connectors.transmission_connect import *
from pprint import pprint

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    form = SearchForm()
    # pprint(results.json())
    return render_template(
        'index.jinja2',
        form=form,
        title='Download',
        template='dashboard',
        alert=get_flashed_messages()
        )

@main_bp.route('/', methods=['GET', 'POST'])
def content(data):
    print('CONTENT')
    render_template('content.jinja2', data)

@main_bp.route('/api/v1/tv/<name>', methods=['GET'])
@main_bp.route('/api/v1/tv/', methods=['POST'])
@login_required
def tv_search(name=None):
    if request.method == 'POST':
        data = request.json
        results = add_show(data)
        if results.status_code >= 200 and results.status_code <= 299:
            return Response("{'text':'Series added successfully'}", status=results.status_code, mimetype='application/json')
        else:
            return Response("{'text':'Failed to add series'}", status=results.status_code, mimetype='application/json')
    else:
        results = search_sonarr(name)
        if results.status_code == 200:
            return jsonify(results.json())
        else:
            return None
    
@main_bp.route('/api/v1/movie/<name>', methods=['GET'])
@main_bp.route('/api/v1/movie', methods=['POST'])
@login_required
def movie_search(name=None):
    if request.method == 'POST':
        data = request.json
        results = add_movie(data)
        if results.status_code >= 200 and results.status_code <= 299:
            return Response("{'text':'Movie added successfully'}", status=results.status_code, mimetype='application/json')
        else:
            return Response("{'text':'Failed to add Movie'}", status=results.status_code, mimetype='application/json')
    else:
        results = search_radarr(name)
        if results.status_code == 200:
            return jsonify(results.json())
        else:
            return None
        
@main_bp.route('/api/v1/downloads/', methods=['GET'])
@login_required
def download_search():
    downloads = get_active_downloads()
    for download in downloads:
        if download['is_stalled'] == True:
            recover_stalled_sonarr(download['name'])
            recover_stalled_radarr(download['name'])
    return jsonify(downloads)

@main_bp.route('/static/<file>')
def not_found(file):
    return send_from_directory('static', file)