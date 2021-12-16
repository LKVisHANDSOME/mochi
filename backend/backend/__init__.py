from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login.utils import login_required
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from backend.config import Config
from flask_login import LoginManager


app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = '該網頁需要登入才能瀏覽'



@app.route('/')
def home():
    return "hello world"


from backend.models import User
import base64
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
def load_user_from_header(header_val):
    header_val = header_val.replace('Basic', '', 1)
    try:
        header_val = base64.b64decode(header_val)
    except TypeError:
        pass
    return User.query.filter_by(user_id = header_val).first()


from backend.routes import problem
api.add_resource(problem, "/problem")

from backend.routes import problem_id
api.add_resource(problem_id, "/problem/<int:problem_id>")

from backend.routes import problem_solution
api.add_resource(problem_solution,"/problem/<int:problem_id>/solution")

from backend.routes import problem_submission
api.add_resource(problem_submission, "/problem/<int:problem_id>/submission/<int:user_id>")

from backend.routes import status
api.add_resource(status, "/status/<int:page>")

from backend.routes import login
api.add_resource(login, "/login")

from backend.routes import logout
api.add_resource(logout, "/logout")

from backend.routes import signup
api.add_resource(signup, "/signup")

from backend.routes import user_profile
api.add_resource(user_profile, "/user/<int:user_id>/profile")

from backend.routes import submission_data
api.add_resource(submission_data, "/submission/<int:submission_id>")

from backend.routes import queue_new
api.add_resource(queue_new, "/submission/new")

from backend.routes import dispatcher
api.add_resource(dispatcher,"/dispatcher")


# from backend.routes import problem, problem_post_args
# api.add_resource(problem, "/problem/<int:problem_id>")