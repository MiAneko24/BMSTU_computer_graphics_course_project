
class InvisiblePolygonsClipper:
    def __init__(self, tg, near, far):
        self.tg = tg
        self.near = near
        self.far = far
        pass

    def clip(self, polygons, normals):
        new_pols = []
        new_normals = []
        for i in range(len(polygons)):
            if not self.triangle_is_trivial_invisible(polygons[i]):
                new_normals.append(normals[i])
                new_pols.append(polygons[i])
        return new_pols, new_normals

    def triangle_is_trivial_invisible(self, vertices):
        flag = True
        for i in range(len(vertices)):
            if not self.is_trivial_invisible(vertices[i - 1], vertices[i]):
                flag = False
                break
        return flag

    def is_trivial_invisible(self, p1, p2):
        T1, sum1 = self.end(p1)
        T2, sum2 = self.end(p2)
        if self.bin_mul(T1, T2) != 0:
            return True
        return False

    def end(self, p):
        T = []
        if (p.x > self.tg * p.z):
            T.append(1)
        else:
            T.append(0)
        if (p.x < -self.tg * p.z):
            T.append(1)
        else:
            T.append(0)
        if (p.y > self.tg * p.z):
            T.append(1)
        else:
            T.append(0)
        if (p.y < -self.tg * p.z):
            T.append(1)
        else:
            T.append(0)
        if (p.z < self.near):
            T.append(1)
        else:
            T.append(0)
        if (p.z > self.far):
            T.append(1)
        else:
            T.append(0)
        sum = 0
        for i in T:
            sum += i
        return T, sum

    def bin_mul(self, T1, T2):
        mul = 0
        for i in range(len(T1)):
            mul += 1 if (T1[i] == 1 and T2[i] == 1) else 0
        return mul