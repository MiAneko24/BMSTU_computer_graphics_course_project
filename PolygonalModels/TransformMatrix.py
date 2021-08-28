from math import cos, sin, tan, radians

import numpy as np


class TransformMatrix:
    dimensions = 4

    def __init__(self):
        self.__matrix = [[0. for i in range(4)] for j in range(4)]
        self.__matrix[3][3] = 1

    @property
    def matrix(self):
        return self.__matrix

    @matrix.setter
    def matrix(self, mat):
        self.__matrix = mat

    @staticmethod
    def RotateMatrix(angle_x=0, angle_y=0, angle_z=0):
        angle_x = radians(angle_x)
        angle_y = radians(angle_y)
        angle_z = radians(angle_z)
        rotate_x = np.array([[1., 0., 0, 0],
                             [0, cos(angle_x), sin(angle_x), 0],
                             [0, -sin(angle_x), cos(angle_x), 0],
                             [0, 0, 0, 1]])
        rotate_y = np.array([[cos(angle_y), 0., -sin(angle_y), 0],
                             [0., 1, 0, 0],
                             [sin(angle_y), 0, cos(angle_y), 0],
                             [0, 0, 0, 1]])
        rotate_z = np.array([[cos(angle_z), sin(angle_z), 0, 0],
                             [-sin(angle_z), cos(angle_z), 0, 0],
                             [0., 0, 1, 0],
                             [0., 0, 0, 1]])
        return rotate_z.dot(np.dot(rotate_y, rotate_x))

    @staticmethod
    def MoveMatrix(dx=0, dy=0, dz=0):
        matrix = np.array([[1. if i == j else 0. for i in range(TransformMatrix.dimensions)] for j in range(TransformMatrix.dimensions)])
        matrix[3][0] = dx
        matrix[3][1] = dy
        matrix[3][2] = dz
        return matrix

    @staticmethod
    def ScaleMatrix(kx=1, ky=1, kz=1):
        matrix = np.array([[1. if i == j else 0. for i in range(TransformMatrix.dimensions)] for j in range(TransformMatrix.dimensions)])
        matrix[0][0] = kx
        matrix[1][1] = ky
        matrix[2][2] = kz
        return matrix

    @staticmethod
    def ProjectionMatrix(fov, ar, near, far):
        fov_rad = radians(fov)
        ky = 1 / tan(fov_rad / 2)
        kx = ky / ar
        return np.array([[kx, 0.0, 0., 0.],
                         [0., ky, 0., 0.],
                         [0., 0., far / (far - near), 1.],
                         [0., 0.,  - (far * near) / (far - near), 0]])
