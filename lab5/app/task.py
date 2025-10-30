from flask import Blueprint, render_template

bp = Blueprint('task', __name__)

@bp.route('/task')
def task():
    return render_template('task.html')