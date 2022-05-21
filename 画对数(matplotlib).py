import matplotlib.pyplot as plt
import numpy as np
from math import *

# ==========================================================
#
#           本程序用于给液塑限画图，作为Turtle的Python练习。
#  QQ：13458482    Write by: 沈卫平   江苏恒基路桥股份有限公司   2022/05/14
#
# ==========================================================


# =============================
#       下面是全局变量
# =============================
# ---------------------------------------- 下面是全局变量
# ----------两含水率在hp点超过数据超2%的无效数据
# hc = 4.4  # 锥入深度
# hb = 9.6
# ha = 20.0
#
# Wc = 20.4  # 含水量
# Wb = 24.3
# Wa = 26.2

# ----------规范中正常数据
hc = 4.71  # 锥入深度
hb = 9.80
ha = 20

Wc = 29.9  # 含水量
Wb = 35.7
Wa = 41.04

Wl = 0  # 液限 塑限 塑性指数
Wp = 0
Ip = 0
hp = 0
hp2 = 0
clay_sand = False  # 是否砂类土，False时是细粒土，True是砂类土

hd = 0  # 两塑限点含水量中值对应锥入深度
Wd = 0  # 两塑限点含水量中值

error_flag = False  # 数据计算过程是否发现出错，为True说明有错


# ----------------------------------------


# ==========================================================
#
#       下面是主程序计算部分的调用，直接进行结果计算和打印输出。
#         先计算，不用从图上取点，因为内部做了直线方程计算
#
# ==========================================================

# 求直线方程相关数据
def get_line_point(x1, y1, x2, y2, mode, new_v=0):
    # y=kx+c
    # mode为1时,得k                    # mode为2时,得c
    # mode为3时,得new_v作为x时对应值y    # mode为4时,得new_v作为y时对应值x
    k = (y1 - y2) / (x1 - x2)
    c = (x1 * y2 - x2 * y1) / (x1 - x2)
    ret = 0.0
    if mode == 1:
        ret = k
    elif mode == 2:
        ret = c
    elif mode == 3:
        ret = k * new_v + c
    else:
        ret = (new_v - c) / k
    return ret


# 求hp
def get_hp(liqud, clay_sand):
    # clay_sand  是否砂类土，False时是细粒土，True是砂类土
    if clay_sand is True:
        return 29.6 - 1.22 * liqud + 0.017 * liqud ** 2 - 0.0000744 * liqud ** 3  # 如果是砂性土的hp（多项式）
    else:
        return liqud / (0.524 * liqud - 7.606)  # 如果是细粒土的hp（双曲线）


# 先打印结果
def print_result():
    print(f"hp={hp2:.2f}")
    print(f"Wl={Wl:.1f}%        Wp={Wp:.1f}%        Ip={Ip:.1f}%")
    if error_flag is True:
        print("数据无效，请检查原始数据。")
    else:
        print("计算正常结束，数据有效。")


def get_result():
    global hp, hp2, Wl, Wp, Ip  # 声音全局变量，不然其它过程不能调用结果
    global error_flag
    hp = get_hp(Wa, clay_sand)
    yhp = log10(hp)
    # a点对数坐标
    xa = log10(Wa)
    ya = log10(ha)
    # b点对数坐标
    xb = log10(Wb)
    yb = log10(hb)
    # c点对数坐标
    xc = log10(Wc)
    yc = log10(hc)
    # 在对数坐标上定ab和ac两线在hp处的含水量检查
    Wab_hp = 10 ** get_line_point(xa, ya, xb, yb, 4, yhp)
    Wac_hp = 10 ** get_line_point(xa, ya, xc, yc, 4, yhp)
    if abs(Wab_hp - Wac_hp) >= 2:  # 如果两个含水量误差大于2, 显示出错，提前退出
        print(f"试验无效, ab线在hp点的含水率是{Wab_hp:.1f}, ac线在hp点的含水率是{Wac_hp:.1f}, 两者相差{abs(Wab_hp - Wac_hp):.1f}, 相差≥2，试验要重做。")
        error_flag = True
        # sys.exit(1)  # 提前退出
    if abs(ha - 20) >= 0.2:  # 如果a点锥入深度不在20±0.2mm范围内，显示出错，提前退出
        print(ha)
        print(f"a点锥入深度为{ha:.2f}，不在20±0.2mm范围内，试验要重做。")
        error_flag = True
        # sys.exit(1)  # 提前退出
    # 求得两个含水量平均值做为d点含水量
    global Wd, hd  # =========================这里是要为改全局变量做准备
    Wd = (Wab_hp + Wac_hp) / 2
    hd = hp
    # d点对数坐标
    xd = log10(Wd)
    yd = log10(hd)
    # 锥入深度为20mm时为液限
    hl = 20
    Wl = 10 ** get_line_point(xa, ya, xd, yd, 4, log10(hl))
    hp2 = get_hp(Wl, clay_sand)  # hp2为hp'
    # hp'在ad线上查得对应含水率为Wp
    Wp = 10 ** get_line_point(xa, ya, xd, yd, 4, log10(hp2))
    Ip = Wl - Wp


