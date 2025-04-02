import tkinter as tk
from tkinter import ttk
import json
import os
from functools import partial

class TradingCalculator:
    def __init__(self, root):
        # 기본 설정값 정의
        self.default_settings = {
            "theme": "dark",
            "exchange_rate": 1450,
            "fee_rate": 0.0005,  # 0.05%
            "last_values": {
                "entry_price": "",
                "target_price": "",
                "leverage": 10,
                "position": "Long",
                "capital": 1000
            }
        }
        
        # 설정 로드
        self.settings = self.load_settings()
        
        # 스타일 설정
        self.setup_styles()
        
        # 메인 창 설정
        self.root = root
        self.root.title("트레이딩 수익/손실 계산기")
        self.root.configure(bg=self.colors["bg"])
        self.root.geometry("600x700")  # 높이 증가
        self.root.minsize(600, 700)  # 최소 크기 증가
        
        # 외부 프레임 (스크롤바 포함)
        outer_frame = ttk.Frame(root)
        outer_frame.pack(fill="both", expand=True)
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # 캔버스에 내용물 배치
        canvas = tk.Canvas(outer_frame, yscrollcommand=scrollbar.set, bg=self.colors["bg"], highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)
        
        # 메인 프레임은 캔버스 내부에 배치
        self.main_frame = tk.Frame(canvas, bg=self.colors["bg"])
        canvas_window = canvas.create_window((0, 0), window=self.main_frame, anchor="nw", width=canvas.winfo_reqwidth())
        
        # 프레임 크기가 변경될 때 캔버스 스크롤 영역 업데이트
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # 프레임 너비를 캔버스 너비와 일치시킴
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        self.main_frame.bind("<Configure>", configure_scroll_region)
        
        # 창 크기 변경 시 캔버스 크기 조정
        def on_canvas_resize(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_resize)
        
        # 그리드 설정
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        
        # UI 생성
        self.create_header()
        self.create_input_fields()
        self.create_results_section()
        self.create_footer()
        
        # 초기 계산
        self.calculate_profit()
        
        # 마우스 휠 스크롤 바인딩
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def setup_styles(self):
        # 색상 테마 설정
        if self.settings["theme"] == "dark":
            self.colors = {
                "bg": "#1A1A2E",
                "entry_bg": "#2D2D44",
                "entry_fg": "#FFFFFF",
                "label_bg": "#16213E",
                "label_fg": "#F0F0F0",
                "accent": "#4CB9E7",
                "accent_hover": "#3CA9D7",
                "positive": "#4CAF50",
                "negative": "#FF5252",
                "neutral": "#FFC107"
            }
        else:
            self.colors = {
                "bg": "#F8F9FA",
                "entry_bg": "#FFFFFF",
                "entry_fg": "#212121",
                "label_bg": "#E9ECEF",
                "label_fg": "#212121",
                "accent": "#0D6EFD",
                "accent_hover": "#0B5ED7",
                "positive": "#198754",
                "negative": "#DC3545",
                "neutral": "#FFC107"
            }
        
        # 폰트 설정
        self.fonts = {
            "title": ("Malgun Gothic", 22, "bold"),
            "label": ("Malgun Gothic", 13),
            "entry": ("Segoe UI", 13),
            "result_title": ("Malgun Gothic", 14),
            "result_value": ("Segoe UI", 22, "bold")
        }
        
        # ttk 스타일 설정
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 버튼 스타일
        self.style.configure("TButton", 
                             font=self.fonts["label"],
                             background=self.colors["accent"],
                             foreground=self.colors["label_fg"])
        
        # 라디오버튼 스타일
        self.style.configure("TRadiobutton", 
                             background=self.colors["bg"],
                             foreground=self.colors["label_fg"],
                             font=self.fonts["label"])
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=self.colors["bg"], pady=10)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        title = tk.Label(header_frame, 
                         text="트레이딩 수익/손실 계산기", 
                         font=self.fonts["title"],
                         bg=self.colors["bg"], 
                         fg=self.colors["accent"])
        title.pack()
        
        subtitle = tk.Label(header_frame, 
                            text="레버리지 및 수수료가 반영된 정확한 손익 계산", 
                            font=self.fonts["label"],
                            bg=self.colors["bg"], 
                            fg=self.colors["label_fg"])
        subtitle.pack(pady=(5, 0))
    
    def create_input_fields(self):
        row = 1
        
        # 입력 필드 생성 함수
        def create_field(label_text, default_value="", row_num=None, special_widget=None):
            label = tk.Label(self.main_frame, 
                             text=label_text, 
                             font=self.fonts["label"],
                             bg=self.colors["label_bg"], 
                             fg=self.colors["label_fg"],
                             relief="flat",
                             padx=15,
                             pady=10)
            label.grid(row=row_num, column=0, sticky='ew', padx=(20,15), pady=8)
            
            if special_widget:
                return special_widget(row_num)
            else:
                entry = tk.Entry(self.main_frame, 
                                font=self.fonts["entry"],
                                bg=self.colors["entry_bg"], 
                                fg=self.colors["entry_fg"],
                                insertbackground=self.colors["entry_fg"],
                                relief="flat",
                                justify='center',
                                highlightthickness=1,
                                highlightbackground=self.colors["accent"])
                entry.insert(0, default_value)
                entry.grid(row=row_num, column=1, sticky='ew', padx=(0,20), pady=8, ipady=8)
                entry.bind("<KeyRelease>", self.calculate_profit)
                return entry
        
        # 진입 가격
        self.entry_price = create_field("진입 가격", 
                                         self.settings["last_values"]["entry_price"], 
                                         row)
        row += 1
        
        # 목표 가격
        self.target_price = create_field("목표 가격", 
                                         self.settings["last_values"]["target_price"], 
                                         row)
        row += 1
        
        # 레버리지 슬라이더
        def create_leverage_widget(row_num):
            frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
            frame.grid(row=row_num, column=1, sticky='ew', padx=(0,20), pady=8)
            
            self.leverage_scale = ttk.Scale(frame, 
                                         from_=1, to=125, 
                                         orient=tk.HORIZONTAL,
                                         command=self.sync_entry_with_slider)
            self.leverage_scale.set(self.settings["last_values"]["leverage"])
            self.leverage_scale.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10))
            
            self.leverage_entry = tk.Entry(frame, 
                                        width=5,
                                        font=self.fonts["entry"],
                                        bg=self.colors["entry_bg"], 
                                        fg=self.colors["entry_fg"],
                                        justify='center',
                                        relief="flat",
                                        highlightthickness=1,
                                        highlightbackground=self.colors["accent"])
            self.leverage_entry.insert(0, str(self.settings["last_values"]["leverage"]))
            self.leverage_entry.pack(side=tk.LEFT, padx=5, ipady=6)
            self.leverage_entry.bind("<KeyRelease>", self.sync_slider_with_entry)
            
            return frame
        
        self.leverage_frame = create_field("레버리지 (1~125)", 
                                         "", 
                                         row, 
                                         create_leverage_widget)
        row += 1
        
        # 포지션 라디오 버튼
        def create_position_widget(row_num):
            frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
            frame.grid(row=row_num, column=1, sticky='ew', padx=(0,20), pady=8)
            
            self.position_var = tk.StringVar(value=self.settings["last_values"]["position"])
            
            self.radio_long = ttk.Radiobutton(frame, 
                                         text="롱 (Long)", 
                                         variable=self.position_var, 
                                         value="Long",
                                         command=self.update_position_and_calculate)
            self.radio_long.pack(side=tk.LEFT, padx=(0, 20))
            
            self.radio_short = ttk.Radiobutton(frame, 
                                          text="숏 (Short)", 
                                          variable=self.position_var, 
                                          value="Short",
                                          command=self.update_position_and_calculate)
            self.radio_short.pack(side=tk.LEFT)
            
            return frame
        
        self.position_frame = create_field("포지션 선택", 
                                         "", 
                                         row, 
                                         create_position_widget)
        row += 1
        
        # 투자금
        self.capital = create_field("실제 투자금 (달러)", 
                                         str(self.settings["last_values"]["capital"]), 
                                         row)
        row += 1
        
        # 환율
        self.exchange_rate = create_field("적용 환율 (1 USD = 원)", 
                                         str(self.settings["exchange_rate"]), 
                                         row)
        row += 1
        
        # 수수료율
        rate_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        rate_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=20, pady=(15, 0))
        
        fee_label = tk.Label(rate_frame, 
                            text=f"적용 수수료율: {self.settings['fee_rate']*100}%", 
                            font=self.fonts["label"],
                            bg=self.colors["bg"], 
                            fg=self.colors["label_fg"])
        fee_label.pack(side=tk.LEFT)
        
        # 수수료 조정 버튼
        fee_btn = ttk.Button(rate_frame, 
                             text="수수료 조정", 
                             command=self.show_fee_dialog)
        fee_btn.pack(side=tk.RIGHT)
    
    def create_results_section(self):
        result_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        result_frame.grid(row=10, column=0, columnspan=2, sticky='ew', padx=20, pady=(20, 0))
        
        # 구분선
        separator = ttk.Separator(result_frame, orient='horizontal')
        separator.pack(fill='x', pady=10)
        
        # 수익률 결과
        tk.Label(result_frame, 
                text="예상 수익률", 
                font=self.fonts["result_title"],
                bg=self.colors["bg"], 
                fg=self.colors["label_fg"]).pack(pady=(10, 5))
        
        self.result_percent_label = tk.Label(result_frame, 
                                            text="0.00%", 
                                            font=self.fonts["result_value"],
                                            bg=self.colors["bg"], 
                                            fg=self.colors["accent"])
        self.result_percent_label.pack(pady=(0, 10))
        
        # 금액 결과
        tk.Label(result_frame, 
                text="예상 수익금액", 
                font=self.fonts["result_title"],
                bg=self.colors["bg"], 
                fg=self.colors["label_fg"]).pack(pady=(5, 5))
        
        self.result_amount_label = tk.Label(result_frame, 
                                           text="$0.00 (₩0)", 
                                           font=self.fonts["result_value"],
                                           bg=self.colors["bg"], 
                                           fg=self.colors["label_fg"])
        self.result_amount_label.pack(pady=(0, 10))
        
        # 초기 투자금 + 수익 결과
        tk.Label(result_frame, 
                text="예상 최종 자산", 
                font=self.fonts["result_title"],
                bg=self.colors["bg"], 
                fg=self.colors["label_fg"]).pack(pady=(5, 5))
        
        self.result_total_label = tk.Label(result_frame, 
                                          text="$0.00 (₩0)", 
                                          font=self.fonts["result_value"],
                                          bg=self.colors["bg"], 
                                          fg=self.colors["accent"])
        self.result_total_label.pack(pady=(0, 10))
    
    def create_footer(self):
        footer_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        footer_frame.grid(row=11, column=0, columnspan=2, sticky='ew', padx=20, pady=(15, 30))
        
        # 저장 버튼
        save_btn = ttk.Button(footer_frame, 
                             text="현재 설정 저장", 
                             command=self.save_current_settings)
        save_btn.pack(side=tk.LEFT)
        
        # 테마 전환 버튼
        theme_btn = ttk.Button(footer_frame, 
                              text="테마 전환", 
                              command=self.toggle_theme)
        theme_btn.pack(side=tk.RIGHT)
    
    def calculate_profit(self, *args):
        try:
            # 입력값 가져오기
            entry_price = float(self.entry_price.get())
            target_price = float(self.target_price.get())
            leverage = int(self.leverage_entry.get())
            capital_usd = float(self.capital.get())
            exchange_rate = float(self.exchange_rate.get())
            position = self.position_var.get()
            fee_rate = self.settings["fee_rate"]
            
            # 유효성 검사
            if entry_price <= 0 or target_price <= 0 or leverage <= 0 or capital_usd <= 0 or exchange_rate <= 0:
                raise ValueError("값은 0보다 커야 합니다")
                
            # 기본 수익률 계산
            if position == 'Long':
                profit_percent = ((target_price - entry_price) / entry_price) * 100
            else:  # Short
                profit_percent = ((entry_price - target_price) / entry_price) * 100
            
            # 수수료 반영한 레버리지 수익률
            # 진입 및 청산 시 두 번의 수수료 적용
            fee_impact = fee_rate * 2 * 100  # 퍼센트로 변환
            leveraged_percent = (profit_percent * leverage) - (fee_impact * leverage)
            
            # 실제 금액 계산
            actual_profit_usd = capital_usd * (leveraged_percent / 100)
            actual_profit_krw = actual_profit_usd * exchange_rate
            
            # 최종 자산 계산
            final_capital_usd = capital_usd + actual_profit_usd
            final_capital_krw = final_capital_usd * exchange_rate
            
            # 색상 결정
            if leveraged_percent > 0:
                percent_color = self.colors["positive"]
            elif leveraged_percent < 0:
                percent_color = self.colors["negative"]
            else:
                percent_color = self.colors["neutral"]
            
            # 결과 표시
            self.result_percent_label.config(text=f"{leveraged_percent:.2f}%", fg=percent_color)
            self.result_amount_label.config(
                text=f"${actual_profit_usd:,.2f} (₩{actual_profit_krw:,.0f})", 
                fg=self.colors["label_fg"])
            self.result_total_label.config(
                text=f"${final_capital_usd:,.2f} (₩{final_capital_krw:,.0f})", 
                fg=percent_color)
            
            # 입력값 저장
            self.settings["last_values"]["entry_price"] = self.entry_price.get()
            self.settings["last_values"]["target_price"] = self.target_price.get()
            self.settings["last_values"]["leverage"] = leverage
            self.settings["last_values"]["position"] = position
            self.settings["last_values"]["capital"] = capital_usd
            self.settings["exchange_rate"] = exchange_rate
            
        except ValueError as e:
            if str(e) == "값은 0보다 커야 합니다":
                message = "모든 값은 0보다 커야 합니다"
            else:
                message = "입력값을 확인하세요"
                
            self.result_percent_label.config(text=message, fg=self.colors["negative"])
            self.result_amount_label.config(text="-", fg=self.colors["label_fg"])
            self.result_total_label.config(text="-", fg=self.colors["label_fg"])
    
    def sync_slider_with_entry(self, *args):
        try:
            val = int(self.leverage_entry.get())
            if 1 <= val <= 125:
                self.leverage_scale.set(val)
                self.calculate_profit()
            elif val > 125:
                self.leverage_entry.delete(0, tk.END)
                self.leverage_entry.insert(0, "125")
                self.leverage_scale.set(125)
                self.calculate_profit()
            elif val < 1:
                self.leverage_entry.delete(0, tk.END)
                self.leverage_entry.insert(0, "1")
                self.leverage_scale.set(1)
                self.calculate_profit()
        except ValueError:
            pass
    
    def sync_entry_with_slider(self, val):
        self.leverage_entry.delete(0, tk.END)
        self.leverage_entry.insert(0, str(int(float(val))))
        self.calculate_profit()
    
    def update_position_and_calculate(self):
        self.calculate_profit()
    
    def toggle_theme(self):
        if self.settings["theme"] == "dark":
            self.settings["theme"] = "light"
        else:
            self.settings["theme"] = "dark"
        
        # 설정 저장
        self.save_settings()
        
        # 사용자에게 알림
        tk.messagebox.showinfo("테마 변경", "테마가 변경되었습니다. 변경 사항을 적용하려면 프로그램을 재시작하세요.")
    
    def show_fee_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("수수료 설정")
        dialog.configure(bg=self.colors["bg"])
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, 
                text="수수료율 설정 (퍼센트)", 
                font=self.fonts["label"],
                bg=self.colors["bg"], 
                fg=self.colors["label_fg"]).pack(pady=(20, 10))
        
        fee_entry = tk.Entry(dialog, 
                           font=self.fonts["entry"],
                           width=10,
                           justify='center',
                           bg=self.colors["entry_bg"], 
                           fg=self.colors["entry_fg"])
        fee_entry.insert(0, str(self.settings["fee_rate"] * 100))
        fee_entry.pack(pady=10)
        
        def save_fee():
            try:
                new_fee = float(fee_entry.get()) / 100
                if 0 <= new_fee <= 1:
                    self.settings["fee_rate"] = new_fee
                    self.save_settings()
                    self.calculate_profit()
                    dialog.destroy()
                else:
                    tk.messagebox.showerror("오류", "수수료율은 0%에서 100% 사이여야 합니다")
            except ValueError:
                tk.messagebox.showerror("오류", "유효한 숫자를 입력하세요")
        
        ttk.Button(dialog, 
                  text="저장", 
                  command=save_fee).pack(pady=10)
    
    def save_current_settings(self):
        try:
            # 현재 입력값으로 설정 업데이트
            self.settings["last_values"]["entry_price"] = self.entry_price.get()
            self.settings["last_values"]["target_price"] = self.target_price.get()
            self.settings["last_values"]["leverage"] = int(self.leverage_entry.get())
            self.settings["last_values"]["position"] = self.position_var.get()
            self.settings["last_values"]["capital"] = float(self.capital.get())
            self.settings["exchange_rate"] = float(self.exchange_rate.get())
            
            # 설정 저장
            self.save_settings()
            
            # 성공 메시지
            tk.messagebox.showinfo("설정 저장", "현재 설정이 성공적으로 저장되었습니다.")
        except:
            tk.messagebox.showerror("오류", "설정 저장 중 오류가 발생했습니다.")
    
    def load_settings(self):
        try:
            if os.path.exists('trading_calculator_settings.json'):
                with open('trading_calculator_settings.json', 'r') as f:
                    settings = json.load(f)
                # 기존 설정에 누락된 항목이 있으면 기본값으로 추가
                for key, value in self.default_settings.items():
                    if key not in settings:
                        settings[key] = value
                    # 중첩된 딕셔너리 처리
                    elif isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            if key not in settings or subkey not in settings[key]:
                                if key not in settings:
                                    settings[key] = {}
                                settings[key][subkey] = subvalue
                return settings
            else:
                return self.default_settings
        except:
            return self.default_settings
    
    def save_settings(self):
        try:
            with open('trading_calculator_settings.json', 'w') as f:
                json.dump(self.settings, f)
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingCalculator(root)
    root.mainloop()