class TradingCalculatorController:
    def __init__(self, model):
        self.model = model
        self.view = None  # 명시적으로 view 속성 초기화
    
    def calculate_profit(self):
        success = self.model.calculate_profit()
        if hasattr(self, 'view') and self.view is not None:  # view 속성 존재 확인
            self.view.update_results(
                self.model.leveraged_percent,
                self.model.actual_profit_usd,
                self.model.actual_profit_krw,
                self.model.calculation_error
            )
        return success
    
    def set_view(self, view):
        self.view = view
    
    def update_entry_price(self, value):
        success = self.model.update_entry_price(value)
        if hasattr(self, 'view') and self.view is not None:
            self.view.update_results(
                self.model.leveraged_percent,
                self.model.actual_profit_usd,
                self.model.actual_profit_krw,
                self.model.calculation_error
            )
        return success
    
    def update_target_price(self, value):
        success = self.model.update_target_price(value)
        if hasattr(self, 'view') and self.view is not None:
            self.view.update_results(
                self.model.leveraged_percent,
                self.model.actual_profit_usd,
                self.model.actual_profit_krw,
                self.model.calculation_error
            )
        return success
    
    def update_leverage(self, value):
        success = self.model.update_leverage(value)
        if hasattr(self, 'view') and self.view is not None:
            self.view.update_results(
                self.model.leveraged_percent,
                self.model.actual_profit_usd,
                self.model.actual_profit_krw,
                self.model.calculation_error
            )
        return success
    
    def update_position(self, value):
        success = self.model.update_position(value)
        if hasattr(self, 'view') and self.view is not None:
            self.view.update_results(
                self.model.leveraged_percent,
                self.model.actual_profit_usd,
                self.model.actual_profit_krw,
                self.model.calculation_error
            )
        return success
    
    def update_capital(self, value):
        success = self.model.update_capital(value)
        if hasattr(self, 'view') and self.view is not None:
            self.view.update_results(
                self.model.leveraged_percent,
                self.model.actual_profit_usd,
                self.model.actual_profit_krw,
                self.model.calculation_error
            )
        return success
    
    def update_exchange_rate(self, value):
        success = self.model.update_exchange_rate(value)
        if hasattr(self, 'view') and self.view is not None:
            self.view.update_results(
                self.model.leveraged_percent,
                self.model.actual_profit_usd,
                self.model.actual_profit_krw,
                self.model.calculation_error
            )
        return success