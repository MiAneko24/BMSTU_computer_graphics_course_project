import numpy as np

from PolygonalModels.SceneObject import SceneObject
from math import pi, cos, sin
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex


class Cone(SceneObject):
    def __init__(self, r, h, up, color=None):
        super().__init__()
        self.__get_polygonal_mesh(r, h, Vertex(up))
        self.__get_sphere(r, h)
        if color is not None:
            self.color = color

    def __get_sphere(self, r, h):
        sphere = Sphere()
        sphere.radius = (h ** 2 + r ** 2) / (2 * h)
        so = self.vertices[1].vector - self.vertices[0].vector
        sphere.center = (sphere.radius * so / h) + self.vertices[0].vector
        self.sphere = sphere

    def __get_polygonal_mesh(self, r, h, up):
        n = int(8 + r / 10)
        # n = 25
        down = Vertex([up.x, up.y - h, up.z])
        vertices = [up, down]
        if h < 0:
            h *= -1
        alpha = 2 * pi / n
        polygons = []
        for i in range(n):
            vertices.append(Vertex([down.x + r * cos(alpha * i), down.y, down.z + r * sin(alpha * i)]))
        for i in range(2):
            for j in range(2, len(vertices) - 1):
                polygons.append([i, j, j + 1])
            polygons.append([i, len(vertices) - 1, 2])
        self.vertices = np.array(vertices)
        self.polygons = np.array(polygons)
        self.calculate_normals()
