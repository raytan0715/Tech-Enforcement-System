import os
import cv2
import numpy as np
import torch
import easyocr
import pytesseract
from PIL import Image
from pathlib import Path

# 定義常量
CONFIDENCE_THRESHOLD = 0.3

# 載入自訂YOLO模型
def load_model():
    try:
        model = torch.hub.load('yolov5', 'custom', path='model/runs/train/car_yolo6/weights/best.pt', source='local')
        model.conf = CONFIDENCE_THRESHOLD  # 設置置信度閾值
        model.iou = 0.5  # 設置 IOU 閾值
        print(f"模型加載成功，標籤名稱: {model.names}")
        return model
    except Exception as e:
        print(f"加載 YOLO 模型時出錯: {str(e)}")
        return None

# 進行車牌偵測
def detect_license_plate_yolo(image_cv, model):
    results = model(image_cv)
    plates = []
    for box in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = box.tolist()
        if int(cls) == 0:  # 假設類別 0 是車牌
            if conf < CONFIDENCE_THRESHOLD:
                print(f"車牌信心值 ({conf:.2f}) 低於閾值。")
                continue
            x1 = max(0, int(x1))
            y1 = max(0, int(y1))
            x2 = min(image_cv.shape[1], int(x2))
            y2 = min(image_cv.shape[0], int(y2))
            plate = image_cv[y1:y2, x1:x2]
            plates.append((plate, conf))
    return plates

# 創建車牌圖片的處理變體
def create_processing_variations(image: np.ndarray):
    variations = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    variations.append(("gray", gray))

    # CLAHE 增強
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(gray)
    variations.append(("clahe", clahe_img))

    # Otsu 二值化
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variations.append(("binary_otsu", binary))

    # 自適應二值化
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    variations.append(("adaptive_gaussian", adaptive))

    # 中值濾波降噪
    median = cv2.medianBlur(gray, 3)
    variations.append(("median", median))

    return variations

# 使用 EasyOCR 進行車牌文字辨識
def recognize_plate_text_with_easyocr(image_variations):
    reader = easyocr.Reader(['en'])  # 使用 EasyOCR
    results = []

    for method, img in image_variations:
        # 進行 OCR 辨識
        ocr_result = reader.readtext(img)
        if ocr_result:
            text = ocr_result[0][1]  # 取得第一個識別結果
            results.append((method, text))
    
    return results

def recognize_license_plate(image_path):
    model = load_model()
    if model is None:
        print("模型加載失敗")
        return None

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    print(f"正在处理图像: {image_path}")
    
    plates = detect_license_plate_yolo(image_rgb, model)
    
    if not plates:
        print("未偵測到任何車牌，預設車牌為 000000")
        return ["無法辨識車牌"]

    license_plates = []
    
    for i, (plate, conf) in enumerate(plates):
        print(f"偵測到的車牌 {i + 1} (信心值: {conf:.2f})")
        
        image_variations = create_processing_variations(plate)
        ocr_results = recognize_plate_text_with_easyocr(image_variations)
        
        if ocr_results:
            best_method, best_text = ocr_results[0]
            best_text = best_text.replace(" ", "").upper()  # 將辨識文字轉為大寫
            
            # 找連續數字的起點和終點
            num_start = num_end = -1
            for j in range(len(best_text)):
                if best_text[j].isdigit():
                    if num_start == -1:
                        num_start = j
                    num_end = j
                elif num_start != -1:  # 遇到非數字，結束連續數字序列
                    break
            
            # 檢查連續數字前後是否有字母
            if num_start > 0 and best_text[num_start-1].isalpha():
                formatted_text = best_text[:num_start] + '-' + best_text[num_start:]
            elif num_end < len(best_text)-1 and best_text[num_end+1].isalpha():
                formatted_text = best_text[:num_end+1] + '-' + best_text[num_end+1:]
            else:
                formatted_text = best_text
                
            print(f"車牌 {i + 1}: {formatted_text} (方法: {best_method})")
            license_plates.append(formatted_text)
        else:
            print(f"車牌 {i + 1} 使用 OCR 未檢測到文字")
    
    return license_plates