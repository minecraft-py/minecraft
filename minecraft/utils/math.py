# 该文件提供的一次函数, 二次函数全部应用于三维笛卡尔坐标系中,
# 即在二维坐标系内增加一 z 轴, 通过将函以给定角度旋转, 计算出
# 旋转后函数图像上的任意一点在三维坐标系中的位置
# 同样的, make_liner_function, make_quadratic_function 两个
# 求解析式函数只接受三维坐标
# * 该文件的具体实现已在上文提出, 且已有规定轮廓但未实现 *

import math


class LinerFunction():

    def __init__(self, k, b):
        # 一次函数
        # 函数解析式: f(x) = kx + b
        pass


class QuadraticFunction():

    def __init__(self, h, k):
        # 二次函数
        # 函数解析式: f(x) = a(x - h) ** 2 + k
        pass


def make_liner_function(p, q):
    # 生成一次函数, 给定直线上任意两点
    assert (len(p) == 3) and (len(q) == 3)

def make_quadratic_function(p, q):
    # 生成抛物线, 给定顶点与任意一点
    # p 为顶点, q 为抛物线上任意一点
    assert (len(p) == 3) and (len(q) == 3)
