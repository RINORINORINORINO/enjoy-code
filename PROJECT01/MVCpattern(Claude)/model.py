# model.py
class TradingCalculatorModel:
    def __init__(self):
        self.entry_price = 0.0
        self.target_price = 0.0
        self.leverage = 10
        self.capital_usd = 1000.0
        self.exchange_rate = 1450.0
        self.position = "Long"
        self.fee_rate = 0.0005  # 거래소 수수료 (0.05%)
        
        # 결과 저장
        self.leveraged_percent = 0.0
        self.actual_profit_usd = 0.0
        self.actual_profit_krw = 0.0
        self.calculation_error = False
        
    def calculate_profit(self):
        try:
            # 기본 수익률 계산
            if self.position == 'Long':
                profit_percent = ((self.target_price - self.entry_price) / self.entry_price * 100)
            else:  # Short
                profit_percent = ((self.entry_price - self.target_price) / self.entry_price * 100)
            
            # 수수료 반영한 레버리지 수익률
            self.leveraged_percent = (profit_percent * self.leverage) - (self.leverage * self.fee_rate * 100)
            
            # 실제 수익 계산
            self.actual_profit_usd = self.capital_usd * (self.leveraged_percent / 100)
            self.actual_profit_krw = self.actual_profit_usd * self.exchange_rate
            
            self.calculation_error = False
            return True
        except Exception:
            self.calculation_error = True
            return False
    
    def update_entry_price(self, value):
        try:
            self.entry_price = float(value)
            return self.calculate_profit()
        except ValueError:
            self.calculation_error = True
            return False
    
    def update_target_price(self, value):
        try:
            self.target_price = float(value)
            return self.calculate_profit()
        except ValueError:
            self.calculation_error = True
            return False
    
    def update_leverage(self, value):
        try:
            self.leverage = int(value)
            return self.calculate_profit()
        except ValueError:
            self.calculation_error = True
            return False
    
    def update_position(self, value):
        self.position = value
        return self.calculate_profit()
    
    def update_capital(self, value):
        try:
            self.capital_usd = float(value)
            return self.calculate_profit()
        except ValueError:
            self.calculation_error = True
            return False
    
    def update_exchange_rate(self, value):
        try:
            self.exchange_rate = float(value)
            return self.calculate_profit()
        except ValueError:
            self.calculation_error = True
            return False