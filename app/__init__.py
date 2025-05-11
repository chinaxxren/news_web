#!/usr/bin/env python
import os
from flask import Flask, Markup
from datetime import datetime, timedelta
import markdown
import logging
from dotenv import load_dotenv
from app.extensions import db, login, babel
from app.database import get_or_create
from flask_wtf.csrf import CSRFProtect
from .filters import register_filters

# 基础配置
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, ".env"))

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(basedir, "app.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# 应用配置
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20
    UPLOAD_FOLDER = os.path.join(basedir, "app/static/uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    LANGUAGES = ["en", "zh"]
    BABEL_DEFAULT_LOCALE = "en"
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "admin"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY") or "dev-csrf-key"


def short_time_ago(dt):
    now = datetime.utcnow()
    if dt.tzinfo is not None:
        now = now.replace(tzinfo=dt.tzinfo)
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m"
    elif seconds < 86400:
        return f"{int(seconds // 3600)}h"
    elif seconds < 604800:
        return f"{int(seconds // 86400)}d"
    else:
        return dt.strftime("%Y-%m-%d")


def create_app(config_class=Config):
    """创建并配置Flask应用"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    login.init_app(app)
    babel.init_app(app)
    csrf = CSRFProtect(app)

    # 注册蓝图
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.admin import bp as admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")

    # 注册命令
    from app.commands import init_data

    app.cli.add_command(init_data)

    # 注册模板过滤器
    def markdown_filter(text):
        return Markup(markdown.markdown(text, extensions=["fenced_code", "codehilite"]))

    app.jinja_env.filters["markdown"] = markdown_filter

    def friendly_time(dt):
        now = datetime.utcnow()
        diff = now - dt
        if diff < timedelta(minutes=1):
            return "just now"
        elif diff < timedelta(hours=1):
            mins = int(diff.total_seconds() // 60)
            return f"{mins}m ago"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() // 3600)
            return f"{hours}h ago"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days}d ago"
        else:
            return dt.strftime("%Y-%m-%d")

    app.jinja_env.filters["friendly_time"] = friendly_time

    register_filters(app)

    # 初始化应用
    with app.app_context():
        # 创建数据库表
        db.create_all()

        # 创建管理员用户
        from app.models import User

        admin, created = get_or_create(
            User,
            username=Config.ADMIN_USERNAME,
            defaults={"email": Config.ADMIN_EMAIL, "is_admin": True},
        )
        if created:
            admin.set_password(Config.ADMIN_PASSWORD)
            logger.info("管理员用户已创建")

        # 确保上传目录存在
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    return app


def register_filters(app):
    app.jinja_env.filters["short_time_ago"] = short_time_ago
