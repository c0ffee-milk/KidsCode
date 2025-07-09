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
from utils.sms_service import generate_code, send_sms, save_verification_code, verify_code

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
    

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    注册服务
    Args:
        user_name: 用户名
        phone: 手机号
        password: 密码
        code: 验证码
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
        phone = request.json.get('phone')
        password = request.json.get('password')
        code = request.json.get('code')

        if not all([name, phone, password, code]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 校验验证码
        if not verify_code(phone, code):
            return jsonify({'error': '验证码无效或已过期'}), 400
            
        # 检查手机号是否已被注册
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            return jsonify({'error': '该手机号已被注册'}), 400


        user = User(
            name=name,
            phone=phone,
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
    

@auth_bp.route('/send-code', methods=['POST'])
def send_code():
    phone = request.json.get('phone')
    if not phone:
        return jsonify({"error": "手机号不能为空"}), 400
    code = generate_code()
    if send_sms(phone, code):
        save_verification_code(phone, code)
        return jsonify({"message": "验证码已发送，请注意查收"})
    else:
        return jsonify({"error": "发送验证码失败"}), 500
