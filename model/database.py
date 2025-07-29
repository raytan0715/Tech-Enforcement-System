from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, BLOB
from flask_login import UserMixin
from config.database import db

class ViolationRecord(db.Model):
    __tablename__ = 'violation_records'

    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    speed_limit = db.Column(db.Integer, nullable=False)
    current_speed = db.Column(db.Integer, nullable=False)
    cam_id = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    longitude = Column(DECIMAL(9, 6), nullable=False)  # 新增經度欄位
    latitude = Column(DECIMAL(9, 6), nullable=False)   # 新增緯度欄位
    image = db.Column(db.LargeBinary, nullable=False)  # 修正這裡
    recognition = db.Column(db.Integer, nullable=False)
    error_code = db.Column(db.Integer, nullable=False)
    ticket = db.Column(db.Integer)

    def __repr__(self):
        return f'<ViolationRecord {self.license_plate} at {self.location}>'

    # 方法來儲存圖片為二進位格式
    def save_image(self, image_file):
        # 將圖片轉為二進位格式並儲存
        with open(image_file, 'rb') as f:
            self.image = f.read()  # 修正這裡，將圖片儲存在 'image' 欄位
