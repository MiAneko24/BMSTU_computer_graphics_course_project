import numpy as np

from ObjectType import ObjectType
from PolygonalModels.SceneObject import SceneObject
from math import pi, cos, sin
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex


class Cone(SceneObject):
    def __init__(self, params):
        super().__init__(params)
        self.type = ObjectType.cone
        self.__get_polygonal_mesh(Vertex([0., self._h, 0.]))
        self.__get_sphere()

    def __get_sphere(self):
        sphere = Sphere()
        sphere.radius = (self._h ** 2 + self._r ** 2) / (2 * self._h)
        so = self.vertices[1].vector - self.vertices[0].vector
        sphere.center = (sphere.radius * so / self._h) + self.vertices[0].vector
        self.sphere = sphere

    def __get_polygonal_mesh(self, up):
        if self._n == 0:
            # кинуть ошибку!
            self._n = int(8 + self._r / 10)
        # n = 25
        down = Vertex([up.x, up.y - self._h, up.z])
        vertices = [up, down]
        if self._h < 0:
            self._h *= -1
        alpha = 2 * pi / self._n
        polygons = []
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
        if super(Cone, self).change(params):
            self.__get_polygonal_mesh(Vertex([0., self._h, 0]))
            self.__get_sphere()

