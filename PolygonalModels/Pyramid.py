from math import sin, pi, cos

import numpy as np

from ObjectType import ObjectType
from PolygonalModels.SceneObject import SceneObject
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex


class Pyramid(SceneObject):

    def __init__(self, params):
        super().__init__(params[3:])
        self.type = ObjectType.pyramid
        a = params[0]
        h = params[1]
        n = params[2]
        up = np.array([0., h, 0.])
        r = a / (2 * sin(pi/n))

        self.__get_polygonal_mesh(r, n, h, Vertex(up))
        self.__get_sphere(r, h)

    def __get_sphere(self, r, h):
        sphere = Sphere()
        sphere.radius = (h ** 2 + r ** 2) / (2 * h)
        so = self.vertices[1].vector - self.vertices[0].vector
        sphere.center = (sphere.radius * so / h) + self.vertices[0].vector
        self.sphere = sphere

    def __get_polygonal_mesh(self, r, n, h, up):
        down = Vertex([up.x, up.y - h, up.z])
        # vertices = [Vertex([120.0, 120.0, 30.0]), Vertex([up.x, up.y, up.z]), Vertex([-100.0, -100.0, 0.0])]
        # polygons = [[0, 1, 2]]
        polygons = []
        vertices = [up, down]
        if h < 0:
            h *= -1
        alpha = 2 * pi / n

        for i in range(n):
            vertices.append(Vertex([down.x + r * cos(alpha * i), down.y, down.z + r * sin(alpha * i)]))
        for i in range(2):
            for j in range(2, len(vertices) - 1):
                polygons.append([i, j, j + 1])
            polygons.append([i, len(vertices) - 1, 2])
        self.vertices = np.array(vertices)
        self.polygons = np.array(polygons)
        self.calculate_normals()
