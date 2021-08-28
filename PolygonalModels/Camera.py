import copy

import numpy as np

from TransformMatrix import TransformMatrix
from Vertex import Vertex


class Camera:
    def __init__(self, width, height, pos=np.array([0., 0., 0.]), up=np.array([0., 1., 0.]), center=np.array([0., 0., -1.]), fov=90, near=3, far=200):
        self.__eye = pos
        self.__up = up
        self.__lookat = center
        self.__fov = fov
        self.__z_near = near
        self.__z_far = far
        self.__aspect_ratio = width / height
        self.__width = width
        self.__height = height
        self.__projection_matrix = TransformMatrix.ProjectionMatrix(fov, self.__aspect_ratio, near, far)
        print("projection matrix is: ", self.__projection_matrix)
        print("lookat matrix is: ", self.lookat())
        print("dot (l x p): ", self.lookat().dot(self.__projection_matrix))

    def lookat(self):
        w = self.__lookat - self.__eye
        # w = w[:3]
        w = w / np.linalg.norm(w) if np.linalg.norm(w) != 0 else np.array([0., 0., 0.])
        u = - np.cross(w, self.__up)
        u = u / np.linalg.norm(u) if np.linalg.norm(u) != 0 else np.array([0., 0., 0.])
        v = np.cross(w, u)
        v = v / np.linalg.norm(v) if np.linalg.norm(v) != 0 else np.array([0., 0., 0.])
        minv = np.array([[1. if i == j else 0. for i in range(4)] for j in range(4)])
        # tr = np.array([[1 if i == j else 0 for i in range(4)] for j in range(4)])
        x0 = - np.dot(self.__eye, u)
        y0 = - np.dot(self.__eye, v)
        z0 = - np.dot(self.__eye, w)

        for i in range(3):
            minv[i][0] = u[i]
            minv[i][1] = v[i]
            minv[i][2] = w[i]
            # tr[i][3] = -self.__center[i]
        minv[3][0] = x0
        minv[3][3] = y0
        minv[3][2] = z0
        minv[3][3] = 1
        # modelview = np.dot(minv, tr)
        # print("________________\nlookat matrix:\n", minv, "\n")
        return minv

    def get_projection(self, vertex):
        vertex.y *= -1
        # return self.__orthogonal_projection(vertex)
        return self.__perspective_projection(vertex)

    def __perspective_projection(self, vertex):
        # matrix = self.viewport().dot(self.__projection_matrix.dot(self.lookat()))
        # print("__________________\nvertex: ", vertex.transform_vector)
        # l = vertex.transform(self.lookat())
        # print("using lookat (coordinates in camera view): ", l.transform_vector)
        # l = l.transform(self.__projection_matrix)
        # print("using projection matrix: ", l.transform_vector)
        # l = l.transform(self.viewport())
        # print("viewport he: ", l.transform_vector)


        # matrix = self.__projection_matrix.dot(self.lookat())
        # print("proj m = ", self.__projection_matrix)
        # print("lookat = ", self.lookat())
        # m = self.lookat().dot(self.__projection_matrix)
        # print("m= ", m)

        matrix = self.lookat().dot(self.__projection_matrix)
        # matrix = self.__projection_matrix.dot(self.viewport())
        # matrix = self.viewport()
        # v = vertex.transform(matrix)
        v = vertex.transform(matrix)
        # l = vertex.transform(m)
        # print("initial data: ", vertex.transform_vector)
        # print("transformed: ", v.transform_vector, "\n")
        # print("viewport ", self.viewport(v.x, v.y))
        v = v.transform(self.viewport(v.x, v.y))
        # print("after viewport: ", v.transform_vector)

        vertex.y *= -1
        v.make_decart_coords()
        # print("transformed2: ", v.transform_vector, "\n")
        return v


    def __orthogonal_projection(self, vertex):
        return copy.deepcopy(vertex)

    def viewport(self, x, y):
        mat = TransformMatrix.MoveMatrix(dx=x + (self.__width / 2), dy=y + (self.__height / 2))
        # mat = TransformMatrix.ScaleMatrix()
        mat[0][0] = self.__width / 2
        mat[1][1] = self.__height / 2
        mat[2][2] = 1
        # mat = np.array([[0 for i in range(TransformMatrix.dimensions)] for j in
        #                 range(TransformMatrix.dimensions)])

        # mat[3][0] = self.__width / 2
        # mat[3][1] = self.__height / 2

        return mat

    # def move_x(self, distance):.
