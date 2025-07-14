from flask import Flask, jsonify, request
from flask_cors import CORS
import config
from extensions import db, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import logging
from logging.handlers import RotatingFileHandler
import os


def init_app(app):
    with app.app_context():
        try:
            # 创建数据库表
            db.create_all()
            
        except Exception as e:
            app.logger.error(f"初始化应用失败: {str(e)}")
            raise e
        

def create_app():
    # 初始化 Flask 应用
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config.Config)

    db.init_app(app)
    jwt.init_app(app)

    # 配置日志
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10240, 
        backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # 启用 CORS（解决微信小程序跨域问题）
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # 注册蓝图
    # 创建蓝图并设置前缀
    from routes.auth import auth_bp
    from routes.ai_assistant import ai_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')


    # 错误处理
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': '请先登录'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': '没有权限执行此操作'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': '请求的资源不存在'
        }), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f'Server Error: {str(error)}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': '服务器内部错误'
        }), 500
    
    # 测试路由
    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({
            'status': 'success',
            'message': 'pong'
        })
    
    # 刷新 JWT Token
    @app.route("/refresh", methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify({
            'status': 'success',
            'message': '刷新成功',
            'token': access_token
        })
    
    # 初始化应用
    init_app(app)
    return app


# 启动应用
if __name__ == '__main__':
    # 创建应用实例
    app = create_app()
    app.run(host='0.0.0.0', port=5000)