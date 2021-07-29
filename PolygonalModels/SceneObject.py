from math import cos, sin

import numpy as np
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex


class SceneObject:

    def __init__(self):
        self.__polygons = np.array([])
        self.__vertices = np.array([])
        self.__normals = np.array([])
        self.__sphere = Sphere()
        self.__color = np.array([0.0, 0.0, 0.0])
        self.__transparency = 0.0
        self.__specular = 0.0
        self.__reflectivity = 0.0
        self.__refraction = 0.0
        self.__transform_matrix = np.array([[1.0 if i == j else 0.0 for i in range(4)] for j in range(4)])

    @property
    def reflectivity(self):
        return self.__reflectivity

    @reflectivity.setter
    def reflectivity(self, rf):
        self.__reflectivity = rf

    @property
    def refraction(self):
        return self.__refraction

    @refraction.setter
    def refraction(self, rf):
        self.__refraction = rf

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, cl):
        self.__color = cl

    @property
    def transparency(self):
        return self.__transparency

    @transparency.setter
    def transparency(self, vs):
        if 0 <= vs <= 1:
            self.__transparency = vs
        else:
            raise ObjectException()

    @property
    def specular(self):
        return self.__specular

    @specular.setter
    def specular(self, sp):
        if 0 <= sp <= 1:
            self.__specular = sp
        else:
            raise ObjectException()

    @property
    def polygons(self):
        return self.__polygons

    @polygons.setter
    def polygons(self, pol):
        if pol.size > 0:
            self.__polygons = pol
        else:
            raise ObjectException()

    @property
    def vertices(self):
        vertices = []
        single_mat = np.array([[1.0 if i == j else 0.0 for i in range(4)] for j in range(4)])
        if not np.allclose(single_mat, self.__transform_matrix):
            for vertex in self.__vertices:
                vertices.append(vertex.transform(self.__transform_matrix))
        else:
            vertices = self.__vertices
        return vertices

    @vertices.setter
    def vertices(self, vertex):
        self.__vertices = vertex
        # TODO: add check params in setters

    @property
    def normals(self):
        return self.__normals

    @normals.setter
    def normals(self, norms):
        self.__normals = norms

    @property
    def sphere(self):
        return self.__sphere

    @sphere.setter
    def sphere(self, sp):
        self.__sphere = sp

    def calculate_normals(self):
        center = np.array([0, 0, 0])
        for i in range(len(self.vertices)):
            center = center + np.array(self.vertices[i].vector)
        center = center / len(self.vertices)
        normals = []
        for poly in self.__polygons:
            first_edge = self.vertices[poly[1]].vector - self.vertices[poly[0]].vector
            second_edge = self.vertices[poly[2]].vector - self.vertices[poly[0]].vector
            normals.append(np.cross(first_edge, second_edge))
            test_vector = center - self.vertices[poly[0]].vector
            if np.dot(normals[-1], test_vector) > 0:
                normals[-1] *= -1
            normals[-1] /= np.linalg.norm(normals[-1])
        self.normals = np.array(normals)
        for i in range(len(self.vertices)):
            normals = []
            for j in range(len(self.polygons)):
                if i in self.polygons[j]:
                    normals.append(np.array(self.normals[j]))
            self.vertices[i].get_normal(normals)

    def transform(self, matrix):
        self.__transform_matrix = self.__transform_matrix.dot(matrix)


class ObjectException(Exception):
    def __init__(self, message="Пустая модель недопустима"):
        self.message = message
        super().__init__(self.message)
