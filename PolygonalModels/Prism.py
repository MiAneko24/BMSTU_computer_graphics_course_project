from math import pi, sin, sqrt

import numpy as np

from PolygonalModels.ObjectType import ObjectType
from PolygonalModels.SceneObject import SceneObject
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex


class Prism(SceneObject):
    def __init__(self, params):
        if params[2] == 0:
            raise AttributeError
        params[0] = params[0] / (2 * sin(pi/params[2]))
        super().__init__(params)
        self.type = ObjectType.pyramid
        up = np.array([0., self._h, 0.])

        self.__get_polygonal_mesh(Vertex(up))
        self.__get_sphere()

    def __get_sphere(self):
        sphere = Sphere()
        sphere.radius = sqrt(self._h ** 2 / 4 + self._r ** 2)
        pq = self.vertices[1].vector - self.vertices[0].vector
        sphere.center = 1 / 2 * pq + self.vertices[0].vector
        self.sphere = sphere

    def __get_polygonal_mesh(self, up):
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
        n = params['n'] if params['n'] is not None else self._n
        params['r'] = params['r'] / (2 * sin(pi / n)) if params['r'] is not None else self._r
        if super(Prism, self).change(params):
            self.__get_polygonal_mesh(Vertex([0., self._h, 0]))
            self.__get_sphere()

    def transform(self, matrix, rotate=False):
        super(Prism, self).transform(matrix, rotate)
        self.__get_sphere()