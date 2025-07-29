import torch
import torchvision
from ultralytics import YOLO

# # 測試 CUDA 是否可用
# print("CUDA 是否可用:", torch.cuda.is_available())
# print("CUDA 版本:", torch.version.cuda)
# print("PyTorch 版本:", torch.__version__)
# print("Torchvision 版本:", torchvision.__version__)
# print("GPU 名稱:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "無")

#  # 測試 torchvision.ops.nms
# from torchvision.ops import nms
# try:
#     boxes = torch.tensor([[0, 0, 10, 10], [1, 1, 11, 11]], dtype=torch.float32).cuda()
#     scores = torch.tensor([0.9, 0.8], dtype=torch.float32).cuda()
#     iou_threshold = 0.5
#     result = nms(boxes, scores, iou_threshold)
#     print("NMS 測試通過，結果:", result)
# except Exception as e:
#     print("NMS 測試失敗，錯誤:", e)

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 加載預設的 yolov5s.pt 模型

model = torch.hub.load('./yolov5', 'custom', path='./runs/train/car_yolo6/weights/best.pt', source='local')


try:
    print("模型加載成功，標籤名稱:", model.names)
except Exception as e:
    print("加載 YOLO 模型失敗，錯誤:", e)

# 測試推論
results = model("images\\unnamed.jpg")  # 替換為您的測試圖片路徑
results.show()  # 顯示檢測結果