import os
from datetime import timedelta

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///KidsCode.db' # 使用 SQLite 作为开发数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG  # 在调试模式下打印SQL语句
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '114514')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  # token过期时间
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 刷新token过期时间

    # 跨域配置
    CORS_ORIGINS = ['*']  # 在生产环境中应该设置具体的域名

    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')