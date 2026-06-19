import config

class BillingCalculator:
    def __init__(self):
        self.items = []
        self.total = 0
    
    def add_item(self, food_name, quantity=1, custom_price=None):
        """Thêm món ăn vào hóa đơn"""
        if food_name in config.FOOD_MENU:
            price = custom_price if custom_price else config.FOOD_MENU[food_name]['price']
            note = config.FOOD_MENU[food_name]['note']
            
            # Kiểm tra xem món đã có trong danh sách chưa
            for item in self.items:
                if item['name'] == food_name and item.get('custom_price') == custom_price:
                    item['quantity'] += quantity
                    item['subtotal'] = item['quantity'] * item['price']
                    self._calculate_total()
                    return
            
            self.items.append({
                'name': food_name,
                'quantity': quantity,
                'price': price,
                'subtotal': price * quantity,
                'note': note,
                'custom_price': custom_price
            })
            self._calculate_total()
    
    def remove_item(self, index):
        """Xóa món ăn khỏi hóa đơn"""
        if 0 <= index < len(self.items):
            del self.items[index]
            self._calculate_total()
    
    def update_quantity(self, index, new_quantity):
        """Cập nhật số lượng món ăn"""
        if 0 <= index < len(self.items) and new_quantity > 0:
            self.items[index]['quantity'] = new_quantity
            self.items[index]['subtotal'] = self.items[index]['price'] * new_quantity
            self._calculate_total()
    
    def _calculate_total(self):
        """Tính tổng tiền"""
        self.total = sum(item['subtotal'] for item in self.items)
    
    def clear_bill(self):
        """Xóa hóa đơn"""
        self.items = []
        self.total = 0
    
    def get_bill_details(self):
        """Lấy chi tiết hóa đơn"""
        return {
            'items': self.items,
            'total': self.total,
            'total_items': len(self.items),
            'total_quantity': sum(item['quantity'] for item in self.items)
        }
