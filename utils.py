import cv2
import numpy as np
from PIL import Image
import io

def preprocess_image(image):
    """Tiền xử lý ảnh trước khi đưa vào model"""
    # Chuyển đổi sang RGB nếu cần
    if isinstance(image, np.ndarray):
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
    # Resize nếu cần
    # image = cv2.resize(image, (640, 640))
    
    return image

def save_uploaded_file(uploaded_file):
    """Lưu file upload vào thư mục temp"""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

def format_currency(amount):
    """Định dạng tiền tệ"""
    return f"{amount:,} VND"
