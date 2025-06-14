import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
import os

# 프리셋 데이터
presets = {
    "sr20det": {
        "bore": 86.0, "stroke": 86.0, "cylinders": 4, "compression_ratio": 8.5, "redline": 7500,
        "engine_type": "turbo", "forced_type": "twin-scroll", "boost": 1.0,
        "layout": "inline", "fuel_type": "gasoline", "use_vvl": "no", "vvl_rpm": 0,
        "vvl_profile": "mild", "ambient": "normal"
    },
    "b16a": {
        "bore": 81.0, "stroke": 77.4, "cylinders": 4, "compression_ratio": 10.4, "redline": 8200,
        "engine_type": "na", "forced_type": "na", "boost": 0,
        "layout": "inline", "fuel_type": "gasoline", "use_vvl": "yes", "vvl_rpm": 5500,
        "vvl_profile": "aggressive", "ambient": "normal"
    }
}

class DynoSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Engine Simulator 2.0")
        self.root.geometry("1280x720")

        self.inputs = {}
        self.canvas = None
        self.figure = plt.Figure(figsize=(7, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.build_gui()
        
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        for key, value in data.items():
                            if key in self.inputs:
                                widget = self.inputs[key]
                                if isinstance(widget, ttk.Combobox):
                                    widget.set(value)
                                else:
                                    widget.delete(0, tk.END)
                                    widget.insert(0, str(value))
                    except json.JSONDecodeError as e:
                        messagebox.showerror("파일 형식 오류", f"유효한 .eng 파일이 아닙니다.\n{e}")


    

    def build_gui(self):
        left_frame = ttk.Frame(self.root, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 그래프를 넣을 캔버스
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        fields = [
            ("bore", "Bore (mm)"),
            ("stroke", "Stroke (mm)"),
            ("cylinders", "Cylinders"),
            ("compression_ratio", "Compression Ratio"),
            ("redline", "Redline RPM"),
            ("engine_type", "Engine Type (na/turbo/supercharger/...)"),
            ("forced_type", "Forced Induction Type"),
            ("boost", "Boost (bar)"),
            ("layout", "Layout (inline/v/boxer)"),
            ("fuel_type", "Fuel Type"),
            ("ambient", "Ambient (normal/cold/hot)"),
            ("use_vvl", "Use VVL (yes/no)"),
            ("vvl_rpm", "VVL RPM"),
            ("vvl_profile", "VVL Profile (mild/aggressive)"),
        ]

        combo_options = {
            "engine_type": ["na", "turbo", "supercharger", "twin-turbo", "twincharged"],
            "forced_type": ["na", "single", "twin-scroll", "variable-geometry", "roots", "centrifugal", "twin-screw"],
            "layout": ["inline", "v", "boxer"],
            "fuel_type": ["gasoline", "high-octane", "diesel", "e85", "methanol", "lpg"],
            "ambient": ["normal", "cold", "hot"],
            "use_vvl": ["yes", "no"],
            "vvl_profile": ["mild", "aggressive"]
        }

        for key, label in fields:
            ttk.Label(left_frame, text=label).pack()
            if key in combo_options:
                cb = ttk.Combobox(left_frame, values=combo_options[key], state="readonly")
                cb.pack(fill=tk.X)
                self.inputs[key] = cb
            else:
                entry = ttk.Entry(left_frame)
                entry.pack(fill=tk.X)
                self.inputs[key] = entry

        ttk.Button(left_frame, text="Simulate", command=self.simulate).pack(fill=tk.X, pady=5)
        ttk.Button(left_frame, text="Load Preset", command=self.load_preset).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="Save Preset", command=self.save_preset).pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="Help", command=self.show_help).pack(fill=tk.X, pady=2)

    def load_preset(self):
        # 프리셋 불러오기
        file_path = askopenfilename(filetypes=[("Engine Preset Files", "*.eng"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    preset_data = json.load(f)
                for key, value in preset_data.items():
                    if key in self.inputs:
                        widget = self.inputs[key]
                        if isinstance(widget, ttk.Combobox):
                            widget.set(value)
                        else:
                            widget.delete(0, tk.END)
                            widget.insert(0, str(value))
                messagebox.showinfo("Preset Loaded", f"프리셋 파일이 성공적으로 불러와졌습니다.")
            except Exception as e:
                messagebox.showerror("불러오기 실패", f"파일을 불러오는 중 오류가 발생했습니다:\n{e}")

    def save_preset(self):
        # 프리셋 저장
        config = {}
        for key, widget in self.inputs.items():
            val = widget.get()
            config[key] = val.lower() if isinstance(widget, ttk.Combobox) else float(val) if key in ["bore", "stroke", "compression_ratio", "boost", "redline", "vvl_rpm"] else int(val) if key == "cylinders" else val

        file_path = asksaveasfilename(defaultextension=".eng", filetypes=[("Engine Preset Files", "*.eng"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=4)
                messagebox.showinfo("Preset Saved", "프리셋이 성공적으로 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("저장 실패", f"프리셋을 저장하는 중 오류가 발생했습니다:\n{e}")

    def show_help(self):
        help_text = (
            "💡 엔진 시뮬레이터 도움말\n\n"
            "🔸 Bore & Stroke (mm): 실린더 직경과 스트로크 길이\n"
            "🔸 Cylinders: 실린더 개수\n"
            "🔸 Compression Ratio: 압축비\n"
            "🔸 Redline RPM: 최대 회전수\n"
            "🔸 Engine Type: na / turbo / supercharger / twin-turbo / twincharged\n"
            "🔸 Fuel Type: gasoline / high-octane / diesel / e85 / methanol / lpg\n"
            "🔸 Layout: inline / v / boxer\n"
            "🔸 Ambient: 주행 환경\n"
            "🔸 VVL: 가변 밸브 리프트\n"
            "🔸 VVL Profile: mild (완만), aggressive (고출력)\n"
            "🔸 VVL RPM: 전환 시점\n"
            "🔸 Forced Induction Type: 여러 과급기 종류 선택\n"
            "🔸 Boost Pressure: 과급 압력 (bar 단위)\n\n"
            "⚙️ 'Simulate' 버튼으로 시뮬레이션 실행\n📋 'Load Preset'으로 예시 엔진 불러오기"
        )
        messagebox.showinfo("도움말", help_text)

    def simulate(self):
        try:
            # 입력값 수집 및 전처리
            config = {}
            for key, widget in self.inputs.items():
                val = widget.get()
                if key in ["bore", "stroke", "compression_ratio", "boost", "redline", "vvl_rpm"]:
                    config[key] = float(val)
                elif key == "cylinders":
                    config[key] = int(val)
                else:
                    config[key] = val.lower()

            config["vvl_enabled"] = (config["use_vvl"] == "yes")
            config["ambient_condition"] = config["ambient"]

            # 단위 변환 및 변수 초기화
            bore = config["bore"] / 1000
            stroke = config["stroke"] / 1000
            cylinders = config["cylinders"]
            compression = config["compression_ratio"]
            redline = config["redline"]
            engine_type = config["engine_type"]
            layout = config["layout"]
            fuel_type = config["fuel_type"]
            vvl_enabled = config["vvl_enabled"]
            vvl_rpm = config["vvl_rpm"]
            vvl_profile = config["vvl_profile"]
            ambient_condition = config["ambient_condition"]
            forced_type = config["forced_type"]
            boost = config["boost"]

            # 연료 및 온도 계수
            fuel_hp_modifier = {
                "gasoline": 1.00, "high-octane": 1.05, "diesel": 0.85,
                "e85": 1.10, "methanol": 1.12, "lpg": 0.92
            }.get(fuel_type, 1.0)

            temp_power_modifier = 1.0
            if ambient_condition == "cold":
                temp_power_modifier = 0.92
            elif ambient_condition == "hot":
                temp_power_modifier = 0.95

            # 기본 계산
            displacement = (np.pi / 4) * (bore ** 2) * stroke * cylinders * 1000
            layout_hp_modifier = {"inline": 1.0, "v": 1.05, "boxer": 0.97}.get(layout, 1.0)
            layout_torque_rpm_modifier = {"inline": 1.0, "v": 1.1, "boxer": 0.85}.get(layout, 1.0)
            na_base_hp = displacement * compression * 10 * layout_hp_modifier * fuel_hp_modifier * temp_power_modifier

            # 과급 부스트 반영
            boost_multiplier = 1.0
            if engine_type == 'turbo':
                boost_multiplier = 1 + boost * (0.95 if forced_type == 'twin-scroll' else 1.0)
            elif engine_type == 'supercharger':
                boost_multiplier = 1 + boost * (0.85 if forced_type == 'roots' else 0.9)
            elif engine_type == 'twin-turbo':
                boost_multiplier = 1 + boost * 0.97
            elif engine_type == 'twincharged':
                boost_multiplier = 1 + boost * 1.05

            max_hp_base = na_base_hp * boost_multiplier
            rpm = np.linspace(1000, redline, 1000)

            # VVL 반영
            vvl_hp_gain = np.ones_like(rpm)
            vvl_torque_gain = np.ones_like(rpm)
            if vvl_enabled:
                for i in range(len(rpm)):
                    if rpm[i] > vvl_rpm:
                        scale = min((rpm[i] - vvl_rpm) / 300, 1.0)
                        if vvl_profile == "mild":
                            vvl_hp_gain[i] += scale * 0.05
                            vvl_torque_gain[i] += scale * 0.05
                        elif vvl_profile == "aggressive":
                            vvl_hp_gain[i] += scale * 0.10
                            vvl_torque_gain[i] += scale * 0.08

            # 토크 및 출력 계산
            peak_hp_rpm = int(redline * 0.85)
            peak_torque_rpm = int(redline * 0.65 * layout_torque_rpm_modifier)
            max_torque = max_hp_base * 7127 / peak_hp_rpm

            sigma = (redline - 1000) / 3.5
            torque = max_torque * np.exp(-((rpm - peak_torque_rpm) ** 2) / (2 * sigma ** 2)) * vvl_torque_gain
            hp = torque * rpm / 7127 * vvl_hp_gain

            # 최고 출력 및 토크
            max_hp_val = np.max(hp)
            max_hp_rpm_actual = rpm[np.argmax(hp)]
            max_torque_val = np.max(torque)
            max_torque_rpm_actual = rpm[np.argmax(torque)]

            # 그래프 초기화 및 출력
            self.ax.clear()
            self.ax.plot(rpm, hp, label="Horsepower (HP)", color="red")
            self.ax.plot(rpm, torque, label="Torque (Nm)", color="blue")
            self.ax.axvline(max_hp_rpm_actual, linestyle='--', color='red', alpha=0.5)
            self.ax.axvline(max_torque_rpm_actual, linestyle='--', color='blue', alpha=0.5)
            self.ax.axvline(redline, linestyle=':', color='black', alpha=0.5)
            if vvl_enabled:
                self.ax.axvline(vvl_rpm, linestyle='--', color='green', alpha=0.4)
                self.ax.text(vvl_rpm, max_hp_val * 0.6, f"VVL\nActive\n({vvl_profile})", color='green', fontsize=8, ha='center')
            self.ax.text(max_hp_rpm_actual, max_hp_val + 10, f"{int(max_hp_val)} HP @ {int(max_hp_rpm_actual)} RPM",
                         color='red', ha='center', fontsize=9, fontweight='bold')
            self.ax.text(max_torque_rpm_actual, max_torque_val + 10, f"{int(max_torque_val)} Nm @ {int(max_torque_rpm_actual)} RPM",
                         color='blue', ha='center', fontsize=9, fontweight='bold')
            self.ax.set_title(f"Engine Output Curve ({layout.capitalize()} {engine_type.capitalize()}, Fuel: {fuel_type}, VVL: {'On' if vvl_enabled else 'Off'}, Ambient: {ambient_condition})")
            self.ax.set_xlabel("RPM")
            self.ax.set_ylabel("Horsepower (HP) / Torque (Nm)")
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("오류 발생", f"입력값이 잘못되었거나 계산 중 문제가 발생했습니다.\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DynoSimulatorApp(root)
    root.mainloop()
