from datetime import datetime


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


def register_filters(app):
    app.jinja_env.filters["short_time_ago"] = short_time_ago
