from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()