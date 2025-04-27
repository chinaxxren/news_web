import click
from flask import current_app
from app import db
from app.models import User, Tag
from datetime import datetime


@click.command("init-data")
def init_data():
    """初始化基础数据"""
    click.echo("开始初始化数据...")

    # 创建管理员用户
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@example.com",
            is_admin=True,
            created_at=datetime.utcnow(),
        )
        admin.set_password("admin123")
        db.session.add(admin)
        click.echo("创建管理员用户")

    # 创建默认标签
    default_tags = ["新闻", "科技", "体育", "娱乐", "财经"]
    for tag_name in default_tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name, created_at=datetime.utcnow())
            db.session.add(tag)
            click.echo(f"创建标签: {tag_name}")

    db.session.commit()
    click.echo("数据初始化完成！")
