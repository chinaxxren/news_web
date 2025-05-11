from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel

# 初始化扩展
db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "请先登录"
babel = Babel()
