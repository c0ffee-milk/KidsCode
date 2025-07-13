from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def generate_token(self):
        """生成JWT Token"""
        expires = timedelta(days=1)
        return create_access_token(identity={'id': self.id}, expires_delta=expires)
    

class VerificationCode(db.Model):
    """验证码"""
    __tablename__ = 'verification_codes'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(11), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Record(db.Model):
    """做题记录"""
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(1000), nullable=False)
    answer = db.Column(db.String(1000), nullable=False)
    comment = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

