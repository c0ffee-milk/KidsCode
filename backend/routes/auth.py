from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from model import User, VerificationCode
import requests
from config import Config
from sqlalchemy.exc import SQLAlchemyError
import logging
import base64
import json
from datetime import timedelta
from utils.sms_service import generate_code, send_sms, save_verification_code, verify_code
from werkzeug.security import generate_password_hash, check_password_hash

import random
import string

auth_bp = Blueprint('auth', __name__)

def generate_random_username(length=10):
    prefix = "user_"
    # 保证总长度不超过64
    random_part_length = min(length, 64 - len(prefix))
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random_part_length))
    return prefix + random_part

def get_unique_username():
    while True:
        username = generate_random_username()
        if not User.query.filter_by(name=username).first():
            return username


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login_with_code', methods=['POST'])
def login_with_code():
    """
    登陆服务
    Args:
        phone: 手机号
        code: 验证码
    返回:
        成功:
            message: 登陆成功
            user_info: {
                id: 用户id
                name: 用户名
                token: 鉴权令牌
                refresh_token: 刷新令牌
            }
        失败:
            error: 错误信息
    """
    try:
        phone = request.json.get('phone')
        code = request.json.get('code')

        if not all([phone, code]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 校验验证码
        if not verify_code(phone, code):
            return jsonify({'error': '验证码无效或已过期'}), 400
        
        user = User.query.filter_by(phone=phone).first()
        if not user:
            name = get_unique_username()
            password = generate_password_hash(phone)
            user = User(
                name=name,
                password=generate_password_hash(password),
                phone=phone
            )
            # 使用后删除验证码
            code = VerificationCode.query.filter_by(phone=phone).first()
            db.session.delete(code)
            db.session.add(user)
            db.session.commit()

            # 生成令牌
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({
                'status': 'success',
                'message': '未查询到用户，已自动注册',
                'id': user.id,
                'name': user.name,
                'token': access_token,
                'refresh_token': refresh_token
            })
        
        else:
            # 使用后删除验证码
            code = VerificationCode.query.filter_by(phone=phone).first()
            db.session.delete(code)
            db.session.commit()

            # 生成令牌
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({
                'status': 'success',
                'message': '登陆成功',
                'id': user.id,
                'name': user.name,
                'token': access_token,
                'refresh_token': refresh_token
            })
        
    except Exception as e:
        logging.error(f"登录过程发生错误: {str(e)}")
        return jsonify({'error': '系统错误'}), 500
    

@auth_bp.route('/login_with_password', methods=['POST'])
def login_with_password():
    """
    登陆服务
    Args:
        phone: 手机号
        password: 密码
    返回:
        成功:
            message: 登陆成功
            user_info: {
                id: 用户id
                name: 用户名
                token: 鉴权令牌
                refresh_token: 刷新令牌
            }
        失败:
            error: 错误信息
    """
    try: 
        phone = request.json.get('phone')
        password = request.json.get('password')
        if not all([phone, password]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        user = User.query.filter_by(phone=phone).first()
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        if check_password_hash(user.password, password):
            # 登陆成功
            # 生成令牌
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({
                'status': 'success',
                'message': '登陆成功',
                'id': user.id,
            })
        else:
            return jsonify({'error': '密码错误'}), 401
        
    except Exception as e:
        logging.error(f"登录过程发生错误: {str(e)}")
        return jsonify({'error': '系统错误'}), 500
    

@auth_bp.route('/self_info', methods=['GET'])
@jwt_required()
def self_info():
    """
    编辑用户信息
    Args:
        无
    返回:
        成功:
            message: 获取成功
            user_info: {
                name: 用户名
                phone: 手机号
            }
        失败:
            error: 错误信息
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        return jsonify({
            'status': 'success',
            'message': '获取成功',
            'name': user.name,
            'phone': user.phone
        })
    except Exception as e:
        logging.error()


@auth_bp.route('/update-info', methods=['POST'])
@jwt_required()
def update_info():
    """
    更新用户信息
    Args:
        name: 用户名
        phone: 手机号
        password: 密码
        code: 验证码
    返回:
        成功:
            message: 更新成功
        失败:
            error: 错误信息
    """
    try: 
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        name = request.json.get('name')
        phone = request.json.get('phone')
        password = request.json.get('password')
        code = request.json.get('code')

        if not all([name, phone, code]):
            return jsonify({'error': '缺少必要参数'}), 400
        
        if not verify_code(phone, code):
            return jsonify({'error': '验证码无效或已过期'}), 400
        
        # 检查用户名是否被其他用户占用
        if User.query.filter(User.name == name, User.id != user_id).first():
            return jsonify({'error': '用户名已被占用'}), 400

        # 检查手机号是否被其他用户占用
        if User.query.filter(User.phone == phone, User.id != user_id).first():
            return jsonify({'error': '手机号已被占用'}), 400
        
        user.name = name
        user.phone = phone
        user.password = generate_password_hash(password)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': '更新成功'
        })

    except Exception as e:
        logging.error(f"更新用户信息过程发生错误: {str(e)}")
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
