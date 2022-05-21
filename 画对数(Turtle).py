from math import *
from turtle import *

# ==========================================================
#
#           本程序用于给液塑限画图，作为Turtle的Python练习。
#  QQ：13458482    Write by: 沈卫平   江苏恒基路桥股份有限公司   2022/05/14
#
# ==========================================================


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

# 将理论坐标转换到最后出图的对数坐标
def realCoord_to_lastCoord(x, y):
    dict_coord["X"] = (log(x, 10) - log(坐标系X轴最小值, 10)) * X_Scale
    dict_coord["Y"] = (log(y, 10) - log(坐标系Y轴最小值, 10)) * Y_Scale


# 将最后出图的对数坐标转换到理论坐标
def lastCoord_to_realCoord(x, y):
    dict_coord["X"] = 10 ** (x / X_Scale + log10(坐标系X轴最小值))
    dict_coord["Y"] = 10 ** (y / Y_Scale + log10(坐标系Y轴最小值))


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


def print_result():
    print(f"hp={hp2:.2f}")
    print(f"Wl={Wl:.1f}%        Wp={Wp:.1f}%        Ip={Ip:.1f}%")
    if error_flag is True:
        print("数据无效，请检查原始数据。")
    else:
        print("计算正常结束，数据有效。")


# =============================下面是计算过程
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


# ==========================================================
#
#       下面是主程序计算部分的调用，直接进行结果计算和打印输出。
#         先计算，不用从图上取点，因为内部做了直线方程计算
#
# ==========================================================
get_result()
print_result()

# ==========================================================
#
#                   下面是下面是进行绘图操作。
#
# ==========================================================

# -------------------------------------------- 下面是全局变量
窗口宽 = 500  # 绘图区窗口高宽
窗口高 = 800

坐标系X轴最小值 = 10  # 大于等于1
坐标系X轴最大值 = round((Wl + 20) / 10) * 10  # 比液限大20的整数倍
坐标系Y轴最小值 = 1  # 大于等于1
坐标系Y轴最大值 = 40  # 10的倍数

垂直横坐标线值列表 = []  # 垂直横坐标线对数值列表
垂直纵坐标线值列表 = []  # 垂直纵坐标线对数值列表

点的半径 = 6

X_Scale = 窗口宽 / (log(坐标系X轴最大值, 10) - log(坐标系X轴最小值, 10))  # 横坐标放大比例
Y_Scale = 窗口高 / (log(坐标系Y轴最大值, 10) - log(坐标系Y轴最小值, 10))  # 纵坐标放大比例

dict_coord = {"X": 1, "Y": 1}


# 做出垂直横坐标对数值,比如10-70,每间隔10做一线
def col_list_cal():
    minX = 坐标系X轴最小值  # "坐标系X轴最小值"是外面声明过的全局变量,如果只读不改,不用global声明
    maxX = 坐标系X轴最大值
    for i in range(minX, maxX + 10, 10):
        垂直横坐标线值列表.append(log10(i) - log10(坐标系X轴最小值))


# 做出垂直纵坐标对数值,比如1-40, 其中如果1-10内每间隔1做一线，10以上的每间隔10做一线
def row_list_cal():
    minY = 坐标系Y轴最小值
    maxY = 坐标系Y轴最大值
    #  小于10部分,就在10之前每间隔1画线，直到10
    for i in range(minY, 10):  # 从i到9，间隙1
        垂直纵坐标线值列表.append(log10(i) - log10(minY))
    minY = 10  # 然后以后画间隙10的线最小值从10开始
    for i in range(minY, maxY + 10, 10):
        垂直纵坐标线值列表.append(log10(i) - log10(坐标系Y轴最小值))


