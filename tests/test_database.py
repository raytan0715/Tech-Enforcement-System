from config.database import SessionLocal
from model.database import Accident
from datetime import datetime

# 測試資料庫連線與資料插入
def test_database():
    db = SessionLocal()

    # 插入測試數據
    test_accident = Accident(
        cam_id="CAM-123",
        speed_limit=60,
        current_speed=80,
        licence_plate="ABC-1234",
        confidence=95.5,
        location="New York",
        date_time=datetime.now(),
        image="test.jpg"
    )
    db.add(test_accident)
    db.commit()
    db.refresh(test_accident)

    print(f"插入數據成功，ID: {test_accident.id}")
    db.close()

if __name__ == "__main__":
    test_database()
