from flask import app
from flask_sqlalchemy import SQLAlchemy
from decouple import config

# 初始化 SQLAlchemy
db = SQLAlchemy()

# 從環境變數或設定檔獲取資料庫 URL
DATABASE_URL = config('DATABASE_URL', default='mysql+pymysql://root:Ray_930715@localhost/traffic_enforcement')

VEHICLE_DATABASE_URL = config('VEHICLE_DATABASE_URL', default='mysql+pymysql://root:Ray_930715@localhost/vehicle_registration')

TRAFFIC_FINE_DATABASE_URL = config('TRAFFIC_FINE_DATABASE_URL', default='mysql+pymysql://root:Ray_930715@localhost/traffic_fines')