# 画出底图,包括外框和双对数网格线
def draw_background():
    tracer(0)  # 完全不显示轨迹，是最快速度
    # speed(0)  # speen最快速度,  但没有上面快
    title('液塑限h-w')
    pensize(5)  # 画外框用粗线
    pencolor("black")
    pendown()
    goto(0, 0)
    goto(窗口宽, 0)
    goto(窗口宽, 窗口高)
    goto(0, 窗口高)
    goto(0, 0)
    pensize(1)  # 网络线用细线
    setheading(90)  # 方向向上
    pencolor("gray")  # 网络线用灰色
    for i in 垂直横坐标线值列表:
        penup()  # 抬笔
        goto(i * X_Scale, 0)
        pendown()  # 落笔
        forward((log(坐标系Y轴最大值, 10) - log(坐标系Y轴最小值, 10)) * Y_Scale)
    setheading(0)  # 方向向右，即X轴正方向
    for i in 垂直纵坐标线值列表:
        penup()
        goto(0, i * Y_Scale)
        pendown()
        forward((log(坐标系X轴最大值, 10) - log(坐标系X轴最小值, 10)) * X_Scale)
    penup()
    goto(窗口宽 / 2, -60)
    write('含水量w(%)', align='center', font=('Arial', 12, "bold"))
    penup()


# 写坐标轴上的刻度文字
def write_coord_text():
    pensize(2)
    pencolor("black")
    # turtle.write(arg, move=False, align=“left”, font = (“Arial”, 8, “normal”))
    for i in 垂直横坐标线值列表:
        penup()
        goto(i * X_Scale, -30)
        pendown()
        write(round(10 ** (i + log10(坐标系X轴最小值))), align='center', font=('Arial', 12, "normal"))
    for i in 垂直纵坐标线值列表:
        penup()
        goto(0 - 30, i * Y_Scale - 10)
        pendown()
        write(round(10 ** (i + log(坐标系Y轴最小值, 10))), align='center', font=('Arial', 12, "normal"))
        penup()


# 给出线性坐标，内部转换成对数坐标，画一个点，并加上标注
def draw_one_point(real_x, real_y, point_color, msg_str):
    penup()
    realCoord_to_lastCoord(real_x, real_y)
    goto(dict_coord["X"], dict_coord["Y"] - 点的半径)
    pendown()
    color(point_color)
    begin_fill()
    circle(点的半径)  # 半径为正(负)，表示圆心在画笔的左边(右边)画圆
    end_fill()  # 每次填充完了都要停,不然会和后面联起来
    penup()
    forward(20)  # 向右移
    pendown()
    write(msg_str, align="left", font=("Arial", 15, "normal"))
    penup()


# 画abc三个点
def draw_abcd_point():
    draw_one_point(Wa, ha, 'green', 'a')
    draw_one_point(Wb, hb, 'green', 'b')
    draw_one_point(Wc, hc, 'green', 'c')
    draw_one_point(Wd, hd, 'green', '')


