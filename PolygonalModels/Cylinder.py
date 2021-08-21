from math import cos, pi, sin, sqrt

import numpy as np

from ObjectType import ObjectType
from PolygonalModels.SceneObject import SceneObject
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex

# Lags in case cylinder, radius is 20, height is 30, check z-buffer

class Cylinder(SceneObject):

    def __init__(self, params):
        super().__init__(params[3:])
        self.type = ObjectType.cylinder
        r = params[0]
        h = params[1]
        n = params[2]
        up = [0., h, 0.]
        self.__get_polygonal_mesh(r, h, n, Vertex(up))
        self.__get_sphere(r, h)

    def __get_sphere(self, r, h):
        sphere = Sphere()
        sphere.radius = sqrt(h ** 2 / 4 + r ** 2)
        pq = self.vertices[1].vector - self.vertices[0].vector
        sphere.center = 1 / 2 * pq + self.vertices[0].vector
        self.sphere = sphere

    def __get_polygonal_mesh(self, r, h, n, up):
        # n = 5
        if n == 0:
            n = int(8 + r / 10)
        print("n= ", n)
        fixed_dots_amount = 2
        down = Vertex([up.x, up.y - h, up.z])
        vertices = [up, down]
        alpha = 2 * pi / n
        polygons = []
        for i in range(n):
            vertices.append(Vertex([up.x + r * cos(alpha * i), up.y, up.z + r * sin(alpha * i)]))
        for i in range(fixed_dots_amount, fixed_dots_amount + n):
            vertices.append(Vertex([vertices[i].x, vertices[i].y - h, vertices[i].z]))

        for i in range(fixed_dots_amount):
            for j in range(fixed_dots_amount + n * i, fixed_dots_amount + n * (i + 1) - 1):
                polygons.append([i, j, j + 1])
            polygons.append([i, fixed_dots_amount + n * (i + 1) - 1, fixed_dots_amount + n * i])

        for i in range(fixed_dots_amount, fixed_dots_amount + n - 1):
            polygons.append([i, i + 1, i + n])
        polygons.append([fixed_dots_amount + n - 1, fixed_dots_amount, fixed_dots_amount + 2 * n - 1])

        for i in range(fixed_dots_amount + n + 1, len(vertices)):
            polygons.append([i - 1, i, i - n])
        polygons.append([len(vertices) - 1, fixed_dots_amount + n, fixed_dots_amount])

        self.vertices = np.array(vertices)
        self.polygons = np.array(polygons)
        self.calculate_normals()
