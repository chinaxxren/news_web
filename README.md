# News Portal

一个基于 Flask + Bootstrap 的新闻资讯网站，支持文章发布、标签管理、后台管理、响应式布局等功能。

## 主要功能

- 文章展示与详情页
- 文章标签与主题
- 文章置顶、推荐、草稿、发布等状态
- 后台管理（文章增删改查）
- 用户登录/登出
- 响应式设计，适配移动端
- 一键社交分享

## 技术栈

- Python 3.x
- Flask
- Jinja2 模板
- Bootstrap 5
- SQLite

## 开发脚本（dev.sh）

本项目提供了 `dev.sh` 脚本，便于开发环境的管理和常用操作。

### 常用命令

```bash
# 启动开发服务器
./dev.sh start

# 停止开发服务器
./dev.sh stop

# 重启开发服务器
./dev.sh restart

# 查看日志
./dev.sh log

# 安装依赖
./dev.sh install

# 清理开发环境
./dev.sh clean

# 运行测试
./dev.sh test

# 代码格式化
./dev.sh format

# 代码检查
./dev.sh check
```

### 功能说明

- 自动检测本机 IP，支持局域网访问
- 支持日志输出与查看
- 一键清理 pycache、测试缓存等
- 支持 pytest 测试、black/isort 格式化、flake8/mypy 检查
- 适合本地开发和团队协作
