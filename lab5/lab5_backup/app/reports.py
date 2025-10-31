from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from io import BytesIO
from app.models import User
from .auth import check_rights
from app.repositories.report_repository import ReportRepository
from app.policies.user_policy import UserPolicy

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/')
@login_required
@check_rights('users', 'view_journal')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    policy = UserPolicy(user_id=current_user.id)
    
    visits = ReportRepository.get_paginated_visits(
        page=page,
        per_page=per_page,
        filters=request.args.to_dict(),
        order_by=request.args.get('order_by', 'created_at'),
        policy=policy
    )
    
    return render_template('reports/index.html', visits=visits)

@bp.route('/by-pages')
@login_required
@check_rights('users', 'view_journal_analytics')
def by_pages():
    stats = ReportRepository.get_page_stats()
    return render_template('reports/by_pages.html', stats=stats)

@bp.route('/by-pages/export')
@login_required
@check_rights('users', 'view_journal_analytics')
def export_by_pages():
    stats = ReportRepository.get_page_stats()

    csv_output = "№;Страница;Количество посещений\n"
    for i, row in enumerate(stats, 1):
        csv_output += f"{i};{row.path};{row.count}\n"

    output = BytesIO()
    output.write(b'\xEF\xBB\xBF')
    output.write(csv_output.encode('utf-8'))
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv; charset=utf-8',
        as_attachment=True,
        download_name='отчет_по_страницам.csv'
    )

@bp.route('/by-users')
@login_required
@check_rights('users', 'view_journal_analytics')
def by_users():
    user_stats = ReportRepository.get_user_stats()
    return render_template('reports/by_users.html', stats=user_stats)

@bp.route('/by-users/export')
@login_required
@check_rights('users', 'view_journal_analytics')
def export_by_users():
    user_stats = ReportRepository.get_user_stats()
    anon_count = ReportRepository.get_anonymous_visits_count()

    csv_output = "№;Пользователь;Количество посещений\n"
    
    for i, row in enumerate(user_stats, 1):
        name = f"{row.last_name} {row.first_name} {row.middle_name or ''}".strip()
        csv_output += f"{i};{name};{row.count}\n"
    
    if anon_count > 0:
        csv_output += f"{len(user_stats)+1};Неаутентифицированный пользователь;{anon_count}\n"

    output = BytesIO()
    output.write(b'\xEF\xBB\xBF')
    output.write(csv_output.encode('utf-8'))
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv; charset=utf-8',
        as_attachment=True,
        download_name='отчет_по_пользователям.csv'
    )