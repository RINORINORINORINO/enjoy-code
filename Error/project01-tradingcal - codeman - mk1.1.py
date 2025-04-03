# 파이널 수정된 MVC 구조의 특정:
# ▪ 포지션: 랭이오 버튼 (Long/숏)으로 가능
# ▪ 레버리지: 슬라이더 + 수자 입력 가능
# ▪ 기본값: 진입가격/목표가격 = 0, 투자금 = 6000

import tkinter as tk

class TradingCalculatorModel:
    def __init__(self, fee_rate=0.0005):
        self.fee_rate = fee_rate

    def calculate(self, entry, target, leverage, capital, rate, position):
        profit_pct = ((target - entry) / entry * 100) if position == "Long" else ((entry - target) / entry * 100)
        adjusted_pct = profit_pct * leverage - (self.fee_rate * 2 * leverage * 100)
        usd_profit = capital * (adjusted_pct / 100)
        krw_profit = usd_profit * rate
        return adjusted_pct, usd_profit, krw_profit

class TradingCalculatorView:
    def __init__(self, root):
        self.root = root
        self.root.title("트레이딩 수익/손실 바로미터 - MVC")

        self.bg_color = "#1C1C1C"
        self.entry_bg = "#3A3A3C"
        self.label_box_bg = "#E6E6E6"
        self.label_fg = "#111111"
        self.entry_fg = "white"
        self.accent_color = "#FFA500"

        self.label_font = ("Malgun Gothic", 13, "bold")
        self.entry_font = ("Segoe UI", 13, "bold")
        self.large_font = ("Malgun Gothic", 18, "bold")

        self.root.configure(bg=self.bg_color)
        self.root.geometry("560x600")
        self.root.minsize(560, 600)
        self.root.resizable(True, True)

        self.fields = {}
        self.result_labels = {}
        self.position_var = tk.StringVar(value="Long")

        self.container = tk.Frame(self.root, bg=self.bg_color)
        self.container.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=2)

        self._build_ui()

    def _create_label_box(self, text):
        lbl = tk.Entry(self.container, bg=self.label_box_bg, fg=self.label_fg, font=self.label_font,
                       justify='center', relief="flat", bd=0,
                       highlightthickness=2, highlightbackground="#111111",
                       takefocus=0)
        lbl.insert(0, text)
        lbl.config(state='readonly')
        return lbl

    def _create_entry(self, default=""):
        e = tk.Entry(self.container, bg=self.entry_bg, fg=self.entry_fg, font=self.entry_font,
                     insertbackground='white', justify='center',
                     relief="flat", bd=0, highlightthickness=2, highlightbackground="#888888")
        e.insert(0, default)
        return e

    def _build_ui(self):
        field_order = [
            ("진입 가격", "0"),
            ("목표 가격", "0"),
            ("레버리지", "10"),
            ("포지션", "Long"),
            ("실제 투자금 (달러)", "6000"),
            ("적용 환율 (1 USD = 원)", "1450")
        ]

        for i, (label, default_val) in enumerate(field_order):
            self._create_label_box(label).grid(row=i, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)

            if label == "포지션":
                frame = tk.Frame(self.container, bg=self.bg_color)
                long_btn = tk.Radiobutton(frame, text="롱", variable=self.position_var, value="Long",
                                          bg=self.bg_color, fg=self.accent_color, selectcolor=self.bg_color,
                                          font=self.entry_font, activebackground=self.bg_color)
                short_btn = tk.Radiobutton(frame, text="숏", variable=self.position_var, value="Short",
                                           bg=self.bg_color, fg="white", selectcolor=self.bg_color,
                                           font=self.entry_font, activebackground=self.bg_color)
                long_btn.pack(side=tk.LEFT, padx=10)
                short_btn.pack(side=tk.LEFT, padx=10)
                frame.grid(row=i, column=1, sticky='w', pady=5)
                self.fields[label] = self.position_var

            elif label == "레버리지":
                frame = tk.Frame(self.container, bg=self.bg_color)
                frame.grid(row=i, column=1, sticky='ew', pady=5)
                frame.columnconfigure(0, weight=1)
                frame.columnconfigure(1, minsize=55)

                self.leverage_slider = tk.Scale(
                    frame, from_=1, to=125, orient=tk.HORIZONTAL, resolution=1,
                    showvalue=False, command=self._sync_entry_with_slider,
                    bg=self.bg_color, troughcolor="#555555", highlightthickness=0
                )
                self.leverage_slider.set(int(default_val))
                self.leverage_slider.grid(row=0, column=0, sticky="ew")

                entry = self._create_entry(default_val)
                entry.grid(row=0, column=1, padx=(10, 0), ipadx=4)
                entry.bind("<KeyRelease>", self._sync_slider_with_entry)
                self.fields[label] = entry

            else:
                entry = self._create_entry(default_val)
                entry.grid(row=i, column=1, sticky='ew', pady=5, ipady=6)
                self.fields[label] = entry

        row = len(field_order)
        profit_label_frame = tk.Frame(self.container, bg=self.bg_color)
        tk.Label(profit_label_frame, text="레버리지 반영 수익률", bg=self.bg_color, fg="gray", font=self.label_font).pack(side=tk.LEFT)
        tk.Label(profit_label_frame, text="(수수료 0.05% 반영)", bg=self.bg_color, fg="#888888", font=("Malgun Gothic", 9)).pack(side=tk.LEFT, padx=(6,0))
        profit_label_frame.grid(row=row, column=0, columnspan=2, pady=(20, 5))

        row += 1
        self.result_labels['percent'] = tk.Label(self.container, text="-", fg=self.accent_color,
                                                 bg=self.bg_color, font=self.large_font)
        self.result_labels['percent'].grid(row=row, column=0, columnspan=2, pady=(0, 10))

        row += 1
        tk.Label(self.container, text="예상 누적 금액", bg=self.bg_color, fg="gray", font=self.label_font).grid(
            row=row, column=0, columnspan=2, pady=(10, 5))
        row += 1
        self.result_labels['amount'] = tk.Label(self.container, text="-", fg="white",
                                                bg=self.bg_color, font=self.large_font)
        self.result_labels['amount'].grid(row=row, column=0, columnspan=2, pady=(0, 30))

    def _sync_entry_with_slider(self, val):
        # 슬라이더 값을 입력창에 반영
        self.fields["레버리지"].delete(0, tk.END)
        self.fields["레버리지"].insert(0, str(int(float(val))))

    def _sync_slider_with_entry(self, event=None):
        # 입력창 값을 슬라이더에 반영
        try:
            val = int(self.fields["레버리지"].get())
            if 1 <= val <= 125:
                self.leverage_slider.set(val)
        except ValueError:
            pass

    def get_inputs(self):
        try:
            entry = float(self.fields["진입 가격"].get())
            target = float(self.fields["목표 가격"].get())
            leverage = int(self.fields["레버리지"].get())
            position = self.position_var.get()
            capital = float(self.fields["실제 투자금 (달러)"].get())
            rate = float(self.fields["적용 환율 (1 USD = 원)"].get())
            return entry, target, leverage, capital, rate, position
        except ValueError:
            return None

    def update_result(self, pct, usd, krw):
        self.result_labels['percent'].config(text=f"{pct:.2f}% (수수료 포함)", fg=self.accent_color)
        self.result_labels['amount'].config(text=f"${usd:,.2f} (₩{krw:,.0f})", fg="white")

    def show_error(self):
        self.result_labels['percent'].config(text="입력을 확인하세요.", fg="red")
        self.result_labels['amount'].config(text="", fg="red")

class TradingCalculatorController:
    def __init__(self, root):
        self.model = TradingCalculatorModel()
        self.view = TradingCalculatorView(root)
        
        # 포지션 변경 이벤트 추가
        self.view.position_var.trace_add("write", lambda *args: self.on_input_change(None))
        
        # 모든 입력 필드에 이벤트 바인딩
        for label, field in self.view.fields.items():
            if isinstance(field, tk.Entry):
                field.bind("<KeyRelease>", self.on_input_change)

    def on_input_change(self, event):
        data = self.view.get_inputs()
        if data:
            pct, usd, krw = self.model.calculate(*data)
            self.view.update_result(pct, usd, krw)
        else:
            self.view.show_error()

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingCalculatorController(root)
    root.mainloop()