import config
from collections import Counter

class BillingCalculator:
    def __init__(self):
        self.food_counts = {}
        self.total_amount = 0
        self.detected_items = []
    
    def calculate_bill(self, detected_foods):
        """
        Tính tiền dựa trên danh sách món ăn phát hiện
        """
        self.detected_items = detected_foods
        self.food_counts = Counter([item['name'] for item in detected_foods])
        
        self.total_amount = sum([
            item['price'] for item in detected_foods
        ])
        
        return self.get_bill_details()
    
    def get_bill_details(self):
        """
        Trả về chi tiết hóa đơn
        """
        if not self.detected_items:
            return {
                'items': [],
                'total': 0,
                'summary': 'Khong phat hien mon an nao'
            }
        
        # Nhóm các món ăn theo tên
        items_summary = []
        for food_name, count in self.food_counts.items():
            price = config.FOOD_PRICES.get(food_name, 0)
            note = config.FOOD_NOTES.get(food_name, '')
            items_summary.append({
                'name': food_name,
                'count': count,
                'price': price,
                'subtotal': price * count,
                'note': note
            })
        
        return {
            'items': items_summary,
            'total': self.total_amount,
            'summary': f'Tong cong: {self.total_amount:,} VND'
        }
