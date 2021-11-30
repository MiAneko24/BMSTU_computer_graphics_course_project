import copy

import numpy as np


class Vertex:
    def __init__(self, coordinates=None):
        self.__eps = 1e-5
        if coordinates is None:
            self.__vector = np.array([0.0 for i in range(4)], dtype=np.float64)
        else:
            coordinates = list(coordinates)
            coordinates.append(1)
            coordinates = [c if abs(c) > self.__eps else 0 for c in coordinates]
            self.__vector = np.array(coordinates, dtype=np.float64)
        self.__normal = np.array([0.0, 0.0, 0.0])
        self.__intense = 0.0

    @property
    def x(self):
        return self.__vector[0]

    @x.setter
    def x(self, x_new):
        self.__vector[0] = x_new

    @property
    def y(self):
        return self.__vector[1]

    @y.setter
    def y(self, y_new):
        self.__vector[1] = y_new

    @property
    def z(self):
        return self.__vector[2]

    @z.setter
    def z(self, z_new):
        self.__vector[2] = z_new

    @property
    def transform_vector(self):
        return np.array(self.__vector)

    @transform_vector.setter
    def transform_vector(self, v):
        if v.size == 4:
            self.__vector = v
        # else raise error

    def transform(self, mat):
        vertex = copy.deepcopy(self)
        mat = copy.deepcopy(mat)
        vertex.transform_vector = self.__vector.dot(mat)

        if vertex.transform_vector[-1] != 0:
            vertex.transform_vector /= vertex.transform_vector[-1]
        mat = mat[:3, :3]
        # norm = list(self.__normal)
        # norm.append(1)
        # vertex.normal = np.linalg.inv(mat.transpose()).dot(np.array(self.__normal))
        vertex.normal = self.__normal.dot(np.linalg.inv(mat).transpose())
        return vertex

    def make_decart_coords(self):
        if self.transform_vector[-1] != 0:
            self.transform_vector /= self.transform_vector[-1]
        if self.z != 0:
            self.x /= self.z
            self.y /= self.z

    @property
    def vector(self):
        return self.__vector[:3]

    @vector.setter
    def vector(self, v):
        if v.size == 3:
            v = list(v)
            v.append(self.__vector[3])
            self.__vector = np.array(v)
        else:
            print("I'm pretty pretty sry")

    def get_normal(self, normals):
        print(normals)
        for i in normals:
            self.__normal = self.__normal + i
        # try/catch?
        self.__normal /= len(normals)
        self.__normal /= np.linalg.norm(self.__normal)

    @property
    def normal(self):
        return self.__normal

    @normal.setter
    def normal(self, n):
        self.__normal = n

    def __str__(self):
        return self.__vector

    @property
    def intense(self):
        return self.__intense

    @intense.setter
    def intense(self, i):
        self.__intense = i