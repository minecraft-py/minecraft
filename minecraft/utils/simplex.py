# MIT License
#
# Copyright (c) 2020 A. Svensson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""这是opensimplex库某一个历史版本的副本。

最新的opensimplex使用了numpy，可能严重影响程序运行效率。
"""

from ctypes import c_long
from math import floor

STRETCH_CONSTANT_2D = -0.211324865405187    # (1/sqrt(2+1)-1)/2
SQUISH_CONSTANT_2D = 0.366025403784439      # (sqrt(2+1)-1)/2
STRETCH_CONSTANT_3D = -1.0 / 6              # (1/sqrt(3+1)-1)/3
SQUISH_CONSTANT_3D = 1.0 / 3                # (sqrt(3+1)-1)/3

NORM_CONSTANT_2D = 47
NORM_CONSTANT_3D = 103

DEFAULT_SEED = 0

# Gradients for 2D. They approximate the directions to the
# vertices of an octagon from the center.
GRADIENTS_2D = (
    5,  2,    2,  5,
    -5,  2,   -2,  5,
    5, -2,    2, -5,
    -5, -2,   -2, -5,
)

# Gradients for 3D. They approximate the directions to the
# vertices of a rhombicuboctahedron from the center, skewed so
# that the triangular and square facets can be inscribed inside
# circles of the same radius.
GRADIENTS_3D = (
    -11,  4,  4,     -4,  11,  4,    -4,  4,  11,
    11,  4,  4,      4,  11,  4,     4,  4,  11,
    -11, -4,  4,     -4, -11,  4,    -4, -4,  11,
    11, -4,  4,      4, -11,  4,     4, -4,  11,
    -11,  4, -4,     -4,  11, -4,    -4,  4, -11,
    11,  4, -4,      4,  11, -4,     4,  4, -11,
    -11, -4, -4,     -4, -11, -4,    -4, -4, -11,
    11, -4, -4,      4, -11, -4,     4, -4, -11,
)


def overflow(x: int):
    # Since normal python ints and longs can be quite humongous we have to use
    # this hack to make them be able to overflow
    return c_long(x).value


class Simplex(object):

    def __init__(self, seed=DEFAULT_SEED):
        # Initializes the class using a permutation array generated from a 64-bit seed.
        # Generates a proper permutation (i.e. doesn't merely perform N
        # successive pair swaps on a base array)
        # Have to zero fill so we can properly loop over it later
        perm = self._perm = [0] * 256
        perm_grad_index_3D = self._perm_grad_index_3D = [0] * 256
        source = [i for i in range(0, 256)]
        seed = overflow(seed * 6364136223846793005 + 1442695040888963407)
        seed = overflow(seed * 6364136223846793005 + 1442695040888963407)
        seed = overflow(seed * 6364136223846793005 + 1442695040888963407)
        for i in range(255, -1, -1):
            seed = overflow(seed * 6364136223846793005 + 1442695040888963407)
            r = int((seed + 31) % (i + 1))
            if r < 0:
                r += i + 1
            perm[i] = source[r]
            perm_grad_index_3D[i] = int(
                (perm[i] % (len(GRADIENTS_3D) / 3)) * 3)
            source[r] = source[i]

    def _extrapolate2d(self, xsb, ysb, dx, dy):
        perm = self._perm
        index = perm[(perm[xsb & 0xFF] + ysb) & 0xFF] & 0x0E

        g1, g2 = GRADIENTS_2D[index:index + 2]
        return g1 * dx + g2 * dy

    def _extrapolate3d(self, xsb, ysb, zsb, dx, dy, dz):
        perm = self._perm
        index = self._perm_grad_index_3D[
            (perm[(perm[xsb & 0xFF] + ysb) & 0xFF] + zsb) & 0xFF
        ]

        g1, g2, g3 = GRADIENTS_3D[index:index + 3]
        return g1 * dx + g2 * dy + g3 * dz

    def noise2d(self, x: float, y: float) -> float:
        # Generate 2D OpenSimplex noise from X,Y coordinates.
        # Place input coordinates onto grid.
        stretch_offset = (x + y) * STRETCH_CONSTANT_2D
        xs = x + stretch_offset
        ys = y + stretch_offset

        # Floor to get grid coordinates of rhombus (stretched square) super-cell origin.
        xsb = floor(xs)
        ysb = floor(ys)

        # Skew out to get actual coordinates of rhombus origin. We'll need these later.
        squish_offset = (xsb + ysb) * SQUISH_CONSTANT_2D
        xb = xsb + squish_offset
        yb = ysb + squish_offset

        # Compute grid coordinates relative to rhombus origin.
        xins = xs - xsb
        yins = ys - ysb

        # Sum those together to get a value that determines which region we're in.
        in_sum = xins + yins

        # Positions relative to origin point.
        dx0 = x - xb
        dy0 = y - yb

        value = 0

        # Contribution (1,0)
        dx1 = dx0 - 1 - SQUISH_CONSTANT_2D
        dy1 = dy0 - 0 - SQUISH_CONSTANT_2D
        attn1 = 2 - dx1 * dx1 - dy1 * dy1
        extrapolate = self._extrapolate2d
        if attn1 > 0:
            attn1 *= attn1
            value += attn1 * attn1 * extrapolate(xsb + 1, ysb + 0, dx1, dy1)

        # Contribution (0,1)
        dx2 = dx0 - 0 - SQUISH_CONSTANT_2D
        dy2 = dy0 - 1 - SQUISH_CONSTANT_2D
        attn2 = 2 - dx2 * dx2 - dy2 * dy2
        if attn2 > 0:
            attn2 *= attn2
            value += attn2 * attn2 * extrapolate(xsb + 0, ysb + 1, dx2, dy2)

        if in_sum <= 1:  # We're inside the triangle (2-Simplex) at (0,0)
            zins = 1 - in_sum
            # (0,0) is one of the closest two triangular vertices
            if zins > xins or zins > yins:
                if xins > yins:
                    xsv_ext = xsb + 1
                    ysv_ext = ysb - 1
                    dx_ext = dx0 - 1
                    dy_ext = dy0 + 1
                else:
                    xsv_ext = xsb - 1
                    ysv_ext = ysb + 1
                    dx_ext = dx0 + 1
                    dy_ext = dy0 - 1
            else:  # (1,0) and (0,1) are the closest two vertices.
                xsv_ext = xsb + 1
                ysv_ext = ysb + 1
                dx_ext = dx0 - 1 - 2 * SQUISH_CONSTANT_2D
                dy_ext = dy0 - 1 - 2 * SQUISH_CONSTANT_2D
        else:  # We're inside the triangle (2-Simplex) at (1,1)
            zins = 2 - in_sum
            # (0,0) is one of the closest two triangular vertices
            if zins < xins or zins < yins:
                if xins > yins:
                    xsv_ext = xsb + 2
                    ysv_ext = ysb + 0
                    dx_ext = dx0 - 2 - 2 * SQUISH_CONSTANT_2D
                    dy_ext = dy0 + 0 - 2 * SQUISH_CONSTANT_2D
                else:
                    xsv_ext = xsb + 0
                    ysv_ext = ysb + 2
                    dx_ext = dx0 + 0 - 2 * SQUISH_CONSTANT_2D
                    dy_ext = dy0 - 2 - 2 * SQUISH_CONSTANT_2D
            else:  # (1,0) and (0,1) are the closest two vertices.
                dx_ext = dx0
                dy_ext = dy0
                xsv_ext = xsb
                ysv_ext = ysb
            xsb += 1
            ysb += 1
            dx0 = dx0 - 1 - 2 * SQUISH_CONSTANT_2D
            dy0 = dy0 - 1 - 2 * SQUISH_CONSTANT_2D

        # Contribution (0,0) or (1,1)
        attn0 = 2 - dx0 * dx0 - dy0 * dy0
        if attn0 > 0:
            attn0 *= attn0
            value += attn0 * attn0 * extrapolate(xsb, ysb, dx0, dy0)

        # Extra Vertex
        attn_ext = 2 - dx_ext * dx_ext - dy_ext * dy_ext
        if attn_ext > 0:
            attn_ext *= attn_ext
            value += attn_ext * attn_ext * \
                extrapolate(xsv_ext, ysv_ext, dx_ext, dy_ext)

        return value / NORM_CONSTANT_2D

    def noise3d(self, x: float, y: float, z: float) -> float:
        # Generate 3D OpenSimplex noise from X,Y,Z coordinates.
        # Place input coordinates on simplectic honeycomb.
        stretch_offset = (x + y + z) * STRETCH_CONSTANT_3D
        xs = x + stretch_offset
        ys = y + stretch_offset
        zs = z + stretch_offset

        # Floor to get simplectic honeycomb coordinates of rhombohedron (stretched cube) super-cell origin.
        xsb = floor(xs)
        ysb = floor(ys)
        zsb = floor(zs)

        # Skew out to get actual coordinates of rhombohedron origin. We'll need these later.
        squish_offset = (xsb + ysb + zsb) * SQUISH_CONSTANT_3D
        xb = xsb + squish_offset
        yb = ysb + squish_offset
        zb = zsb + squish_offset

        # Compute simplectic honeycomb coordinates relative to rhombohedral origin.
        xins = xs - xsb
        yins = ys - ysb
        zins = zs - zsb

        # Sum those together to get a value that determines which region we're in.
        in_sum = xins + yins + zins

        # Positions relative to origin point.
        dx0 = x - xb
        dy0 = y - yb
        dz0 = z - zb

        value = 0
        extrapolate = self._extrapolate3d
        if in_sum <= 1:  # We're inside the tetrahedron (3-Simplex) at (0,0,0)

            # Determine which two of (0,0,1), (0,1,0), (1,0,0) are closest.
            a_point = 0x01
            a_score = xins
            b_point = 0x02
            b_score = yins
            if a_score >= b_score and zins > b_score:
                b_score = zins
                b_point = 0x04
            elif a_score < b_score and zins > a_score:
                a_score = zins
                a_point = 0x04

            # Now we determine the two lattice points not part of the tetrahedron that may contribute.
            # This depends on the closest two tetrahedral vertices, including (0,0,0)
            wins = 1 - in_sum
            # (0,0,0) is one of the closest two tetrahedral vertices.
            if wins > a_score or wins > b_score:
                # Our other closest vertex is the closest out of a and b.
                c = b_point if (b_score > a_score) else a_point

                if (c & 0x01) == 0:
                    xsv_ext0 = xsb - 1
                    xsv_ext1 = xsb
                    dx_ext0 = dx0 + 1
                    dx_ext1 = dx0
                else:
                    xsv_ext0 = xsv_ext1 = xsb + 1
                    dx_ext0 = dx_ext1 = dx0 - 1

                if (c & 0x02) == 0:
                    ysv_ext0 = ysv_ext1 = ysb
                    dy_ext0 = dy_ext1 = dy0
                    if (c & 0x01) == 0:
                        ysv_ext1 -= 1
                        dy_ext1 += 1
                    else:
                        ysv_ext0 -= 1
                        dy_ext0 += 1
                else:
                    ysv_ext0 = ysv_ext1 = ysb + 1
                    dy_ext0 = dy_ext1 = dy0 - 1

                if (c & 0x04) == 0:
                    zsv_ext0 = zsb
                    zsv_ext1 = zsb - 1
                    dz_ext0 = dz0
                    dz_ext1 = dz0 + 1
                else:
                    zsv_ext0 = zsv_ext1 = zsb + 1
                    dz_ext0 = dz_ext1 = dz0 - 1
            else:  # (0,0,0) is not one of the closest two tetrahedral vertices.
                # Our two extra vertices are determined by the closest two.
                c = (a_point | b_point)

                if (c & 0x01) == 0:
                    xsv_ext0 = xsb
                    xsv_ext1 = xsb - 1
                    dx_ext0 = dx0 - 2 * SQUISH_CONSTANT_3D
                    dx_ext1 = dx0 + 1 - SQUISH_CONSTANT_3D
                else:
                    xsv_ext0 = xsv_ext1 = xsb + 1
                    dx_ext0 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D
                    dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D

                if (c & 0x02) == 0:
                    ysv_ext0 = ysb
                    ysv_ext1 = ysb - 1
                    dy_ext0 = dy0 - 2 * SQUISH_CONSTANT_3D
                    dy_ext1 = dy0 + 1 - SQUISH_CONSTANT_3D
                else:
                    ysv_ext0 = ysv_ext1 = ysb + 1
                    dy_ext0 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D
                    dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D

                if (c & 0x04) == 0:
                    zsv_ext0 = zsb
                    zsv_ext1 = zsb - 1
                    dz_ext0 = dz0 - 2 * SQUISH_CONSTANT_3D
                    dz_ext1 = dz0 + 1 - SQUISH_CONSTANT_3D
                else:
                    zsv_ext0 = zsv_ext1 = zsb + 1
                    dz_ext0 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D
                    dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D

            # Contribution (0,0,0)
            attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0
            if attn0 > 0:
                attn0 *= attn0
                value += attn0 * attn0 * \
                    extrapolate(xsb + 0, ysb + 0, zsb + 0, dx0, dy0, dz0)

            # Contribution (1,0,0)
            dx1 = dx0 - 1 - SQUISH_CONSTANT_3D
            dy1 = dy0 - 0 - SQUISH_CONSTANT_3D
            dz1 = dz0 - 0 - SQUISH_CONSTANT_3D
            attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
            if attn1 > 0:
                attn1 *= attn1
                value += attn1 * attn1 * \
                    extrapolate(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1)

            # Contribution (0,1,0)
            dx2 = dx0 - 0 - SQUISH_CONSTANT_3D
            dy2 = dy0 - 1 - SQUISH_CONSTANT_3D
            dz2 = dz1
            attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
            if attn2 > 0:
                attn2 *= attn2
                value += attn2 * attn2 * \
                    extrapolate(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2)

            # Contribution (0,0,1)
            dx3 = dx2
            dy3 = dy1
            dz3 = dz0 - 1 - SQUISH_CONSTANT_3D
            attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
            if attn3 > 0:
                attn3 *= attn3
                value += attn3 * attn3 * \
                    extrapolate(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3)
        # We're inside the tetrahedron (3-Simplex) at (1,1,1)
        elif in_sum >= 2:

            # Determine which two tetrahedral vertices are the closest, out of (1,1,0), (1,0,1), (0,1,1) but not (1,1,1).
            a_point = 0x06
            a_score = xins
            b_point = 0x05
            b_score = yins
            if a_score <= b_score and zins < b_score:
                b_score = zins
                b_point = 0x03
            elif a_score > b_score and zins < a_score:
                a_score = zins
                a_point = 0x03

            # Now we determine the two lattice points not part of the tetrahedron that may contribute.
            # This depends on the closest two tetrahedral vertices, including (1,1,1)
            wins = 3 - in_sum
            # (1,1,1) is one of the closest two tetrahedral vertices.
            if wins < a_score or wins < b_score:
                # Our other closest vertex is the closest out of a and b.
                c = b_point if (b_score < a_score) else a_point

                if (c & 0x01) != 0:
                    xsv_ext0 = xsb + 2
                    xsv_ext1 = xsb + 1
                    dx_ext0 = dx0 - 2 - 3 * SQUISH_CONSTANT_3D
                    dx_ext1 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D
                else:
                    xsv_ext0 = xsv_ext1 = xsb
                    dx_ext0 = dx_ext1 = dx0 - 3 * SQUISH_CONSTANT_3D

                if (c & 0x02) != 0:
                    ysv_ext0 = ysv_ext1 = ysb + 1
                    dy_ext0 = dy_ext1 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D
                    if (c & 0x01) != 0:
                        ysv_ext1 += 1
                        dy_ext1 -= 1
                    else:
                        ysv_ext0 += 1
                        dy_ext0 -= 1
                else:
                    ysv_ext0 = ysv_ext1 = ysb
                    dy_ext0 = dy_ext1 = dy0 - 3 * SQUISH_CONSTANT_3D

                if (c & 0x04) != 0:
                    zsv_ext0 = zsb + 1
                    zsv_ext1 = zsb + 2
                    dz_ext0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D
                    dz_ext1 = dz0 - 2 - 3 * SQUISH_CONSTANT_3D
                else:
                    zsv_ext0 = zsv_ext1 = zsb
                    dz_ext0 = dz_ext1 = dz0 - 3 * SQUISH_CONSTANT_3D
            else:  # (1,1,1) is not one of the closest two tetrahedral vertices.
                # Our two extra vertices are determined by the closest two.
                c = (a_point & b_point)

                if (c & 0x01) != 0:
                    xsv_ext0 = xsb + 1
                    xsv_ext1 = xsb + 2
                    dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D
                    dx_ext1 = dx0 - 2 - 2 * SQUISH_CONSTANT_3D
                else:
                    xsv_ext0 = xsv_ext1 = xsb
                    dx_ext0 = dx0 - SQUISH_CONSTANT_3D
                    dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D

                if (c & 0x02) != 0:
                    ysv_ext0 = ysb + 1
                    ysv_ext1 = ysb + 2
                    dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D
                    dy_ext1 = dy0 - 2 - 2 * SQUISH_CONSTANT_3D
                else:
                    ysv_ext0 = ysv_ext1 = ysb
                    dy_ext0 = dy0 - SQUISH_CONSTANT_3D
                    dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D

                if (c & 0x04) != 0:
                    zsv_ext0 = zsb + 1
                    zsv_ext1 = zsb + 2
                    dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D
                    dz_ext1 = dz0 - 2 - 2 * SQUISH_CONSTANT_3D
                else:
                    zsv_ext0 = zsv_ext1 = zsb
                    dz_ext0 = dz0 - SQUISH_CONSTANT_3D
                    dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D

            # Contribution (1,1,0)
            dx3 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D
            dy3 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D
            dz3 = dz0 - 0 - 2 * SQUISH_CONSTANT_3D
            attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
            if attn3 > 0:
                attn3 *= attn3
                value += attn3 * attn3 * \
                    extrapolate(xsb + 1, ysb + 1, zsb + 0, dx3, dy3, dz3)

            # Contribution (1,0,1)
            dx2 = dx3
            dy2 = dy0 - 0 - 2 * SQUISH_CONSTANT_3D
            dz2 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D
            attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
            if attn2 > 0:
                attn2 *= attn2
                value += attn2 * attn2 * \
                    extrapolate(xsb + 1, ysb + 0, zsb + 1, dx2, dy2, dz2)

            # Contribution (0,1,1)
            dx1 = dx0 - 0 - 2 * SQUISH_CONSTANT_3D
            dy1 = dy3
            dz1 = dz2
            attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
            if attn1 > 0:
                attn1 *= attn1
                value += attn1 * attn1 * \
                    extrapolate(xsb + 0, ysb + 1, zsb + 1, dx1, dy1, dz1)

            # Contribution (1,1,1)
            dx0 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D
            dy0 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D
            dz0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D
            attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0
            if attn0 > 0:
                attn0 *= attn0
                value += attn0 * attn0 * \
                    extrapolate(xsb + 1, ysb + 1, zsb + 1, dx0, dy0, dz0)
        else:  # We're inside the octahedron (Rectified 3-Simplex) in between.
            # Decide between point (0,0,1) and (1,1,0) as closest
            p1 = xins + yins
            if p1 > 1:
                a_score = p1 - 1
                a_point = 0x03
                a_is_further_side = True
            else:
                a_score = 1 - p1
                a_point = 0x04
                a_is_further_side = False

            # Decide between point (0,1,0) and (1,0,1) as closest
            p2 = xins + zins
            if p2 > 1:
                b_score = p2 - 1
                b_point = 0x05
                b_is_further_side = True
            else:
                b_score = 1 - p2
                b_point = 0x02
                b_is_further_side = False

            # The closest out of the two (1,0,0) and (0,1,1) will replace the furthest out of the two decided above, if closer.
            p3 = yins + zins
            if p3 > 1:
                score = p3 - 1
                if a_score <= b_score and a_score < score:
                    a_point = 0x06
                    a_is_further_side = True
                elif a_score > b_score and b_score < score:
                    b_point = 0x06
                    b_is_further_side = True
            else:
                score = 1 - p3
                if a_score <= b_score and a_score < score:
                    a_point = 0x01
                    a_is_further_side = False
                elif a_score > b_score and b_score < score:
                    b_point = 0x01
                    b_is_further_side = False

            # Where each of the two closest points are determines how the extra two vertices are calculated.
            if a_is_further_side == b_is_further_side:
                if a_is_further_side:  # Both closest points on (1,1,1) side

                    # One of the two extra points is (1,1,1)
                    dx_ext0 = dx0 - 1 - 3 * SQUISH_CONSTANT_3D
                    dy_ext0 = dy0 - 1 - 3 * SQUISH_CONSTANT_3D
                    dz_ext0 = dz0 - 1 - 3 * SQUISH_CONSTANT_3D
                    xsv_ext0 = xsb + 1
                    ysv_ext0 = ysb + 1
                    zsv_ext0 = zsb + 1

                    # Other extra point is based on the shared axis.
                    c = (a_point & b_point)
                    if (c & 0x01) != 0:
                        dx_ext1 = dx0 - 2 - 2 * SQUISH_CONSTANT_3D
                        dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D
                        dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D
                        xsv_ext1 = xsb + 2
                        ysv_ext1 = ysb
                        zsv_ext1 = zsb
                    elif (c & 0x02) != 0:
                        dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D
                        dy_ext1 = dy0 - 2 - 2 * SQUISH_CONSTANT_3D
                        dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D
                        xsv_ext1 = xsb
                        ysv_ext1 = ysb + 2
                        zsv_ext1 = zsb
                    else:
                        dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D
                        dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D
                        dz_ext1 = dz0 - 2 - 2 * SQUISH_CONSTANT_3D
                        xsv_ext1 = xsb
                        ysv_ext1 = ysb
                        zsv_ext1 = zsb + 2
                else:  # Both closest points on (0,0,0) side

                    # One of the two extra points is (0,0,0)
                    dx_ext0 = dx0
                    dy_ext0 = dy0
                    dz_ext0 = dz0
                    xsv_ext0 = xsb
                    ysv_ext0 = ysb
                    zsv_ext0 = zsb

                    # Other extra point is based on the omitted axis.
                    c = (a_point | b_point)
                    if (c & 0x01) == 0:
                        dx_ext1 = dx0 + 1 - SQUISH_CONSTANT_3D
                        dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D
                        dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D
                        xsv_ext1 = xsb - 1
                        ysv_ext1 = ysb + 1
                        zsv_ext1 = zsb + 1
                    elif (c & 0x02) == 0:
                        dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D
                        dy_ext1 = dy0 + 1 - SQUISH_CONSTANT_3D
                        dz_ext1 = dz0 - 1 - SQUISH_CONSTANT_3D
                        xsv_ext1 = xsb + 1
                        ysv_ext1 = ysb - 1
                        zsv_ext1 = zsb + 1
                    else:
                        dx_ext1 = dx0 - 1 - SQUISH_CONSTANT_3D
                        dy_ext1 = dy0 - 1 - SQUISH_CONSTANT_3D
                        dz_ext1 = dz0 + 1 - SQUISH_CONSTANT_3D
                        xsv_ext1 = xsb + 1
                        ysv_ext1 = ysb + 1
                        zsv_ext1 = zsb - 1
            else:  # One point on (0,0,0) side, one point on (1,1,1) side
                if a_is_further_side:
                    c1 = a_point
                    c2 = b_point
                else:
                    c1 = b_point
                    c2 = a_point

                # One contribution is a _permutation of (1,1,-1)
                if (c1 & 0x01) == 0:
                    dx_ext0 = dx0 + 1 - SQUISH_CONSTANT_3D
                    dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D
                    dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D
                    xsv_ext0 = xsb - 1
                    ysv_ext0 = ysb + 1
                    zsv_ext0 = zsb + 1
                elif (c1 & 0x02) == 0:
                    dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D
                    dy_ext0 = dy0 + 1 - SQUISH_CONSTANT_3D
                    dz_ext0 = dz0 - 1 - SQUISH_CONSTANT_3D
                    xsv_ext0 = xsb + 1
                    ysv_ext0 = ysb - 1
                    zsv_ext0 = zsb + 1
                else:
                    dx_ext0 = dx0 - 1 - SQUISH_CONSTANT_3D
                    dy_ext0 = dy0 - 1 - SQUISH_CONSTANT_3D
                    dz_ext0 = dz0 + 1 - SQUISH_CONSTANT_3D
                    xsv_ext0 = xsb + 1
                    ysv_ext0 = ysb + 1
                    zsv_ext0 = zsb - 1

                # One contribution is a _permutation of (0,0,2)
                dx_ext1 = dx0 - 2 * SQUISH_CONSTANT_3D
                dy_ext1 = dy0 - 2 * SQUISH_CONSTANT_3D
                dz_ext1 = dz0 - 2 * SQUISH_CONSTANT_3D
                xsv_ext1 = xsb
                ysv_ext1 = ysb
                zsv_ext1 = zsb
                if (c2 & 0x01) != 0:
                    dx_ext1 -= 2
                    xsv_ext1 += 2
                elif (c2 & 0x02) != 0:
                    dy_ext1 -= 2
                    ysv_ext1 += 2
                else:
                    dz_ext1 -= 2
                    zsv_ext1 += 2

            # Contribution (1,0,0)
            dx1 = dx0 - 1 - SQUISH_CONSTANT_3D
            dy1 = dy0 - 0 - SQUISH_CONSTANT_3D
            dz1 = dz0 - 0 - SQUISH_CONSTANT_3D
            attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1
            if attn1 > 0:
                attn1 *= attn1
                value += attn1 * attn1 * \
                    extrapolate(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1)

            # Contribution (0,1,0)
            dx2 = dx0 - 0 - SQUISH_CONSTANT_3D
            dy2 = dy0 - 1 - SQUISH_CONSTANT_3D
            dz2 = dz1
            attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2
            if attn2 > 0:
                attn2 *= attn2
                value += attn2 * attn2 * \
                    extrapolate(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2)

            # Contribution (0,0,1)
            dx3 = dx2
            dy3 = dy1
            dz3 = dz0 - 1 - SQUISH_CONSTANT_3D
            attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3
            if attn3 > 0:
                attn3 *= attn3
                value += attn3 * attn3 * \
                    extrapolate(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3)

            # Contribution (1,1,0)
            dx4 = dx0 - 1 - 2 * SQUISH_CONSTANT_3D
            dy4 = dy0 - 1 - 2 * SQUISH_CONSTANT_3D
            dz4 = dz0 - 0 - 2 * SQUISH_CONSTANT_3D
            attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4
            if attn4 > 0:
                attn4 *= attn4
                value += attn4 * attn4 * \
                    extrapolate(xsb + 1, ysb + 1, zsb + 0, dx4, dy4, dz4)

            # Contribution (1,0,1)
            dx5 = dx4
            dy5 = dy0 - 0 - 2 * SQUISH_CONSTANT_3D
            dz5 = dz0 - 1 - 2 * SQUISH_CONSTANT_3D
            attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5
            if attn5 > 0:
                attn5 *= attn5
                value += attn5 * attn5 * \
                    extrapolate(xsb + 1, ysb + 0, zsb + 1, dx5, dy5, dz5)

            # Contribution (0,1,1)
            dx6 = dx0 - 0 - 2 * SQUISH_CONSTANT_3D
            dy6 = dy4
            dz6 = dz5
            attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6
            if attn6 > 0:
                attn6 *= attn6
                value += attn6 * attn6 * \
                    extrapolate(xsb + 0, ysb + 1, zsb + 1, dx6, dy6, dz6)

        # First extra vertex
        attn_ext0 = 2 - dx_ext0 * dx_ext0 - dy_ext0 * dy_ext0 - dz_ext0 * dz_ext0
        if attn_ext0 > 0:
            attn_ext0 *= attn_ext0
            value += attn_ext0 * attn_ext0 * \
                extrapolate(xsv_ext0, ysv_ext0, zsv_ext0,
                            dx_ext0, dy_ext0, dz_ext0)

        # Second extra vertex
        attn_ext1 = 2 - dx_ext1 * dx_ext1 - dy_ext1 * dy_ext1 - dz_ext1 * dz_ext1
        if attn_ext1 > 0:
            attn_ext1 *= attn_ext1
            value += attn_ext1 * attn_ext1 * \
                extrapolate(xsv_ext1, ysv_ext1, zsv_ext1,
                            dx_ext1, dy_ext1, dz_ext1)

        return value / NORM_CONSTANT_3D
