import numpy as np
import matplotlib.pyplot as plt

# 도움말 표시 함수
def show_help():
    print("\n=== 🛠 Engine Simulator Help ===")
    print("이 시뮬레이터는 입력한 엔진 파라미터를 바탕으로 출력 곡선과 점화 간격을 시뮬레이션합니다.")
    print("\n입력 항목 안내:")
    print("1. Bore (mm): 실린더의 직경입니다. 예: 86")
    print("2. Stroke (mm): 피스톤의 왕복 거리입니다. 예: 86")
    print("3. Number of Cylinders: 실린더 개수입니다. 예: 4, 6, 8")
    print("4. Compression Ratio: 압축비입니다. 예: 10.5")
    print("5. Redline RPM: 최대 회전수입니다. 예: 7500")
    print("6. Engine Type:")
    print("   - NA: 자연흡기")
    print("   - Turbo: 터보차저")
    print("   - Supercharger: 슈퍼차저")
    print("   - Twin-Turbo: 트윈터보")
    print("   - Twincharged: 터보 + 슈퍼차저")
    print("7. Engine Layout:")
    print("   - inline: 직렬")
    print("   - v: V형")
    print("   - boxer: 수평대향")
    print("8. Fuel Type:")
    print("   - gasoline / high-octane / diesel / e85 / methanol / lpg")
    print("9. Use VVL? (yes / no): VVL (가변 밸브 리프트) 사용 여부")
    print("10. Ambient Condition: 주행 환경")
    print("   - normal / cold / hot")
    print("※ 과급기 선택 시 추가 입력 항목이 있습니다.")
    input("\n계속하려면 엔터를 누르세요...")
    print()

# 과급기 옵션 표시 함수
def show_forced_induction_options(engine_type):
    print("\n사용 가능한 과급기 유형:")
    if engine_type == "turbo":
        print(" - single (일반 싱글 터보)")
        print(" - twin-scroll (트윈스크롤 터보)")
        print(" - variable-geometry (가변 터빈 터보)")
    elif engine_type == "supercharger":
        print(" - roots (루츠형 슈퍼차저)")
        print(" - centrifugal (원심형 슈퍼차저)")
        print(" - twin-screw (트윈스크류 슈퍼차저)")

# 프리셋
presets = {
    "sr20det": {
        "bore": 86.0, "stroke": 86.0, "cylinders": 4, "compression": 8.5, "redline": 7500,
        "engine_type": "turbo", "forced_type": "twin-scroll", "boost": 1.0,
        "layout": "inline", "fuel_type": "gasoline", "vvl_enabled": False, "vvl_rpm": 0,
        "vvl_profile": None, "ambient_condition": "normal"
    },
    "b16a": {
        "bore": 81.0, "stroke": 77.4, "cylinders": 4, "compression": 10.4, "redline": 8200,
        "engine_type": "na", "forced_type": "na", "boost": 0,
        "layout": "inline", "fuel_type": "high-octane", "vvl_enabled": True, "vvl_rpm": 5500,
        "vvl_profile": "aggressive", "ambient_condition": "normal"
    },
    "c32b": {
        "bore": 90.0, "stroke": 78, "cylinders": 6, "compression": 10.2, "redline": 8200,
        "engine_type": "na", "forced_type": "na", "boost": 0,
        "layout": "v", "fuel_type": "high-octane", "vvl_enabled": True, "vvl_rpm": 5500,
        "vvl_profile": "aggressive", "ambient_condition": "normal"
    }
}

initial = input("입력을 시작하려면 엔터, 도움말은 'help', 예시는 'example', 프리셋 불러오기는 'load preset': ").strip().lower()
config = {}

if initial == "help":
    show_help()
elif initial == "example":
    config = {
        "bore": 86.0, "stroke": 86.0, "cylinders": 4, "compression": 10.5, "redline": 7500,
        "engine_type": "na", "layout": "inline", "fuel_type": "gasoline",
        "vvl_enabled": True, "vvl_rpm": 5200, "vvl_profile": "mild", "ambient_condition": "normal",
        "forced_type": None, "boost": 0
    }
elif initial == "load preset":
    print("사용 가능한 프리셋:", ", ".join(presets.keys()))
    key = input("불러올 프리셋 이름 입력: ").strip().lower()
    if key in presets:
        config = presets[key]
    else:
        print("프리셋을 찾을 수 없습니다. 기본 입력을 진행합니다.")

