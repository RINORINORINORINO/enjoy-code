import tkinter as tk
from model import TradingCalculatorModel
from view import TradingCalculatorView
from controller import TradingCalculatorController

def main():
    # MVC 패턴 구성
    model = TradingCalculatorModel()
    controller = TradingCalculatorController(model)
    
    root = tk.Tk()
    view = TradingCalculatorView(root, controller)
    
    root.mainloop()

if __name__ == "__main__":
    main()