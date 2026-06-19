import cv2
import numpy as np
from roboflow import Roboflow
import config
import os
from PIL import Image

class FoodDetector:
    def __init__(self):
        self.rf = None
        self.model = None
        self.initialize_model()
    
    def initialize_model(self):
        """Khởi tạo model từ Roboflow"""
        try:
            self.rf = Roboflow(api_key=config.ROBOFLOW_API_KEY)
            self.model = self.rf.workspace().project(config.ROBOFLOW_MODEL_ID).version(config.ROBOFLOW_MODEL_VERSION).model
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def detect_foods(self, image_path):
        """
        Phát hiện món ăn trong ảnh
        Returns: List các món ăn phát hiện được
        """
        if self.model is None:
            print("Model not initialized")
            return []
        
        try:
            # Dự đoán với model Roboflow
            result = self.model.predict(image_path, confidence=40, overlap=30)
            
            # Lấy danh sách các đối tượng phát hiện
            predictions = result.json()['predictions']
            
            detected_foods = []
            for pred in predictions:
                class_name = pred['class'].lower()
                confidence = pred['confidence']
                
                if class_name in config.FOOD_PRICES:
                    detected_foods.append({
                        'name': class_name,
                        'confidence': confidence,
                        'price': config.FOOD_PRICES[class_name],
                        'note': config.FOOD_NOTES.get(class_name, '')
                    })
            
            return detected_foods
            
        except Exception as e:
            print(f"Error during detection: {e}")
            return []
    
    def detect_with_cv2(self, image):
        """
        Phương pháp dự phòng sử dụng OpenCV cho detection cơ bản
        """
        # TODO: Implement detection với OpenCV nếu cần
        pass
