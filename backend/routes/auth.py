from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, jwt, redis_client
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from model import User, RoleEnum
import requests
from config import Config
from sqlalchemy.exc import SQLAlchemyError
import logging
import base64
import json
from Cryptodome.Cipher import AES
from utils.csv_utils import verify_user_identity
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    登陆服务
    Args:
        user_name: 用户名
        password: 密码
    返回:
        成功:
            message: 登陆成功
            user_info: {
                id: 用户id
                user_name: 用户名
                token: 鉴权令牌
                refresh_token: 刷新令牌
            }
        失败:
            error: 错误信息
    """
    try:
        name = request.json.get('user_name')
        password = request.json.get('password')

        if not all([name, password]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        user = User.query.filter_by(user_name=name).first()
        if not user or not user.check_password(password):
            return jsonify({'error': '用户名或密码错误'}), 401
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'status': 'success',
            'message': '登录成功',
            'id': user.id,
            'user_name': user.user_name,
            'token': access_token,
            'refresh_token': refresh_token
        })
    except Exception as e:
        logging.error(f"登录过程发生错误: {str(e)}")
        return jsonify({'error': '系统错误'}), 500
    

@auth_bp.route('/register', methods=['POST']):
def register():
    """
    注册服务
    Args:
        user_name: 用户名
        password: 密码
    返回:
        成功:
            message: 登陆成功
            user_info: {
                id: 用户id
                user_name: 用户名
                token: 鉴权令牌
                refresh_token: 刷新令牌
            }
        失败:
            error: 错误信息
    """
    try:
        name = request.json.get('user_name')
        password = request.json.get('password')

        if not all([name, password]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        user = User(
            name=name,
            password=password
        )
        db.session.add(user)
        db.session.commit()

        # 生成令牌
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'status': 'success',
            'message': '注册成功',
            'id': user.id,
            'user_name': user.user_name,
            'token': access_token,
            'refresh_token': refresh_token
        })
    
    except Exception as e:
        logging.error(f"注册过程发生错误: {str(e)}")
        return jsonify({'error': '系统错误'}), 500