from flask import Flask, g

from src.blueprints.main import blueprint as main_blueprint
from src.blueprints.posts import blueprint as posts_blueprint
from src.blueprints.auth import bp as auth_blueprint
from src.config import Config
from src.db import db
from src.services.auth import get_current_user_from_session

app = Flask(__name__, template_folder="templates")
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(main_blueprint)
app.register_blueprint(posts_blueprint)
app.register_blueprint(auth_blueprint)


@app.before_request
def before_request():
    g.current_user = get_current_user_from_session()


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
