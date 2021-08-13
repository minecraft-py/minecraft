# 该文件提供的一次函数, 二次函数全部应用于三维笛卡尔坐标系中,
# 即在二维坐标系内增加一 z 轴, 通过将函以给定角度旋转, 计算出
# 旋转后函数图像上的任意一点在三维坐标系中的位置
# 同样的, make_liner_function, make_quadratic_function 两个
# 求解析式函数只接受三维坐标

import math


class LinerFunction():

    def __init__(self, k, b, degree=0):
        # 一次函数
        # 函数解析式: f(x) = kx + b
        self.k = k
        self.b = b
        self.degree = degree

    def get(self, x):
        y = self.k * x + self.b
        z = math.tan(math.radians(self.degree)) * x
        return (x, y, z)

    def __repr__(self):
        return '%s(k=%s, b=%s, degree=%s)' % (self.__class__.__name__, self.k, self.b, self.degree)


class QuadraticFunction():

    def __init__(self, h, k):
        # 二次函数
        # 函数解析式: f(x) = a(x - h) ** 2 + k
        pass


def make_liner_function(p, q):
    # 生成一次函数, 给定直线上任意两点
    assert (len(p) == 3) and (len(q) == 3)
    deg = math.degrees(math.atan(abs(p[2] - q[2]) / abs(p[0] - q[0])))
    k = (p[1] - q[1]) / (p[0] - q[0])
    b = p[1] - k * p[0]
    return LinerFunction(k, b, deg)

def make_quadratic_function(p, q):
    # 生成抛物线, 给定顶点与任意一点
    # p 为顶点, q 为抛物线上任意一点
    assert (len(p) == 3) and (len(q) == 3)
