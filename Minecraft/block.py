def tex_coord(x, y, n=4):
    #返回纹理正方形绑定的顶点
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m

def tex_coords(top, bottom, side):
    # 返回纹理正方形的顶面, 底面, 侧面
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result

def tex_coords_all(top, bottom, side0, side1, side2, side3):
    # 返回纹理正方形所有的面
    # 同 tex_coords() 类似, 但是要传入全部的四个侧面
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side0, side1 = tex_coord(*side0), tex_coord(*side1)
    side2, side3 = tex_coord(*side2), tex_coord(*side3)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side0)
    result.extend(side1)
    result.extend(side2)
    result.extend(side3)
    return result

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
DIRT = tex_coords((0, 1), (0, 1), (0, 1))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
STONE = tex_coords((0, 2), (0, 2), (0, 2))
LOG = tex_coords((1, 2), (1, 2), (2, 2))
LEAF = tex_coords((3, 1), (3, 1), (3, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
PLANK = tex_coords((3, 0), (3, 0), (3, 0))
CRAFT_TABLE = tex_coords((0, 3), (3, 0), (1, 3))
BEDROCK = tex_coords((2, 1), (2, 1), (2, 1))
