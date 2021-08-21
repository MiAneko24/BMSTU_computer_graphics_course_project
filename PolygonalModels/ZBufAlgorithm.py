import numpy as np
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene
from numpy import inf
import copy

from Vertex import Vertex

eps = 0.5

class ZBufAlgorithm:
    def __init__(self, scene, brush, src, cam):
        self.__z_buf = []
        self.__color_buf = []
        self.__scene = scene
        self.clear()
        self.__src = src
        self.__brush = brush
        self.__cam = cam
        self.__borders = [round(self.__scene.width()), round(self.__scene.height())]

    def sort_vertices(self, vertices):
        for i in range(2):
            for j in range(3 - i - 1):
                if vertices[j].y > vertices[j + 1].y or (vertices[j].y == vertices[j + 1].y and vertices[j].x > vertices[j + 1].x):
                    vertices[j], vertices[j + 1] = vertices[j + 1], vertices[j]
        return vertices

    def clear(self):
        self.__z_buf = [[1. for i in range(round(self.__scene.height()))] for j in range(round(self.__scene.width()))]
        self.__color_buf = [[[255, 255, 255] for i in range(round(self.__scene.height()))] for j in
                            range(round(self.__scene.width()))]


    def visit(self, obj):
        self.object_processing(obj)

    def draw(self):

        for i in range(round(self.__scene.width())): #OK CODE
            for j in range(round(self.__scene.height())):
                color = self.__color_buf[i][j]
                color = QColor(color[0], color[1], color[2])
                # self.__brush.setColor(color)
                self.__scene.addLine(i, j, i, j, QPen(color))
        print("READY")

    def object_processing(self, obj):
        for polygon in obj.polygons:
        # for p in range(3):
            vertices = []
            # polygon = obj.polygons[p]
            for i in range(len(polygon)):
                vertices.append(self.__cam.get_projection(obj.vertices[polygon[i]]))
                l = vertices[-1].vector - self.__src.coordinates.vector
                l = l / np.linalg.norm(l)
                # vertices[-1].normal *= -1
                vertices[-1].intense = self.__src.diffuse_light * (vertices[-1].normal.dot(l) * obj.reflectivity) + 0.3
                # print(vertices[-1].vector)
                if vertices[-1].intense > 1:
                    vertices[-1].intense = 1
                elif vertices[-1].intense < 0:
                    vertices[-1].intense = 0

            vertices = self.sort_vertices(vertices)
            y_max = vertices[-1].y

            for i in range(3):
                self.__scene.addLine(vertices[i - 1].x, vertices[i - 1].y, vertices[i].x, vertices[i].y,
                                     QPen(QColor(255, 0, 0)))

            right = copy.deepcopy(vertices[0])  # OK CODE
            left = copy.deepcopy(vertices[0])
            right, left, left_const_d = self.halfway(vertices, right, left, obj.color)

            if right.y < y_max:  # OK CODDE
                self.halfway(vertices, right, left, obj.color, back=True, left_const_delta=left_const_d)
            # break

    def halfway(self, vertices, right, left, color, back=False, left_const_delta=False):
        delta_right = Vertex()
        delta_left = Vertex()
        swap = False
        if back:
            dly = (vertices[2].y - vertices[0].y)
            delta_left.x = (vertices[2].x - vertices[0].x) / dly if dly != 0 else 1
            delta_left.y = 1 if dly != 0 else 0
            delta_left.z = (vertices[2].z - vertices[0].z) / dly if dly != 0 else 1
            dry = (vertices[2].y - vertices[1].y)
            delta_right.x = (vertices[2].x - vertices[1].x) / dry if dry != 0 else 1
            delta_right.y = 1 if dry != 0 else 0
            delta_right.z = (vertices[2].z - vertices[1].z) / dry if dry != 0 else 1
            if not left_const_delta and not vertices[0].y == vertices[1].y:
                left = copy.deepcopy(vertices[1])
                delta_right, delta_left = delta_left, delta_right
                swap = True
            else:
                right = copy.deepcopy(vertices[1])
            vertices = [vertices[(i + 1) % len(vertices)] for i in range(len(vertices))]
            if abs(vertices[2].y - left.y) < abs(vertices[0].y - left.y):
                vertices[0], vertices[2] = vertices[2], vertices[0]
        else:
            dly = round(vertices[0].y - vertices[1].y)
            delta_left.x = (vertices[0].x - vertices[1].x) / dly if dly != 0 else 1
            delta_left.y = 1 if dly != 0 else 0
            delta_left.z = (vertices[0].z - vertices[1].z) / dly if dly != 0 else 1
            dry = (vertices[0].y - vertices[2].y)
            delta_right.x = (vertices[0].x - vertices[2].x) / dry if dry != 0 else 1
            delta_right.y = 1 if dry != 0 else 0
            delta_right.z = (vertices[0].z - vertices[2].z) / dry if dry != 0 else 1

        if not back and delta_left.x > delta_right.x:
            right, left = left, right
            delta_left, delta_right = delta_right, delta_left
            left_const_delta = True
            swap = True

        cycle = False
        y_start = left.y
        for y in range(round(y_start), round(vertices[1].y)):
            cycle = True
            right.intense, left.intense = self.get_intenses(vertices, left.y, swap, back)

            delta_z = (right.z - left.z) / (right.x - left.x) if right.x != left.x else 0
            z = left.z
            for x in range(round(left.x), round(right.x)):
                z += delta_z
                if 0 < x < self.__borders[0] and 0 < y < self.__borders[1] and \
                        self.__z_buf[x][y] >= z >= 0:
                    self.__z_buf[x][y] = z
                    t = (right.x - x) / (right.x - left.x)
                    i = (1 - t) * right.intense + t * left.intense
                    i = i if i < 1 else 1
                    i = i if i > 0 else 0
                    # print("changed (", x, ";, ", y, ")")
                    # print("i = ", i, ", color = ", color)
                    self.__color_buf[x][y] = i * color

            tmp = right.vector + delta_right.vector
            right.vector = tmp
            temp = left.vector + delta_left.vector
            left.vector = temp
        if not cycle:
            if vertices[0].x <= vertices[1].x:
                left = copy.deepcopy(vertices[0])
                right = copy.deepcopy(vertices[1])
            else:
                left = copy.deepcopy(vertices[1])
                right = copy.deepcopy(vertices[0])

        return right, left, left_const_delta

    def get_intenses(self, vertices, y, swap, back):
        if back:
            start = vertices[1]
            left = vertices[2] if not swap else vertices[0]
            right = vertices[0] if not swap else vertices[2]
        else:
            start = vertices[0]
            left = vertices[1] if not swap else vertices[2]
            right = vertices[2] if not swap else vertices[1]

        t1 = (y - right.y) / (start.y - right.y)
        t2 = (y - left.y) / (start.y - left.y)
        right_intense = (1 - t1) * right.intense + t1 * start.intense
        left_intense = (1 - t2) * left.intense + t2 * start.intense
        return right_intense, left_intense
