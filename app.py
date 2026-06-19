import streamlit as st
import os
import tempfile
from food_detector import FoodDetector
from billing_calculator import BillingCalculator
import config
from PIL import Image
import cv2
import numpy as np

# Cấu hình trang
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON if config.PAGE_ICON else None,
    layout="centered"
)

# CSS tùy chỉnh để giao diện tối giản
st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        .bill-item {
            padding: 10px;
            border-bottom: 1px solid #f0f0f0;
        }
        .total-amount {
            font-size: 24px;
            font-weight: bold;
            color: #2e7d32;
            text-align: right;
            padding: 20px;
            border-top: 2px solid #2e7d32;
        }
        .stButton button {
            width: 100%;
        }
        .detection-result {
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        .food-name {
            font-weight: bold;
            text-transform: capitalize;
        }
        .price {
            color: #1a73e8;
        }
        .note {
            color: #757575;
            font-size: 12px;
        }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Khởi tạo session state"""
    if 'detector' not in st.session_state:
        st.session_state.detector = FoodDetector()
    if 'calculator' not in st.session_state:
        st.session_state.calculator = BillingCalculator()
    if 'detected_foods' not in st.session_state:
        st.session_state.detected_foods = []
    if 'bill_details' not in st.session_state:
        st.session_state.bill_details = None

def process_image(image_file):
    """Xử lý ảnh và phát hiện món ăn"""
    try:
        # Lưu ảnh tạm thời
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_file.getvalue())
            temp_path = tmp_file.name
        
        # Phát hiện món ăn
        detector = st.session_state.detector
        detected_foods = detector.detect_foods(temp_path)
        
        # Xóa file tạm
        os.unlink(temp_path)
        
        return detected_foods
    
    except Exception as e:
        st.error(f"Loi xu ly anh: {str(e)}")
        return []

def display_bill(bill_details):
    """Hiển thị hóa đơn"""
    if not bill_details or not bill_details['items']:
        st.info("Khong phat hien mon an nao trong anh")
        return
    
    st.subheader("Hoa don")
    
    # Hiển thị từng món
    for item in bill_details['items']:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
        with col1:
            st.markdown(f'<span class="food-name">{item["name"]}</span>', unsafe_allow_html=True)
            if item.get('note'):
                st.markdown(f'<span class="note">{item["note"]}</span>', unsafe_allow_html=True)
        with col2:
            st.write(f"{item['count']}")
        with col3:
            st.write(f"{item['price']:,}")
        with col4:
            st.write(f"{item['subtotal']:,}")
    
    # Tổng tiền
    st.markdown(f"""
        <div class="total-amount">
            Tong cong: {bill_details['total']:,} VND
        </div>
    """, unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header"><h1>Food Billing System</h1></div>', unsafe_allow_html=True)
    
    # Sidebar - Hướng dẫn
    with st.sidebar:
        st.subheader("Huong dan")
        st.write("1. Tai anh mon an len")
        st.write("2. He thong se tu dong phat hien")
        st.write("3. Xem hoa don duoc tao")
        st.write("---")
        st.write("Mon an ho tro:")
        for food in config.FOOD_PRICES.keys():
            price = config.FOOD_PRICES[food]
            st.write(f"- {food.title()}: {price:,} VND")
    
    # Main content
    tab1, tab2 = st.tabs(["Tai anh", "Hoa don"])
    
    with tab1:
        # Upload file
        uploaded_file = st.file_uploader(
            "Chon anh mon an",
            type=['jpg', 'jpeg', 'png'],
            help="Tai anh len de he thong tu dong phat hien mon an"
        )
        
        if uploaded_file is not None:
            # Hiển thị ảnh
            image = Image.open(uploaded_file)
            st.image(image, caption='Anh da tai', use_column_width=True)
            
            # Nút phát hiện
            if st.button("Phat hien mon an", type="primary"):
                with st.spinner("Dang phan tich anh..."):
                    detected_foods = process_image(uploaded_file)
                    
                    if detected_foods:
                        st.session_state.detected_foods = detected_foods
                        calculator = st.session_state.calculator
                        bill_details = calculator.calculate_bill(detected_foods)
                        st.session_state.bill_details = bill_details
                        
                        st.success(f"Da phat hien {len(detected_foods)} mon an")
                        
                        # Hiển thị kết quả tạm thời
                        st.markdown("**Mon an phat hien:**")
                        for food in detected_foods:
                            st.markdown(f"""
                                <div class="detection-result">
                                    <span class="food-name">{food['name']}</span>
                                    <span class="price">- {food['price']:,} VND</span>
                                    {f'<span class="note">({food["note"]})</span>' if food.get('note') else ''}
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("Khong phat hien mon an nao. Vui long thu lai voi anh khac.")
    
    with tab2:
        # Hiển thị hóa đơn
        if st.session_state.bill_details:
            display_bill(st.session_state.bill_details)
        else:
            st.info("Chua co hoa don. Hay tai anh va phat hien mon an truoc.")

if __name__ == "__main__":
    main()
