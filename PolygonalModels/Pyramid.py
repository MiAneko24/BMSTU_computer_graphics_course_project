from math import sin, pi, cos

import numpy as np

from ObjectType import ObjectType
from PolygonalModels.SceneObject import SceneObject
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex


class Pyramid(SceneObject):

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
        sphere.radius = (self._h ** 2 + self._r ** 2) / (2 * self._h)
        so = self.vertices[1].vector - self.vertices[0].vector
        sphere.center = (sphere.radius * so / self._h) + self.vertices[0].vector
        self.sphere = sphere

    def __get_polygonal_mesh(self, up):
        down = Vertex([up.x, up.y - self._h, up.z])
        # vertices = [Vertex([120.0, 120.0, 30.0]), Vertex([up.x, up.y, up.z]), Vertex([-100.0, -100.0, 0.0])]
        # polygons = [[0, 1, 2]]
        polygons = []
        vertices = [up, down]
        if self._h < 0:
            self._h *= -1
        alpha = 2 * pi / self._n

        for i in range(self._n):
            vertices.append(Vertex([down.x + self._r * cos(alpha * i), down.y, down.z + self._r * sin(alpha * i)]))
        for i in range(2):
            for j in range(2, len(vertices) - 1):
                polygons.append([i, j, j + 1])
            polygons.append([i, len(vertices) - 1, 2])
        self.vertices = np.array(vertices)
        self.polygons = np.array(polygons)
        self.calculate_normals()

    def change(self, params):
        n = params['n'] if params['n'] is not None else self._n
        params['r'] = params['r'] / (2 * sin(pi/n)) if params['r'] is not None else self._r
        if super(Pyramid, self).change(params):
            self.__get_polygonal_mesh(Vertex([0., self._h, 0]))
            self.__get_sphere()
