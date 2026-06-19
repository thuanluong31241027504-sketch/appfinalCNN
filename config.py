# Cấu hình giá món ăn và thông tin
FOOD_PRICES = {
    'com trang': 10000,
    'dau hu sot ca': 25000,
    'ca hu kho': 30000,
    'thit kho trung': 30000,
    'thit kho': 25000,
    'canh chua co ca': 25000,
    'canh chua khong ca': 10000,
    'suon nuong': 30000,
    'canh rau': 7000,
    'rau xao': 10000,
    'trung chien': 25000
}

FOOD_NOTES = {
    'com trang': 'Mot gia tien nhieu hay it',
    'thit kho trung': 'Mot trung, them 1 trung + 6000 dong',
    'canh rau': 'Cai hay muong',
    'rau xao': 'Lagim/cu san/dau que/dau dua'
}

# Cấu hình Roboflow
ROBOFLOW_API_KEY = "YOUR_API_KEY"  # Thay bằng API key của bạn
ROBOFLOW_MODEL_ID = "your-model-id"  # Thay bằng model ID
ROBOFLOW_MODEL_VERSION = 1  # Version của model

# Cấu hình Streamlit
PAGE_TITLE = "Food Billing System"
PAGE_ICON = "🍽️"  # Có thể bỏ nếu không muốn emoji