if not config:
    config["bore"] = float(input("① Bore (mm): "))
    config["stroke"] = float(input("② Stroke (mm): "))
    config["cylinders"] = int(input("③ Number of Cylinders: "))
    config["compression"] = float(input("④ Compression Ratio: "))
    config["redline"] = int(input("⑤ Redline RPM: "))
    config["engine_type"] = input("⑥ Engine Type (NA / Turbo / Supercharger / Twin-Turbo / Twincharged): ").strip().lower()
    config["layout"] = input("⑦ Engine Layout (inline / v / boxer): ").strip().lower()
    config["fuel_type"] = input("⑧ Fuel Type (gasoline / high-octane / diesel / e85 / methanol / lpg): ").strip().lower()
    config["vvl_enabled"] = input("⑨ Use VVL? (yes / no): ").strip().lower() == "yes"
    config["ambient_condition"] = input("⑩ Ambient Condition (normal / cold / hot): ").strip().lower()

    if config["vvl_enabled"]:
        config["vvl_rpm"] = int(input("VVL Activation RPM: "))
        config["vvl_profile"] = input("VVL Profile (mild / aggressive): ").strip().lower()
        if config["vvl_profile"] not in ["mild", "aggressive"]:
            print("잘못된 입력입니다. 기본값 'mild'로 설정합니다.")
            config["vvl_profile"] = "mild"
    else:
        config["vvl_rpm"] = 0
        config["vvl_profile"] = None

if not config.get("forced_type") and config["engine_type"] in ["turbo", "supercharger"]:
    show_forced_induction_options(config["engine_type"])
    config["forced_type"] = input(f"{config['engine_type'].capitalize()} Type: ").strip().lower()
    config["boost"] = float(input("Boost (bar): "))
elif not config.get("forced_type") and config["engine_type"] in ["twin-turbo", "twincharged"]:
    config["forced_type"] = config["engine_type"]
    config["boost"] = float(input("Boost (bar): "))
elif config["engine_type"] == "na":
    config["boost"] = 0
    config["forced_type"] = None

# 시뮬레이션 계산
bore = config["bore"] / 1000
stroke = config["stroke"] / 1000
cylinders = config["cylinders"]
compression = config["compression"]
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

fuel_hp_modifier = {
    "gasoline": 1.00, "high-octane": 1.05, "diesel": 0.85,
    "e85": 1.10, "methanol": 1.12, "lpg": 0.92
}.get(fuel_type, 1.0)

temp_power_modifier = 1.0
if ambient_condition == "cold":
    temp_power_modifier = 0.92
elif ambient_condition == "hot":
    temp_power_modifier = 0.95

displacement = (np.pi / 4) * (bore ** 2) * stroke * cylinders * 1000
layout_hp_modifier = {"inline": 1.0, "v": 1.05, "boxer": 0.97}.get(layout, 1.0)
layout_torque_rpm_modifier = {"inline": 1.0, "v": 1.1, "boxer": 0.85}.get(layout, 1.0)

na_base_hp = displacement * compression * 10 * layout_hp_modifier * fuel_hp_modifier * temp_power_modifier

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

peak_hp_rpm = int(redline * 0.85)
peak_torque_rpm = int(redline * 0.65 * layout_torque_rpm_modifier)
max_torque = max_hp_base * 7127 / peak_hp_rpm

sigma = (redline - 1000) / 3.5
torque = max_torque * np.exp(-((rpm - peak_torque_rpm) ** 2) / (2 * sigma ** 2)) * vvl_torque_gain
hp = torque * rpm / 7127 * vvl_hp_gain

max_hp_val = np.max(hp)
max_hp_rpm_actual = rpm[np.argmax(hp)]
max_torque_val = np.max(torque)
max_torque_rpm_actual = rpm[np.argmax(torque)]

interval_deg = 720 / cylinders
rpm_sim = 3000
rev_per_sec = rpm_sim / 60
spark_interval_time = 1 / (rev_per_sec * cylinders)
sim_time = np.linspace(0, 1, 1000)
spark_times = np.arange(0, 1, spark_interval_time)

plt.figure(figsize=(10, 5))
plt.plot(rpm, hp, label="Horsepower (HP)", color="red")
plt.plot(rpm, torque, label="Torque (Nm)", color="blue")
plt.axvline(max_hp_rpm_actual, linestyle='--', color='red', alpha=0.5)
plt.axvline(max_torque_rpm_actual, linestyle='--', color='blue', alpha=0.5)
plt.axvline(redline, linestyle=':', color='black', alpha=0.5)
if vvl_enabled:
    plt.axvline(vvl_rpm, linestyle='--', color='green', alpha=0.4)
    plt.text(vvl_rpm, max_hp_val * 0.6, f"VVL\nActive\n({vvl_profile})", color='green', fontsize=8, ha='center')
plt.text(max_hp_rpm_actual, max_hp_val + 10, f"{int(max_hp_val)} HP @ {int(max_hp_rpm_actual)} RPM",
         color='red', ha='center', fontsize=9, fontweight='bold')
plt.text(max_torque_rpm_actual, max_torque_val + 10, f"{int(max_torque_val)} Nm @ {int(max_torque_rpm_actual)} RPM",
         color='blue', ha='center', fontsize=9, fontweight='bold')
plt.title(f"Engine Output Curve ({layout.capitalize()} {engine_type.capitalize()}, Fuel: {fuel_type}, VVL: {'On' if vvl_enabled else 'Off'}, Ambient: {ambient_condition})")
plt.xlabel("RPM")
plt.ylabel("Horsepower (HP) / Torque (Nm)")
plt.legend()
plt.grid(True)
plt.yticks(np.arange(0, max(max_hp_val, max_torque_val) * 1.2, 50))
plt.tight_layout()
plt.show()
