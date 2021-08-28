from math import cos, pi, sin, sqrt

import numpy as np

from ObjectType import ObjectType
from PolygonalModels.SceneObject import SceneObject
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex


class Cylinder(SceneObject):

    def __init__(self, params):
        super().__init__(params)
        self.type = ObjectType.cylinder
        # self._r = params[0]
        # self._h = params[1]
        # self._n = params[2]
        up = [0., self._h, 0.]
        self.__get_polygonal_mesh(Vertex(up))
        self.__get_sphere()

    def __get_sphere(self):
        sphere = Sphere()
        sphere.radius = sqrt(self._h ** 2 / 4 + self._r ** 2)
        pq = self.vertices[1].vector - self.vertices[0].vector
        sphere.center = 1 / 2 * pq + self.vertices[0].vector
        self.sphere = sphere

    def __get_polygonal_mesh(self, up):
        # n = 5
        if self._n == 0:
            self._n = int(8 + self._r / 10)
        print("n= ", self._n)
        fixed_dots_amount = 2
        down = Vertex([up.x, up.y - self._h, up.z])
        vertices = [up, down]
        alpha = 2 * pi / self._n
        polygons = []
        for i in range(self._n):
            vertices.append(Vertex([up.x + self._r * cos(alpha * i), up.y, up.z + self._r * sin(alpha * i)]))
        for i in range(fixed_dots_amount, fixed_dots_amount + self._n):
            vertices.append(Vertex([vertices[i].x, vertices[i].y - self._h, vertices[i].z]))

        for i in range(fixed_dots_amount):
            for j in range(fixed_dots_amount + self._n * i, fixed_dots_amount + self._n * (i + 1) - 1):
                polygons.append([i, j, j + 1])
            polygons.append([i, fixed_dots_amount + self._n * (i + 1) - 1, fixed_dots_amount + self._n * i])

        for i in range(fixed_dots_amount, fixed_dots_amount + self._n - 1):
            polygons.append([i, i + 1, i + self._n])
        polygons.append([fixed_dots_amount + self._n - 1, fixed_dots_amount, fixed_dots_amount + 2 * self._n - 1])

        for i in range(fixed_dots_amount + self._n + 1, len(vertices)):
            polygons.append([i - 1, i, i - self._n])
        polygons.append([len(vertices) - 1, fixed_dots_amount + self._n, fixed_dots_amount])

        self.vertices = np.array(vertices)
        self.polygons = np.array(polygons)
        self.calculate_normals()

    def change(self, params):
        if super(Cylinder, self).change(params):
            self.__get_polygonal_mesh(Vertex([0., self._h, 0]))
            self.__get_sphere()
