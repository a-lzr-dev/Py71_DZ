from datetime import datetime

from flask import Blueprint, render_template

blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=["GET"])
def index():
    return render_template("index.html", dt=datetime.now())


@blueprint.route('/about', methods=["GET"])
def about_view():
    return render_template("about.html")