# 画ab、ac、ad三根线，再把液塑限点的横竖坐标线标出来
def draw_ab_ac_ad_line():
    realCoord_to_lastCoord(Wa, ha)  # a点最后出图的对数坐标
    x1 = dict_coord["X"]
    y1 = dict_coord["Y"]
    realCoord_to_lastCoord(Wb, hb)  # b点最后出图的对数坐标
    x2 = dict_coord["X"]
    y2 = dict_coord["Y"]
    realCoord_to_lastCoord(Wc, hc)  # c点最后出图的对数坐标
    x3 = dict_coord["X"]
    y3 = dict_coord["Y"]
    realCoord_to_lastCoord(Wd, hd)  # d点最后出图的对数坐标
    x4 = dict_coord["X"]
    y4 = dict_coord["Y"]
    # ----------ab线
    y_up = ha + 8  # ----- 比a高8个线性值
    y_up = (log10(y_up) - log10(坐标系Y轴最小值)) * Y_Scale  # y_up现在是上端出头，比上点ha高8线性值的对数坐标
    y_down = hp - 2  # ---- 比hp低2
    if y_down < 1.5:
        y_down = 1.5
    y_down = (log10(y_down) - log10(坐标系Y轴最小值)) * Y_Scale  # y_down现在是下端出头，比下点hp低1.5线性值的对数坐标
    pensize(2)
    x_up = get_line_point(x1, y1, x2, y2, 4, y_up)
    x_down = get_line_point(x1, y1, x2, y2, 4, y_down)
    goto(x_up, y_up)
    pendown()
    goto(x_down, y_down)
    penup()
    # ----------ac线
    x_up = get_line_point(x1, y1, x3, y3, 4, y_up)
    x_down = get_line_point(x1, y1, x3, y3, 4, y_down)
    goto(x_up, y_up)
    pendown()
    goto(x_down, y_down)
    penup()
    # ----------ad线
    x_up = get_line_point(x1, y1, x4, y4, 4, y_up)
    x_down = get_line_point(x1, y1, x4, y4, 4, y_down)
    color('red')
    goto(x_up, y_up)
    pendown()
    goto(x_down, y_down)
    penup()

    # ----------画液限点的虚线
    pensize(3)
    pencolor("violet")
    draw_dash_line(x1, 0, x1, y1, 15, 15)
    draw_dash_line(x1, y1, 0, y1, 15, 15)

    # ----------画塑限点的虚线
    draw_dash_line(x4, 0, x4, y4, 15, 15)
    draw_dash_line(x4, y4, 0, y4, 15, 15)


# 自定义画虚线方法，因为Turtle没有画虚线功能
def draw_dash_line(x1, y1, x2, y2, line, blank):
    # x1,y1是起点坐标，x2,y2是终点坐标，line是虚线的每小段实线段长，blank是虚线的每小段空白段的长
    a = y2 - y1
    b = x2 - x1
    c = sqrt(a * a + b * b)
    dis = c  # 要画的总距离
    goto(x1, y1)
    if c == 0:  # 防止后面被0除，angle就得不到正常值
        angle = 0
    else:
        angle = abs(asin(a / c) * 180 / pi)  # 得到角度的度数值，发现此处不能用degrees()函数转换，官方math库有重大缺陷，传入某些数据会导致系统崩溃
    # 下面根据a和b的正负号判断象限，校正转向角度
    if a >= 0 and b >= 0:  # 第一象限
        angle = angle
    elif a >= 0 and b < 0:  # 第二象限
        angle = 180 - angle
    elif a <= 0 and b <= 0:  # 第三象限
        angle = 180 + angle
    elif a <= 0 and b >= 0:  # 第四象限
        angle = -angle
    setheading(angle)  # 为正逆时针转向，为负顺时针转向。每次X轴正方向为基准转向。
    d = 0  # 虚线从出发点开始的累计行进距离值
    while d <= dis:
        left_d = dis - d  # 剩下还有多少距离没爬
        if left_d >= blank + line:  # 如果有的是剩余距离
            pendown()  # 走画一段，再抬笔走一段，形成虚线
            forward(line)
            penup()
            forward(blank)
        elif left_d >= line:  # 如果剩余距离只能放得下一个完整的line长
            pendown()
            forward(line)
        elif left_d < line:  # 如果剩余距离只能放得一个不完整的line长
            pendown()
            forward(left_d)
        penup()
        d = d + line + blank


# ==========================================================
#
#       下面是主程序绘图部分的调用，部分调用前面计算结果。
#
# ==========================================================
col_list_cal()  # 生成竖向坐标轴线刻度值
row_list_cal()  # 生成横向坐标轴线刻度值

setup(窗口宽, 窗口高)  # 设置窗口
# screensize(窗口宽,窗口高)#设置画布大小
setworldcoordinates(0, 0, 窗口宽, 窗口高)  # 设置世界坐标体系，左下角为（0，0）
draw_background()
write_coord_text()
draw_abcd_point()
draw_ab_ac_ad_line()

setworldcoordinates(-100, -100, 窗口宽 + 100, 窗口高 + 100)
# print(window_width(), window_height())
hideturtle()
done()  # 运行结束但不退出，必须是乌龟图形程序中的最后一个语句。

