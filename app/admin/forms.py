from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class ArticleForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired(), Length(max=200)])
    subtitle = StringField("副标题", validators=[Length(max=200)])
    content = TextAreaField("内容", validators=[DataRequired()])
    tags = StringField("标签（用逗号分隔）")
    is_published = BooleanField("发布")
    is_top = BooleanField("置顶")
    is_recommended = BooleanField("推荐")
    submit = SubmitField("提交")


class TagForm(FlaskForm):
    name = StringField("标签名称", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("提交")


class UserForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[Length(min=8)])
    password2 = PasswordField("确认密码", validators=[EqualTo("password")])
    is_admin = BooleanField("管理员权限")
    submit = SubmitField("提交")

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("用户名已存在")

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError("邮箱已存在")


class ImageUploadForm(FlaskForm):
    image = FileField(
        "选择图片",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png", "gif"], "只允许上传图片文件!"),
        ],
    )
    submit = SubmitField("上传")
