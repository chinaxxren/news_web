#!/bin/bash

# 设置错误时退出
set -e

# 应用名称和端口
APP_NAME="news_web"
PORT=5000
PID_FILE="app.pid"
LOG_FILE="app.log"

# 获取本机IP地址
get_ip() {
    if command -v ip &> /dev/null; then
        ip addr show | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | cut -d/ -f1 | head -n 1
    elif command -v ifconfig &> /dev/null; then
        ifconfig | grep "inet " | grep -v "127.0.0.1" | awk '{print $2}' | head -n 1
    else
        echo "无法获取IP地址"
        exit 1
    fi
}

# 获取进程ID
get_pid() {
    if [ -f $PID_FILE ]; then
        cat $PID_FILE
    else
        echo ""
    fi
}

# 停止应用
stop_app() {
    echo "停止开发服务器..."
    PID=$(get_pid)
    if [ ! -z "$PID" ]; then
        kill $PID 2>/dev/null || true
        rm -f $PID_FILE
        echo "开发服务器已停止"
    else
        echo "开发服务器未运行"
    fi
}

# 启动应用
start_app() {
    echo "启动开发服务器..."
    # 设置开发环境变量
    export FLASK_APP=run.py
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    
    # 获取本机IP
    IP=$(get_ip)
    if [ -z "$IP" ]; then
        echo "错误：无法获取本机IP地址"
        exit 1
    fi
    
    # 使用 python 运行应用
    nohup python run.py > $LOG_FILE 2>&1 &
    echo $! > $PID_FILE
    echo "开发服务器已启动，PID: $(get_pid)"
    echo "日志文件: $LOG_FILE"
    echo "本地访问地址: http://localhost:$PORT"
    echo "局域网访问地址: http://$IP:$PORT"
    echo "注意：确保防火墙已开放 $PORT 端口"
}

# 显示日志
show_log() {
    if [ -f $LOG_FILE ]; then
        tail -f $LOG_FILE
    else
        echo "日志文件不存在"
    fi
}

# 清理开发环境
clean() {
    echo "清理开发环境..."
    stop_app
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    find . -type f -name ".coverage" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    find . -type d -name "*.egg" -exec rm -rf {} +
    find . -type d -name ".pytest_cache" -exec rm -rf {} +
    find . -type d -name ".mypy_cache" -exec rm -rf {} +
    find . -type d -name ".coverage" -exec rm -rf {} +
    find . -type d -name "htmlcov" -exec rm -rf {} +
    rm -f $LOG_FILE
    echo "清理完成"
}

# 安装依赖
install_deps() {
    echo "安装项目依赖..."
    pip install -r requirements.txt
    echo "依赖安装完成"
}

# 运行测试
run_tests() {
    echo "运行测试..."
    pytest --cov=app tests/
}

# 代码格式化
format_code() {
    echo "格式化代码..."
    black .
    isort .
}

# 代码检查
check_code() {
    echo "检查代码..."
    flake8 .
    mypy .
}

# 显示帮助信息
show_help() {
    echo "开发环境管理脚本"
    echo "用法: ./dev.sh [命令]"
    echo ""
    echo "命令:"
    echo "  start    启动开发服务器"
    echo "  stop     停止开发服务器"
    echo "  restart  重启开发服务器"
    echo "  log      显示日志"
    echo "  clean    清理开发环境"
    echo "  install  安装项目依赖"
    echo "  test     运行测试"
    echo "  format   格式化代码"
    echo "  check    检查代码"
    echo "  help     显示帮助信息"
}

# 根据参数执行相应命令
case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        stop_app
        start_app
        ;;
    log)
        show_log
        ;;
    clean)
        clean
        ;;
    install)
        install_deps
        ;;
    test)
        run_tests
        ;;
    format)
        format_code
        ;;
    check)
        check_code
        ;;
    help|*)
        show_help
        ;;
esac 