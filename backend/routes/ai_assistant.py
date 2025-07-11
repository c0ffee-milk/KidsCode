from flask import Blueprint, request, jsonify
from extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from model import User, VerificationCode
from config import Config
import logging
from services.ai_service import AIService

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/ai_analyze', methods=['POST'])
@jwt_required()
def ai_analyze():
    """
    获取ai分析
    Args:
        subject: 题目
        content: 回答内容

    返回:
        成功:
            message: 获取成功
            respond: {
                is_right: 正误判断
                analysis: 建议内容
            }
        失败:
            error: 错误信息
    """
    try:
        subject = request.json.get('subject')
        content = request.json.get('content')

        if not all([subject, content]):
            return jsonify(error='缺少必要参数'), 400
        
        ai_service = AIService()
        respond = ai_service.get_analysis(subject, content)

        if(respond == False):
            return jsonify(error='AI服务获取失败'), 500
        
        return jsonify({
            'message': '获取成功',
            'respond': respond
        })
    
    except Exception as e:
        return jsonify(error=str(e)), 500


