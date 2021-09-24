from flask import Blueprint, jsonify

bp = Blueprint('home', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'result': 'congratulations!'})
