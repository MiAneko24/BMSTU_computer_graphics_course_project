import numpy as np

from math import sqrt


class Sphere:
    def __init__(self):
        self.__radius = 0
        self.__center = []
        # self.__transform_mat = TransformMatrix.ScaleMatrix()

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, r):
        self.__radius = r
        # TODO: add radius check in setter

    @property
    def center(self):
        return self.__center

    @center.setter
    def center(self, cent):
        self.__center = cent


    def is_intersected(self, O, D):
        # TODO: add Ray class & intersection wth sphere algorithm. Maybe create an intersection method in ray itself?
        OS = O - self.center
        a = D.dot(D)
        b = 2 * OS.dot(D)
        c = OS.dot(OS) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        return discriminant >= 0
        # t1 = (-b + sqrt(discriminant)) / (2 * a)
        # t2 = (-b - sqrt(discriminant)) / (2 * a)

