from flask import Blueprint, request, jsonify
import os
import uuid
from services.ai_recognition import recognize_license_plate
from services.violation_process import process_violation
import requests

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoicmF5dGFuIiwiYSI6ImNtNHRpaXFrMDBiZGcyanBvZ21xcXl5NnAifQ.sKCK5cCaw7Sns6uIkdIZvQ'

# 設定圖片上傳的目錄
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 檢查檔案格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

violations_bp = Blueprint('violations', __name__)

@violations_bp.route('/upload_image', methods=['POST'])
def upload_image():
    # 检查图片文件
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(image.filename):
        return jsonify({'error': 'Invalid file format'}), 400

    # 保存图片
    file_extension = image.filename.rsplit('.', 1)[1].lower()
    new_filename = str(uuid.uuid4()) + '.' + file_extension
    filename = os.path.join(UPLOAD_FOLDER, new_filename)
    image.save(filename)

    # 获取表单数据
    location = request.form['location']
    speed_limit = request.form['speed_limit']
    current_speed = request.form['current_speed']
    cam_id = request.form['cam_id']
    date_time = request.form['date_time']

    try:
        # 转换地址为经纬度
        longitude, latitude = get_coordinates_from_address(location)
        if longitude is None or latitude is None:
            return jsonify({'error': '无法解析地址'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # 调用 AI 识别服务
    license_plate = recognize_license_plate(filename)

    if license_plate:
        process_violation(
            license_plate, location, speed_limit, current_speed,
            cam_id, date_time, filename, longitude, latitude
        )
        os.remove(filename)
        return jsonify({'message': 'Violation recorded successfully', 'license_plate': license_plate})
    else:
        os.remove(filename)
        return jsonify({'error': 'License plate not recognized'}), 400
    
def get_coordinates_from_address(address):
    """调用 Mapbox API 将地址转换为经纬度"""
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
    params = {
        "access_token": MAPBOX_ACCESS_TOKEN,
        "limit": 1,
        "language": "zh-TW"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            longitude, latitude = data['features'][0]['center']
            return longitude, latitude
        else:
            return None, None
    else:
        raise Exception(f"Mapbox API 请求失败: {response.status_code}")