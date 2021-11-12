import copy

import numpy as np

from Vertex import Vertex


class Shader:
    def __init__(self, z_buf, src, cam, width, height):
        self._eps = 0.1
        self._width = width
        self._height = height
        self._z_buf = z_buf
        self.__src = src
        self.__cam = cam

    def sort_vertices(self, vertices):
        for i in range(3):
            for j in range(3 - i - 1):
                if round(vertices[j].y) > round(vertices[j + 1].y) or (round(vertices[j].y) == round(vertices[j + 1].y) and vertices[j].x > vertices[j + 1].x):
                    vertices[j], vertices[j + 1] = vertices[j + 1], vertices[j]
        return vertices

    def visit(self, obj):
        self.object_processing(obj)

    # def check_:
        #отсечение

    def get_polygons_with_vertices(self, obj):
        polygons = []
        for polygon in obj.polygons:
            vertices = []
            for i in range(len(polygon)):
                vertices.append(obj.vertices[polygon[i]])
            polygons.append(vertices)
        return polygons


    def object_processing(self, obj):
        polygons = self.__cam.get_polygons_projection(self.get_polygons_with_vertices(obj), obj.normals)

        for vertices in polygons:
            # vertices = polygons[6]
        # for j in range(len(obj.polygons)):
            # i = 7
            # polygon = obj.polygons[j]
            # for p in range(3):
            # vertices = []
            # polygon = obj.polygons[104]
            for i in range(len(vertices)):
                l = -vertices[i].vector + self.__src.coordinates.vector
                l = l / np.linalg.norm(l)
                # vertices[-1].normal *= -1
                vertices[i].intense = np.clip(0, self.__src.diffuse_light * vertices[i].normal.dot(l) * obj.diffuse, 1) + obj.get_shadow_color(self.__src)
                print("intense = ", vertices[i].intense, ", shadow = ", obj.get_shadow_color(self.__src))
                vertices[i] = self.__cam.get_projection(vertices[i])
                # print(vertices[-1].intense)
                # if vertices[i].intense > 1:
                #     vertices[i].intense = 1
                # elif vertices[i].intense < 0:
                #     vertices[i].intense = 0

            vertices = self.sort_vertices(vertices)
            y_max = vertices[-1].y

            right = copy.deepcopy(vertices[0])  # OK CODE
            left = copy.deepcopy(vertices[0])
            right, left, left_const_d = self.halfway(vertices, right, left, obj.color[:3])

            if right.y < y_max:  # OK CODDE
                self.halfway(vertices, right, left, obj.color[:3], back=True, left_const_delta=left_const_d)
            # break

    def halfway(self, vertices, right, left, color, back=False, left_const_delta=False):
        delta_right = Vertex()
        delta_left = Vertex()
        swap = False
        if back:
            dly = (vertices[2].y - vertices[0].y)
            delta_left.x = (vertices[2].x - vertices[0].x) / dly if abs(dly) > self._eps else 1
            delta_left.y = 1 if abs(dly) > self._eps else 0
            delta_left.z = (vertices[2].z - vertices[0].z) / dly if abs(dly) > self._eps else 1
            dry = (vertices[2].y - vertices[1].y)
            delta_right.x = (vertices[2].x - vertices[1].x) / dry if abs(dry) > self._eps else 1
            delta_right.y = 1 if abs(dry) > self._eps else 0
            delta_right.z = (vertices[2].z - vertices[1].z) / dry if abs(dry) > self._eps else 1
            if not left_const_delta and abs(vertices[0].y - vertices[1].y) > self._eps:
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
            delta_left.x = (vertices[0].x - vertices[1].x) / dly if abs(dly) > self._eps else 1
            delta_left.y = 1 if abs(dly) > self._eps else 0
            delta_left.z = (vertices[0].z - vertices[1].z) / dly if abs(dly) > self._eps else 1
            dry = (vertices[0].y - vertices[2].y)
            delta_right.x = (vertices[0].x - vertices[2].x) / dry if abs(dry) > self._eps else 1
            delta_right.y = 1 if abs(dry) > self._eps else 0
            delta_right.z = (vertices[0].z - vertices[2].z) / dry if abs(dry) > self._eps else 1

        if not back and delta_left.x > delta_right.x:
            right, left = left, right
            delta_left, delta_right = delta_right, delta_left
            left_const_delta = True
            swap = True

        cycle = False
        y_start = round(left.y)
        y_end = round(vertices[1].y)
        # if y_start > self._height or y_end < 0:
        #     y_start = y_end
        # else:
        #     y_start = max(y_start, 0)
        #     y_end = min(y_end, round(self._height))
        if y_start < 0:
            tmp = right.vector + delta_right.vector * - y_start
            right.vector = tmp
            temp = left.vector + delta_left.vector * - y_start
            left.vector = temp
            y_start = 0
        for y in range(y_start, y_end):
            cycle = True
            right.intense, left.intense = self.get_intenses(vertices, left.y, swap, back)

            delta_z = (right.z - left.z) / (right.x - left.x) if right.x != left.x else 0
            z = left.z
            x_start = round(left.x)
            x_end = round(right.x + 0.5)
            # if x_start > self._width or x_end < 0:
            #     x_start = x_end
            # else:
            #     x_start = max(0, x_start)
            #     x_end = min(round(self._width), x_end)
            for x in range(x_start, x_end):
                z += delta_z
                if self._z_buf.check_pixel_on_scene([x, y, z]):
                    t = (right.x - x) / (right.x - left.x) if abs(right.x - left.x) > self._eps else right.x - x
                    i = (1 - t) * right.intense + t * left.intense
                    # i = i if i < 1 else 1
                    # i = i if i > 0 else 0
                    # print("changed (", x, ";, ", y, ")")
                    # print("i = ", i, ", add_color = ", add_color)
                    self._z_buf.analyse_pixel([x, y, z], i)
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

    def multiply_color(self, color, i):
        for j in range(color.shape[0]):
            color[j] = round(color[j] * i)
        return color

    def get_intenses(self, vertices, y, swap, back):
        if back:
            start = vertices[1]
            left = vertices[2] if not swap else vertices[0]
            right = vertices[0] if not swap else vertices[2]
        else:
            start = vertices[0]
            left = vertices[1] if not swap else vertices[2]
            right = vertices[2] if not swap else vertices[1]

        t1 = (y - right.y) / (start.y - right.y) if abs(start.y - right.y) > self._eps else y - right.y
        t2 = (y - left.y) / (start.y - left.y) if abs(start.y - left.y) > self._eps else y - left.y
        right_intense = (1 - t1) * right.intense + t1 * start.intense
        left_intense = (1 - t2) * left.intense + t2 * start.intense
        return right_intense, left_intense

