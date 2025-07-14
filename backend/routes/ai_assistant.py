from flask import Blueprint, request, jsonify
from extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from model import User, Record
from config import Config
import logging
from backend.utils.ai_service import AIService

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


@ai_bp.route('/ai_judge', methods=['POST'])
@jwt_required()
def ai_judge():
    """
    ai判定与评价
    Args:
        subject: 题目
        content: 回答内容

    返回:
        成功:
            message: 获取成功
            respond: {
                movement: 行动指令序列,
                is_right: 正误判断
            }
        失败:
            error: 错误信息
    """
    try:
        subject = request.json.get('subject')
        content = request.json.get('content')

        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404

        if not all([subject, content]):
            return jsonify(error='缺少必要参数'), 400
        
        ai_service = AIService()
        respond = ai_service.ai_judge(subject, content)

        if(respond == False):
            return jsonify(error='AI服务获取失败'), 500
        
        movement = respond['movement']
        is_right = respond['is_right']
        comment = respond['result']

        record = Record(
            user_id=user_id,
            question=subject,
            answer=content,
            comment=comment
        )

        db.session.add(record)
        db.session.commit()
        
        return jsonify({
            'message': '获取成功',
            'respond': {
                'movement': movement,
                'is_right': is_right
            }
        })
    
    except Exception as e:
        return jsonify(error=str(e)), 500


@ai_bp.route('/ai_evaluate', methods=['POST'])
@jwt_required()
def ai_evaluate():
    """
    获取ai评估
    Args:
        无

    返回:
        成功:
            message: 获取成功
            respond: {
                score: {
                        "逻辑思维": score1,
                        "创造力": score2,
                        "问题解决": score3,
                        "代码规范": score4,
                        "空间想象": score5
                    },
                comment: 总体评价
            }
        失败:
            error: 错误信息
    """
    try:
        user_id = get_jwt_identity()
        infos = []
        record = Record.query.filter_by(user_id=user_id).all()
        for info in record:
            infos.append(info.comment)

        if len(infos) == 0:
            return jsonify(error='缺少必要参数'), 400
        
        ai_service = AIService()
        respond = ai_service.ai_evaluate(infos)

        if(respond == False):
            return jsonify(error='AI服务获取失败'), 500
        
        return jsonify({
            'message': '获取成功',
            'respond': {
                'score': respond['score'],
                'comment': respond['comment']
            }
        })
    
    except Exception as e:
        return jsonify(error=str(e)), 500