# =============================下面是计算过程
get_result()
print_result()


# =============================到此计算过程结束

# =============================
#
#    下面是下面是进行绘图操作。
#
# =============================
# 下面设图的特性和绘底图
def draw_background():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决图例和坐标轴标题的中文显示乱码问题
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.figure(figsize=(4, 7), dpi=100)  # 设图的尺寸，英寸
    plt.title('液塑限h-w')
    #  ---------------绘制半对数坐标系下x和y的关系图像
    plt.semilogx()  # 将x轴设置为对数坐标轴(semilogx()默认以10为底数，这意味着x轴上的每单位刻度的大小为10)
    plt.semilogy()  # 将y轴设置为对数坐标轴
    # ---------------设坐标轴上的刻度
    plt.xlim(10, 50)  # x轴的刻度从10-50
    plt.xticks([10, 20, 30, 40, 50], [r'$10$', r'$20$', r'$30$', r'$40$', r'$50$']) # 这里直接把r'$10$'换用‘10’也可以
    plt.ylim(1, 30)  # x轴的刻度从1-30
    plt.yticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30],
               [r'$1$', r'$2$', r'$3$', r'$4$', r'$5$', r'$6$', r'$7$', r'$8$', r'$9$', r'$10$', r'$20$', r'$30$'])
    plt.grid(True)  # 显示网格
    plt.xlabel("含水率w (%)", fontsize=12)  # 显示x轴的标题
    plt.ylabel("锥入深度h (mm)", fontsize=12)


