import tkinter as tk

class TradingCalculatorView:
    def __init__(self, root, controller):
        self.controller = controller
        controller.set_view(self)  # 컨트롤러에 즉시 뷰 설정
        
        # 스타일
        self.bg_color = "#1C1C1C"
        self.entry_bg = "#3A3A3C"
        self.entry_fg = "white"
        self.label_box_bg = "#E6E6E6"
        self.label_fg = "#111111"
        self.accent_color = "#FFA500"
        self.label_font = ("Malgun Gothic", 13, "bold")
        self.large_font = ("Malgun Gothic", 18, "bold")
        self.entry_font = ("Segoe UI", 13, "bold")
        
        # 메인 윈도우 설정
        self.root = root
        self.root.title("트레이딩 수익/손실 바로미터")
        self.root.configure(bg=self.bg_color)
        self.root.geometry("560x560")
        self.root.minsize(560, 560)
        self.root.resizable(True, True)
        
        # 메인 컨테이너
        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=2)
        
        # UI 요소들 생성
        self.create_ui_elements()
        
        # 초기 계산 실행
        self.controller.calculate_profit()
    
    def create_ui_elements(self):
        row = 0
        
        # 진입 가격
        self.box_label("진입 가격").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
        self.entry_entry_price = self.styled_entry()
        self.entry_entry_price.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)
        self.entry_entry_price.bind("<KeyRelease>", lambda event: self.controller.update_entry_price(self.entry_entry_price.get()))
        
        row += 1
        # 목표 가격
        self.box_label("목표 가격").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
        self.entry_target_price = self.styled_entry()
        self.entry_target_price.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)
        self.entry_target_price.bind("<KeyRelease>", lambda event: self.controller.update_target_price(self.entry_target_price.get()))
        
        row += 1
        # 레버리지
        self.box_label("레버리지 (1~125)").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
        frame_leverage = tk.Frame(self.container, bg=self.bg_color)
        self.scale_leverage = tk.Scale(frame_leverage, from_=1, to=125, orient=tk.HORIZONTAL,
                              resolution=1, showvalue=False, command=self.handle_leverage_scale,
                              bg=self.bg_color, troughcolor="#555555", highlightthickness=0)
        self.scale_leverage.set(10)
        self.scale_leverage.pack(side=tk.LEFT, fill='x', expand=True)
        
        self.entry_leverage = tk.Entry(frame_leverage, width=5, bg=self.entry_bg, fg=self.entry_fg,
                              font=self.entry_font, justify='center', insertbackground='white',
                              relief="flat", bd=0, highlightthickness=2, highlightbackground="#888888")
        self.entry_leverage.insert(0, "10")
        self.entry_leverage.pack(side=tk.LEFT, padx=5)
        self.entry_leverage.bind("<KeyRelease>", self.handle_leverage_entry)
        frame_leverage.grid(row=row, column=1, sticky='ew', pady=5)
        
        row += 1
        # 포지션
        self.box_label("포지션").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
        frame_position = tk.Frame(self.container, bg=self.bg_color)
        self.position_var = tk.StringVar(value="Long")
        self.radio_long = tk.Radiobutton(frame_position, text="롱", variable=self.position_var, value="Long",
                                    command=self.handle_position_change,
                                    bg=self.bg_color, fg=self.accent_color, selectcolor=self.bg_color,
                                    font=self.entry_font, activebackground=self.bg_color)
        self.radio_long.pack(side=tk.LEFT, padx=10)
        self.radio_short = tk.Radiobutton(frame_position, text="숏", variable=self.position_var, value="Short",
                                     command=self.handle_position_change,
                                     bg=self.bg_color, fg="white", selectcolor=self.bg_color,
                                     font=self.entry_font, activebackground=self.bg_color)
        self.radio_short.pack(side=tk.LEFT, padx=10)
        frame_position.grid(row=row, column=1, sticky='w', pady=5)
        
        row += 1
        # 실제 투자금
        self.box_label("실제 투자금 (달러)").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
        self.entry_capital = self.styled_entry("1000")
        self.entry_capital.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)
        self.entry_capital.bind("<KeyRelease>", lambda event: self.controller.update_capital(self.entry_capital.get()))
        
        row += 1
        # 환율
        self.box_label("적용 환율 (1 USD = 원)").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
        self.entry_exchange_rate = self.styled_entry("1450")
        self.entry_exchange_rate.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)
        self.entry_exchange_rate.bind("<KeyRelease>", lambda event: self.controller.update_exchange_rate(self.entry_exchange_rate.get()))
        
        # 결과 출력
        row += 1
        frame_profit_label = tk.Frame(self.container, bg=self.bg_color)
        tk.Label(frame_profit_label, text="레버리지 반영 수익률", bg=self.bg_color, fg="gray", font=self.label_font).pack(side=tk.LEFT)
        tk.Label(frame_profit_label, text="(수수료 0.05% 반영)", bg=self.bg_color, fg="#888888", font=("Malgun Gothic", 9)).pack(side=tk.LEFT, padx=(6,0))
        frame_profit_label.grid(row=row, column=0, columnspan=2, pady=(20, 5))
        
        row += 1
        self.result_percent_label = tk.Label(self.container, text="-", font=self.large_font, bg=self.bg_color, fg=self.accent_color)
        self.result_percent_label.grid(row=row, column=0, columnspan=2, pady=(0, 10))
        
        row += 1
        tk.Label(self.container, text="예상 누적 금액", bg=self.bg_color, fg="gray", font=self.label_font).grid(
            row=row, column=0, columnspan=2, pady=(10, 5))
        
        row += 1
        self.result_amount_label = tk.Label(self.container, text="-", font=self.large_font, bg=self.bg_color, fg="white")
        self.result_amount_label.grid(row=row, column=0, columnspan=2, pady=(0, 30))
        
        # 초기 포지션 색상 업데이트
        self.update_position_colors()
    
    def box_label(self, text):
        lbl = tk.Entry(self.container, bg=self.label_box_bg, fg=self.label_fg, font=self.label_font,
                       justify='center', relief="flat", bd=0,
                       highlightthickness=2, highlightbackground="#111111",
                       takefocus=0)  # 탭 포커스 제거
        lbl.insert(0, text)
        lbl.config(state='readonly')
        return lbl
    
    def styled_entry(self, default=""):
        e = tk.Entry(self.container, bg=self.entry_bg, fg=self.entry_fg, font=self.entry_font,
                     insertbackground='white', justify='center',
                     relief="flat", bd=0,
                     highlightthickness=2, highlightbackground="#888888")
        e.insert(0, default)
        return e
    
    def handle_leverage_scale(self, val):
        self.entry_leverage.delete(0, tk.END)
        self.entry_leverage.insert(0, str(int(float(val))))
        self.controller.update_leverage(int(float(val)))
    
    def handle_leverage_entry(self, event):
        try:
            val = int(self.entry_leverage.get())
            if 1 <= val <= 125:
                self.scale_leverage.set(val)
                self.controller.update_leverage(val)
        except:
            pass
    
    def handle_position_change(self):
        self.update_position_colors()
        self.controller.update_position(self.position_var.get())
    
    def update_position_colors(self):
        if self.position_var.get() == "Long":
            self.radio_long.config(fg=self.accent_color)
            self.radio_short.config(fg="white")
        else:
            self.radio_long.config(fg="white")
            self.radio_short.config(fg=self.accent_color)
    
    def update_results(self, leveraged_percent, actual_profit_usd, actual_profit_krw, has_error):
        if has_error:
            self.result_percent_label.config(text="입력을 확인하세요.", fg="red")
            self.result_amount_label.config(text="", fg="red")
        else:
            self.result_percent_label.config(text=f"{leveraged_percent:.2f}%", fg=self.accent_color)
            self.result_amount_label.config(
                text=f"${actual_profit_usd:,.2f} (₩{actual_profit_krw:,.0f})", fg="white")