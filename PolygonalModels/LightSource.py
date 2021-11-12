import numpy as np


class LightSource:
    def __init__(self, coords, diffuse_light=np.array([1., 1, 1, 1.]), specular_light=np.array([1., 1, 1, 1.]), ambient_light=np.array([1., 1, 1, 1.])):
        self.__coordinates = coords
        self.__diffuse_light = diffuse_light
        self.__specular_light = specular_light
        self.__ambient = ambient_light

    @property
    def coordinates(self):
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, coords):
        self.__coordinates = coords

    @property
    def specular_light(self):
        return self.__specular_light

    @specular_light.setter
    def specular_light(self, sl):
        self.__specular_light = sl

    @property
    def diffuse_light(self):
        # return self.__diffuse_light * self.color

        return self.__diffuse_light

    @diffuse_light.setter
    def diffuse_light(self, dl):
        self.__diffuse_light = dl

    def transform_position(self, matrix):
        self.__coordinates = self.__coordinates.dot(matrix)

    @property
    def ambient_light(self):
        return self.__ambient

    @ambient_light.setter
    def ambient_light(self, value):
        self.__ambient = value