# 画ab、ac、ad三根线，再把液塑限点的横竖坐标线标出来
def draw_ab_ac_ad_line():
    # global hp, hp2, Wd, Wl, Wp, Ip  # 声音全局变量，不然其它过程不能调用结果
    # ---------------绘制ab和ac线,有标记符
    x = np.array([Wb, Wa])
    y = np.array([hb, ha])
    plt.plot(x, y, marker='o', color="blue")  # 画有标记符的线
    x = np.array([Wc, Wa])
    y = np.array([hc, ha])
    plt.plot(x, y, marker='o', color="darkgreen")

    # ---------------绘制ab线延长部分,无有标记符
    # ---------------左下点
    hy1 = hp - 2
    if hy1 < 1.5:
        hy1 = 1.5
    hx1 = get_line_point(log10(Wa), log10(ha), log10(Wb), log10(hb), 4, log10(hy1))
    hx1 = 10 ** hx1
    # ---------------右上点
    hy2 = ha + 8
    hx2 = get_line_point(log10(Wa), log10(ha), log10(Wb), log10(hb), 4, log10(hy2))
    hx2 = 10 ** hx2
    x = np.array([hx2, hx1])
    y = np.array([hy2, hy1])
    plt.plot(x, y, marker='', color="blue")  # 画没有标记符的线
    # ---------------绘制ac线延长部分
    # ---------------左下点
    hx1 = get_line_point(log10(Wa), log10(ha), log10(Wc), log10(hc), 4, log10(hy1))
    hx1 = 10 ** hx1
    # ---------------右上点
    # hy2用前面的
    hx2 = get_line_point(log10(Wa), log10(ha), log10(Wc), log10(hc), 4, log10(hy2))
    hx2 = 10 ** hx2
    x = np.array([hx2, hx1])
    y = np.array([hy2, hy1])
    plt.plot(x, y, marker='', color="darkgreen")

    # ---------------绘制ad线
    x = np.array([Wa, Wd])
    y = np.array([ha, hd])
    plt.plot(x, y, marker='s', color="red")

    # ---------------绘制ad线延长部分
    # ---------------左下点
    hx1 = get_line_point(log10(Wa), log10(ha), log10(Wd), log10(hd), 4, log10(hy1))
    hx1 = 10 ** hx1
    # ---------------右上点
    # hy2用前面的
    hx2 = get_line_point(log10(Wa), log10(ha), log10(Wd), log10(hd), 4, log10(hy2))
    hx2 = 10 ** hx2
    x = np.array([hx2, hx1])
    y = np.array([hy2, hy1])
    plt.plot(x, y, marker='', color="red")  # ad线

    # ---------------画液限点的水平和垂直虚线
    x = np.array([0, Wl])
    y = np.array([20, 20])
    plt.plot(x, y, linestyle="--", color="darkorange")
    x = np.array([Wl, Wl])
    y = np.array([0, 20])
    plt.plot(x, y, linestyle="--", color="darkorange")

    # ---------------画塑限点的水平和垂直虚线
    x = np.array([0, Wp])
    y = np.array([hd, hd])
    plt.plot(x, y, linestyle="--", color="darkorange")
    x = np.array([Wd, Wd])
    y = np.array([0, hd])
    plt.plot(x, y, linestyle="--", color="darkorange")

    # ---------------画上加备注文本a b c
    plt.annotate(
        r'$a$',  # 备注文本
        xycoords='data',  # 定位目标点使用的参照坐标系
        xy=(Wa, ha),  # 目标点的坐标
        textcoords='offset points',  # 定位文本位置使用的坐标系
        xytext=(-10, 10),  # 备注文本的位置坐标
        fontsize=12,  # 字体大小
        # arrowprops=dict(arrowstyle='->', connectionstyle='angle3')
    )
    plt.annotate(
        r'$b$',  # 备注文本
        xycoords='data',  # 定位目标点使用的参照坐标系
        xy=(Wb, hb),  # 目标点的坐标
        textcoords='offset points',  # 定位文本位置使用的坐标系
        xytext=(-10, 10),  # 备注文本的位置坐标
        fontsize=12,  # 字体大小
    )
    plt.annotate(
        r'$c$',  # 备注文本
        xycoords='data',  # 定位目标点使用的参照坐标系
        xy=(Wc, hc),  # 目标点的坐标
        textcoords='offset points',  # 定位文本位置使用的坐标系
        xytext=(-10, 10),  # 备注文本的位置坐标
        fontsize=12,  # 字体大小
    )
    # ---------------画上加备注文本液限和塑限
    plt.annotate(
        '液限',  # 备注文本
        xycoords='data',  # 定位目标点使用的参照坐标系
        xy=(Wa, ha),  # 目标点的坐标
        textcoords='offset points',  # 定位文本位置使用的坐标系
        xytext=(-40, -30),  # 备注文本的位置坐标
        fontsize=10,  # 字体大小
        arrowprops=dict(arrowstyle='->', connectionstyle='angle3')
    )
    plt.annotate(
        '塑限',  # 备注文本
        xy=(Wd, hd),  # 目标点的坐标
        textcoords='offset points',  # 定位文本位置使用的坐标系
        xytext=(-40, 30),  # 备注文本的位置坐标
        fontsize=10,  # 字体大小
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2')
    )


# =============================
#       下面开始出图
# =============================
draw_background()
draw_ab_ac_ad_line()
plt.show()  # 出图
