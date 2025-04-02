import tkinter as tk

def calculate_profit(*args):
    try:
        entry_price = float(entry_entry_price.get())
        target_price = float(entry_target_price.get())
        leverage = int(entry_leverage.get())
        capital_usd = float(entry_capital.get())
        exchange_rate = float(entry_exchange_rate.get())
        position = position_var.get()

        # 거래소 수수료 (0.05%)
        fee_rate = 0.0005

        # 기본 수익률 계산
        profit_percent = ((target_price - entry_price) / entry_price * 100
                          if position == 'Long'
                          else (entry_price - target_price) / entry_price * 100)

        # 수수료 반영한 레버리지 수익률
        leveraged_percent = (profit_percent * leverage) - (leverage * fee_rate * 100)

        actual_profit_usd = capital_usd * (leveraged_percent / 100)
        actual_profit_krw = actual_profit_usd * exchange_rate

        result_percent_label.config(text=f"{leveraged_percent:.2f}%", fg=accent_color)
        result_amount_label.config(
            text=f"${actual_profit_usd:,.2f} (₩{actual_profit_krw:,.0f})", fg="white")

    except ValueError:
        result_percent_label.config(text="입력을 확인하세요.", fg="red")
        result_amount_label.config(text="", fg="red")

def sync_slider_with_entry(*args):
    try:
        val = int(entry_leverage.get())
        if 1 <= val <= 125:
            scale_leverage.set(val)
            calculate_profit()
    except:
        pass

def sync_entry_with_slider(val):
    entry_leverage.delete(0, tk.END)
    entry_leverage.insert(0, str(int(float(val))))
    calculate_profit()

def update_position_colors():
    if position_var.get() == "Long":
        radio_long.config(fg=accent_color)
        radio_short.config(fg="white")
    else:
        radio_long.config(fg="white")
        radio_short.config(fg=accent_color)
    calculate_profit()

# 스타일
bg_color = "#1C1C1C"
entry_bg = "#3A3A3C"
entry_fg = "white"
label_box_bg = "#E6E6E6"
label_fg = "#111111"
accent_color = "#FFA500"
label_font = ("Malgun Gothic", 13, "bold")
large_font = ("Malgun Gothic", 18, "bold")
entry_font = ("Segoe UI", 13, "bold")

root = tk.Tk()
root.title("트레이딩 수익/손실 바로미터")
root.configure(bg=bg_color)
root.geometry("560x560")
root.minsize(560, 560)
root.resizable(True, True)

container = tk.Frame(root, bg=bg_color)
container.pack(fill="both", expand=True, padx=30, pady=30)

container.columnconfigure(0, weight=1)
container.columnconfigure(1, weight=2)

def box_label(text):
    lbl = tk.Entry(container, bg=label_box_bg, fg=label_fg, font=label_font,
                   justify='center', relief="flat", bd=0,
                   highlightthickness=2, highlightbackground="#111111",
                   takefocus=0)  # 탭 포커스 제거
    lbl.insert(0, text)
    lbl.config(state='readonly')
    return lbl

def styled_entry(default=""):
    e = tk.Entry(container, bg=entry_bg, fg=entry_fg, font=entry_font,
                 insertbackground='white', justify='center',
                 relief="flat", bd=0,
                 highlightthickness=2, highlightbackground="#888888")
    e.insert(0, default)
    e.bind("<KeyRelease>", calculate_profit)
    return e

# UI 구성
row = 0
box_label("진입 가격").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
entry_entry_price = styled_entry()
entry_entry_price.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)

row += 1
box_label("목표 가격").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
entry_target_price = styled_entry()
entry_target_price.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)

row += 1
box_label("레버리지 (1~125)").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
frame_leverage = tk.Frame(container, bg=bg_color)
scale_leverage = tk.Scale(frame_leverage, from_=1, to=125, orient=tk.HORIZONTAL,
                          resolution=1, showvalue=False, command=sync_entry_with_slider,
                          bg=bg_color, troughcolor="#555555", highlightthickness=0)
scale_leverage.set(10)
scale_leverage.pack(side=tk.LEFT, fill='x', expand=True)
entry_leverage = tk.Entry(frame_leverage, width=5, bg=entry_bg, fg=entry_fg,
                          font=entry_font, justify='center', insertbackground='white',
                          relief="flat", bd=0, highlightthickness=2, highlightbackground="#888888")
entry_leverage.insert(0, "10")
entry_leverage.pack(side=tk.LEFT, padx=5)
entry_leverage.bind("<KeyRelease>", sync_slider_with_entry)
frame_leverage.grid(row=row, column=1, sticky='ew', pady=5)

row += 1
box_label("포지션").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
frame_position = tk.Frame(container, bg=bg_color)
position_var = tk.StringVar(value="Long")
radio_long = tk.Radiobutton(frame_position, text="롱", variable=position_var, value="Long",
                            command=update_position_colors,
                            bg=bg_color, fg=accent_color, selectcolor=bg_color,
                            font=entry_font, activebackground=bg_color)
radio_long.pack(side=tk.LEFT, padx=10)
radio_short = tk.Radiobutton(frame_position, text="숏", variable=position_var, value="Short",
                             command=update_position_colors,
                             bg=bg_color, fg="white", selectcolor=bg_color,
                             font=entry_font, activebackground=bg_color)
radio_short.pack(side=tk.LEFT, padx=10)
frame_position.grid(row=row, column=1, sticky='w', pady=5)

row += 1
box_label("실제 투자금 (달러)").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
entry_capital = styled_entry("1000")
entry_capital.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)

row += 1
box_label("적용 환율 (1 USD = 원)").grid(row=row, column=0, sticky='ew', padx=(0,10), pady=5, ipady=6)
entry_exchange_rate = styled_entry("1450")
entry_exchange_rate.grid(row=row, column=1, sticky='ew', pady=5, ipady=6)

# 결과 출력
row += 1
frame_profit_label = tk.Frame(container, bg=bg_color)
tk.Label(frame_profit_label, text="레버리지 반영 수익률", bg=bg_color, fg="gray", font=label_font).pack(side=tk.LEFT)
tk.Label(frame_profit_label, text="(수수료 0.05% 반영)", bg=bg_color, fg="#888888", font=("Malgun Gothic", 9)).pack(side=tk.LEFT, padx=(6,0))
frame_profit_label.grid(row=row, column=0, columnspan=2, pady=(20, 5))
row += 1
result_percent_label = tk.Label(container, text="-", font=large_font, bg=bg_color, fg=accent_color)
result_percent_label.grid(row=row, column=0, columnspan=2, pady=(0, 10))

row += 1
tk.Label(container, text="예상 누적 금액", bg=bg_color, fg="gray", font=label_font).grid(
    row=row, column=0, columnspan=2, pady=(10, 5))
row += 1
result_amount_label = tk.Label(container, text="-", font=large_font, bg=bg_color, fg="white")
result_amount_label.grid(row=row, column=0, columnspan=2, pady=(0, 30))

update_position_colors()

root.mainloop()
