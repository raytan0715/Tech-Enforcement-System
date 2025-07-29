from flask import Flask
from .endpoints.violations import upload_image
from api.endpoints.violations import violations_bp
from api.endpoints.manual import manual_bp  # 引入 manual 蓝图

def init_routes(app: Flask):
    # 註冊路由
    app.add_url_rule('/api/upload_image', 'upload_image', upload_image, methods=['POST'])
    # 註冊 Blueprint 路由
    app.register_blueprint(violations_bp, url_prefix='/api')
    app.register_blueprint(manual_bp, url_prefix='/api')

