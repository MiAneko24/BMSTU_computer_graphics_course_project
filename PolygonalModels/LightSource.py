import numpy as np


class LightSource:
    def __init__(self, coords, diffuse_light=0.0, specular_light=0.0, color=np.array([255, 255, 255])):
        self.__coordinates = coords
        self.__diffuse_light = diffuse_light
        self.__specular_light = specular_light
        self.__color = color

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
        return self.__diffuse_light

    @diffuse_light.setter
    def diffuse_light(self, dl):
        self.__diffuse_light = dl

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, cl):
        self.__color = cl

    def transform_position(self, matrix):
        self.__coordinates = self.__coordinates.dot(matrix)