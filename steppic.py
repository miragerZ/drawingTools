import matplotlib.pyplot as plt
import re

plt.rcParams['font.sans-serif'] = ['Times New Roman']  # 设置字体为Times New Roman
plt.rcParams['axes.unicode_minus'] = False

# ========== 格式化函数 ==========
def format_with_subscript(text):
    """将文本中的数字转换为下标"""
    # 匹配 字母/星号 + 数字 的模式，将数字转为下标
    return re.sub(r'([A-Za-z*])(\d+)', r'\1$_{{\2}}$', text)

# ========== 输入接口函数 ==========
def get_input_data():
    """获取用户输入的步骤和自由能数据"""
    print("=" * 50)
    print("电催化自由能台阶图输入接口")
    print("=" * 50)
    
    # 输入步骤名称
    steps_input = input("请输入步骤名称（用逗号分隔，如：*,*NO,*NHO,*NHOH）：")
    steps = [s.strip() for s in steps_input.split(',')]
    
    # 输入自由能数据
    energies_input = input("请输入每步的自由能（单位：eV，用逗号分隔，如：0.0,0.5,0.2,-0.3）：")
    try:
        free_energies = [float(e.strip()) for e in energies_input.split(',')]
    except ValueError:
        print("输入格式错误，使用默认数据")
        steps = ['*', '*NO', '*NHO', '*NHOH', '*NH', '*NH2', '*NH3']
        free_energies = [0.0, 0.5, 0.2, -0.3, 0.1, -0.2, -2]
    
    # 验证长度匹配
    if len(steps) != len(free_energies):
        print(f"警告：步骤数({len(steps)})与能量数({len(free_energies)})不匹配")
    
    return steps, free_energies

# ========== 默认使用方式（取消注释下面两行来启用输入接口） ==========
steps, free_energies = get_input_data()

# ========== 或者直接输入数据（默认使用） ==========
# 步骤名称
#steps = ['*', '*NO', '*NHO', '*NHOH', '*NH', '*NH2', '*NH3']  # 示例步骤名称，请替换为你的实际步骤名称
# 每一步的自由能（单位：eV，示例数据请替换为你的实际数据）
#free_energies = [0.0, 0.5, 0.2, -0.3, 0.1, -0.2, -2]


# 画台阶和虚线
plt.figure(figsize=(8, 5))

# 台阶宽度（缩短实线长度）
step_width = 0.3  # 实线台阶长度
num = len(free_energies)
for i in range(num):
    # 实线台阶（居中于每个数据点，首尾也延伸一半）
    left = i - step_width/2
    right = i + step_width/2
    plt.plot([left, right], [free_energies[i], free_energies[i]], color='b', linewidth=2)
    # 虚线斜线连接相邻台阶
    if i < num - 1:
        start_x = right
        end_x = (i+1) - step_width/2
        plt.plot([start_x, end_x], [free_energies[i], free_energies[i+1]], color='b', linestyle='--', linewidth=1)

# 数据点
plt.scatter(range(len(free_energies)), free_energies, color='b', zorder=5, s=1)  # 增加数据点的大小

# 标注每个能量值
for i, energy in enumerate(free_energies):
    plt.text(i, energy+0.05, f'{energy:.2f}', ha='center', fontsize=12)

# 在相邻数据点之间添加竖直虚线
for i in range(len(free_energies) - 1):
    plt.axvline(x=i+0.5, linestyle='--', color='gray', linewidth=0.8, alpha=0.5)

plt.xticks(range(len(steps)), [format_with_subscript(s) for s in steps], fontsize=14)
plt.ylabel('Free Energy (eV)', fontsize=20)
#plt.title('Electrochemical Free Energy Step Plot', fontsize=14)

# 设置y轴范围，在最大值和最小值外留一段距离
y_min = min(free_energies)
y_max = max(free_energies)
margin = (y_max - y_min) * 0.15  # 留出15%的距离
plt.ylim(y_min - margin, y_max + margin)

# 设置y轴数字字体大小
plt.yticks(fontsize=14)

plt.tight_layout()
plt.show()