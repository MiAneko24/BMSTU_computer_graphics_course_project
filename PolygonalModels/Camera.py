import copy

import numpy as np

from TransformMatrix import TransformMatrix
from Vertex import Vertex


class Camera:
    def __init__(self, width, height, pos=np.array([0, 0, 0]), up=np.array([0, 1, 0]), center=np.array([0, 0, -1]), fov=60, near=1, far=1000):
        self.__position = pos
        self.__up = up
        self.__center = center
        self.__fov = fov
        self.__z_near = near
        self.__z_far = far
        self.__aspect_ratio = width / height
        self.__width = width
        self.__height = height
        self.__projection_matrix = TransformMatrix.ProjectionMatrix(fov, self.__aspect_ratio, near, far)

    def lookat(self):
        direction = self.__position - self.__center
        z = direction / np.linalg.norm(direction) if np.linalg.norm(direction) != 0 else np.array([0, 0, 0])
        x = np.cross(self.__up, z)
        x = x / np.linalg.norm(x) if np.linalg.norm(x) != 0 else np.array([0, 0, 0])
        y = np.cross(z, x)
        y = y / np.linalg.norm(y) if np.linalg.norm(y) != 0 else np.array([0, 0, 0])
        minv = np.array([[1 if i == j else 0 for i in range(4)] for j in range(4)])
        tr = np.array([[1 if i == j else 0 for i in range(4)] for j in range(4)])
        for i in range(3):
            minv[0][i] = x[i]
            minv[1][i] = y[i]
            minv[2][i] = z[i]
            tr[i][3] = -self.__center[i]
        modelview = np.dot(minv, tr)
        return modelview

    def get_projection(self, vertex):
        vertex.y *= -1
        # return self.__orthogonal_projection(vertex)
        return self.__perspective_projection(vertex)

    def __perspective_projection(self, vertex):
        # matrix = self.viewport().dot(self.__projection_matrix.dot(self.lookat()))
        prom = vertex.transform(self.__projection_matrix)
        # matrix = self.viewport().dot(self.__projection_matrix)
        matrix = self.viewport()
        v = vertex.transform(matrix)
        vertex.y *= -1
        return v

    def __orthogonal_projection(self, vertex):
        return copy.deepcopy(vertex)

    def viewport(self):
        mat = np.array([[1 if i==j else 0 for i in range(TransformMatrix.dimensions)] for j in range(TransformMatrix.dimensions)])
        mat[0][3] = self.__width / 2
        mat[1][3] = self.__height / 2
        return mat

    # def move_x(self, distance):.
