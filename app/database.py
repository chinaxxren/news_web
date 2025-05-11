from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Optional, Tuple, Any
from app.extensions import db

# 配置日志
logger = logging.getLogger(__name__)


@contextmanager
def session_scope():
    """提供一个事务范围的会话上下文管理器"""
    try:
        yield db.session
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.session.close()


def init_db(app):
    """初始化数据库"""
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database tables: {str(e)}")
            raise


def get_or_create(model, **kwargs) -> Tuple[Any, bool]:
    """获取或创建模型实例

    Args:
        model: SQLAlchemy模型类
        **kwargs: 查询参数

    Returns:
        Tuple[实例, 是否新创建]
    """
    defaults = kwargs.pop("defaults", {})
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False

    kwargs.update(defaults)
    instance = model(**kwargs)
    with session_scope() as session:
        session.add(instance)
    return instance, True


def safe_commit() -> bool:
    """安全地提交数据库更改

    Returns:
        bool: 是否成功提交
    """
    try:
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Failed to commit changes: {str(e)}")
        return False


def safe_delete(instance) -> bool:
    """安全地删除数据库实例

    Args:
        instance: 要删除的数据库实例

    Returns:
        bool: 是否成功删除
    """
    try:
        db.session.delete(instance)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Failed to delete instance: {str(e)}")
        return False


def get_by_id(model, id: int) -> Optional[Any]:
    """通过ID获取模型实例

    Args:
        model: SQLAlchemy模型类
        id: 实例ID

    Returns:
        Optional[Any]: 找到的实例或None
    """
    return model.query.get(id)


def get_all(model) -> list:
    """获取模型的所有实例

    Args:
        model: SQLAlchemy模型类

    Returns:
        list: 所有实例的列表
    """
    return model.query.all()


def filter_by(model, **kwargs) -> list:
    """根据条件过滤模型实例

    Args:
        model: SQLAlchemy模型类
        **kwargs: 过滤条件

    Returns:
        list: 符合条件的实例列表
    """
    return model.query.filter_by(**kwargs).all()
