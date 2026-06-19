import streamlit as st
import config
from billing_calculator import BillingCalculator

# Cấu hình trang
st.set_page_config(
    page_title="Food Billing System",
    page_icon="🍽️",
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f5f5;
        }
        .main-header {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .bill-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        .total-amount {
            font-size: 28px;
            font-weight: bold;
            color: #2e7d32;
            text-align: right;
            padding: 15px;
            border-top: 2px solid #2e7d32;
            margin-top: 10px;
        }
        .food-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }
        .item-name {
            font-weight: 500;
        }
        .item-price {
            color: #1a73e8;
        }
        .note-text {
            color: #757575;
            font-size: 12px;
            font-style: italic;
        }
        .stButton button {
            width: 100%;
            border-radius: 8px;
        }
        .quantity-input {
            max-width: 80px;
        }
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 10px;
            margin: 10px 0;
        }
        .menu-item {
            background-color: white;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            cursor: pointer;
            transition: all 0.3s;
        }
        .menu-item:hover {
            border-color: #1a73e8;
            box-shadow: 0 2px 8px rgba(26,115,232,0.2);
        }
        .menu-item.selected {
            border-color: #1a73e8;
            background-color: #e8f0fe;
        }
        .bill-header {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

def init_session_state():
    """Khởi tạo session state"""
    if 'calculator' not in st.session_state:
        st.session_state.calculator = BillingCalculator()
    if 'selected_food' not in st.session_state:
        st.session_state.selected_food = None

def add_food_to_bill(food_name):
    """Thêm món ăn vào hóa đơn"""
    calculator = st.session_state.calculator
    calculator.add_item(food_name)
    st.session_state.selected_food = None
    st.rerun()

def display_bill():
    """Hiển thị hóa đơn"""
    calculator = st.session_state.calculator
    bill_details = calculator.get_bill_details()
    
    if not bill_details['items']:
        st.info("Chưa có món ăn nào trong hóa đơn")
        return
    
    # Header hóa đơn
    st.markdown("""
        <div class="bill-header">
            <span>Món ăn</span>
            <span style="margin-left: auto; padding-right: 20px;">Số lượng</span>
            <span style="padding-right: 20px;">Đơn giá</span>
            <span>Thành tiền</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị từng món
    for idx, item in enumerate(bill_details['items']):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1.5, 0.5])
        
        with col1:
            st.markdown(f"**{item['name']}**")
            if item.get('note'):
                st.markdown(f'<span class="note-text">{item["note"]}</span>', unsafe_allow_html=True)
        
        with col2:
            # Input số lượng
            new_qty = st.number_input(
                "",
                min_value=1,
                max_value=99,
                value=item['quantity'],
                key=f"qty_{idx}",
                label_visibility="collapsed"
            )
            if new_qty != item['quantity']:
                calculator.update_quantity(idx, new_qty)
                st.rerun()
        
        with col3:
            st.markdown(f'<span class="item-price">{item["price"]:,}đ</span>', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'**{item["subtotal"]:,}đ**')
        
        with col5:
            if st.button("×", key=f"del_{idx}", use_container_width=True):
                calculator.remove_item(idx)
                st.rerun()
    
    # Tổng tiền
    st.markdown(f"""
        <div class="total-amount">
            Tổng cộng: {bill_details['total']:,} VND
        </div>
    """, unsafe_allow_html=True)
    
    # Nút xóa hóa đơn
    if st.button("Xóa hóa đơn", type="secondary", use_container_width=True):
        calculator.clear_bill()
        st.rerun()

def main():
    init_session_state()
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0; color: #1a73e8;">🍽️ Food Billing System</h1>
            <p style="margin: 5px 0 0 0; color: #666;">Tính tiền món ăn tự động</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Layout chính
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📋 Thực đơn")
        
        # Hiển thị menu dạng grid
        menu_items = list(config.FOOD_MENU.items())
        cols_per_row = 3
        
        for i in range(0, len(menu_items), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(menu_items):
                    food_name, food_info = menu_items[i + j]
                    with cols[j]:
                        with st.container():
                            st.markdown(f"""
                                <div class="menu-item">
                                    <div style="font-weight: 500;">{food_name}</div>
                                    <div style="color: #1a73e8; font-weight: bold;">{food_info['price']:,}đ</div>
                                    <div style="font-size: 11px; color: #666;">{food_info['note']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"Thêm", key=f"add_{food_name}", use_container_width=True):
                                add_food_to_bill(food_name)
    
    with col_right:
        st.subheader("🧾 Hóa đơn")
        display_bill()
        
        # Thêm thông tin
        with st.expander("ℹ️ Hướng dẫn"):
            st.write("""
                1. Chọn món ăn từ thực đơn bên trái
                2. Món ăn sẽ tự động thêm vào hóa đơn
                3. Điều chỉnh số lượng nếu cần
                4. Xem tổng tiền tự động tính
            """)

if __name__ == "__main__":
    main()
