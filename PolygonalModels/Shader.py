import copy

import numpy as np

from PolygonalModels.Vertex import Vertex


class Shader:
    def __init__(self, z_buf, src, cam, width, height):
        self._eps = 1e-5
        self._width = width
        self._height = height
        self._z_buf = z_buf
        self.__src = src
        self.__cam = cam

    # def sort_vertices(self, vertices):
    #     for i in range(3):
    #         for j in range(3 - i - 1):
    #             if round(vertices[j].y) > round(vertices[j + 1].y) or (round(vertices[j].y) == round(vertices[j + 1].y) and vertices[j].x > vertices[j + 1].x):
    #                 vertices[j], vertices[j + 1] = vertices[j + 1], vertices[j]
    #     return vertices

    def sign(self, num):
        return 0 if abs(num) < self._eps else -1 if num < 0 else 1

    def sort_vertices(self, vertices):
        s = []
        # print("verts = ", [v.vector for v in vertices])
        tmp = vertices[0]
        for i in vertices:
            tmp = i if (i.y > tmp.y and abs(i.y - tmp.y) > self._eps) or (abs(i.y - tmp.y) < self._eps and i.x <= tmp.x) else tmp
        s.append(tmp)
        vertices.remove(tmp)
        if abs(tmp.x - vertices[0].x) < self._eps or abs(tmp.x -vertices[1].x) < self._eps:
            left = vertices[0] if vertices[0].x < vertices[1].x else vertices[1]
        else:
            k1 = (vertices[0].y - tmp.y) / (vertices[0].x - tmp.x)
            k2 = (vertices[1].y - tmp.y) / (vertices[1].x - tmp.x)
            s_k1 = self.sign(k1)
            s_k2 = self.sign(k2)
            first_is_left = (k1 > k2 and ((s_k1 > 0 and s_k2 <= 0) or (s_k1 <= 0 and s_k2 > 0))) or (k1 < k2 and (s_k1 == s_k2 == 1 or s_k1 == s_k2 == -1 or (s_k1 == -1 and s_k2 == 0) or (s_k2 == -1 and s_k1 == 0)))
            left = vertices[0] if first_is_left else vertices[1]
        vertices.remove(left)
        s.append(left)
        s.extend(vertices)
        # print("sorted = ", [v.vector for v in s])
        return s

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
            # if len(polygons) > 3:
            #     vertices = polygons[2]
            # vertices = polygons[1]
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
                # print("intense = ", vertices[i].intense, ", shadow = ", obj.get_shadow_color(self.__src))
                vertices[i] = self.__cam.get_projection(vertices[i])
                # print(vertices[-1].intense)
                # if vertices[i].intense > 1:
                #     vertices[i].intense = 1
                # elif vertices[i].intense < 0:
                #     vertices[i].intense = 0
                # break

            vertices = self.sort_vertices(copy.deepcopy(vertices))
            # m = self.sort_vertices(m)
            # for v in m:
            #     print("f_sort: v[0] = ", v.vector, end='')
            # print()

            self.halfway(vertices)

            # if right.y < y_max:  # OK CODDE
            #     self.halfway(vertices, right, left, obj.color[:3], back=True, left_const_delta=left_const_d)
            # break

    def count_sides_steps(self, vertices, y_cur, it = 0):
        delta_right = Vertex()
        delta_left = Vertex()
        if it == 0:
            vertices = self.sort_vertices(vertices)
        # for v in vertices:
        #     print("s_sort: v[0] = ", v.vector, end='')
        # print()
        if y_cur < vertices[1].y:
            vertices[0], vertices[2] = vertices[2], vertices[0]
        elif y_cur < vertices[2].y:
            vertices[0], vertices[1] = vertices[1], vertices[0]
        # print("vert[0] = ", vertices[0].vector,", vert[1] = ", vertices[1].vector, ", vert[2] = ", vertices[2].vector)
        # if back:
        dly = (round(vertices[0].y) - round(vertices[1].y)) * -1
        delta_left.x = (vertices[0].x - vertices[1].x) / dly if abs(dly) > self._eps else 1
        delta_left.y = -1 if abs(dly) > self._eps else 0
        delta_left.z = (vertices[0].z - vertices[1].z) / dly if abs(dly) > self._eps else 1
        dry = (round(vertices[0].y) - round(vertices[2].y)) * -1
        delta_right.x = (vertices[0].x - vertices[2].x) / dry if abs(dry) > self._eps else 1
        delta_right.y = -1 if abs(dry) > self._eps else 0
        delta_right.z = (vertices[0].z - vertices[2].z) / dry if abs(dry) > self._eps else 1
        print("delta left = ", delta_left.vector, ", delta_right = ", delta_right.vector)
        return delta_left, delta_right, vertices

    def halfway(self, vertices):
        right = copy.deepcopy(vertices[0])  # OK CODE
        left = copy.deepcopy(vertices[0])
        delta_left, delta_right, vertices = self.count_sides_steps(vertices, round(right.y) - 1)

        if vertices[1].y > vertices[2].y:
            mid_y = round(vertices[1].y)
            min_y = round(vertices[2].y)
        else:
            mid_y = round(vertices[2].y)
            min_y = round(vertices[1].y)
            # if not left_const_delta and abs(vertices[0].y - vertices[1].y) > self._eps:
            #     left = copy.deepcopy(vertices[1])
            #     delta_right, delta_left = delta_left, delta_right
            #     swap = True
            # else:
            #     right = copy.deepcopy(vertices[1])
            # vertices = [vertices[(i + 1) % len(vertices)] for i in range(len(vertices))]
            # if abs(vertices[2].y - left.y) < abs(vertices[0].y - left.y):
            #     vertices[0], vertices[2] = vertices[2], vertices[0]
        # else:
        #     dly = round(vertices[0].y - vertices[1].y)
        #     delta_left.x = (vertices[0].x - vertices[1].x) / dly if abs(dly) > self._eps else 1
        #     delta_left.y = 1 if abs(dly) > self._eps else 0
        #     delta_left.z = (vertices[0].z - vertices[1].z) / dly if abs(dly) > self._eps else 1
        #     dry = (vertices[0].y - vertices[2].y)
        #     delta_right.x = (vertices[0].x - vertices[2].x) / dry if abs(dry) > self._eps else 1
        #     delta_right.y = 1 if abs(dry) > self._eps else 0
        #     delta_right.z = (vertices[0].z - vertices[2].z) / dry if abs(dry) > self._eps else 1

        # if not back and delta_left.x > delta_right.x:
        #     right, left = left, right
        #     delta_left, delta_right = delta_right, delta_left
        #     left_const_delta = True
        #     swap = True

        cycle = False
        y_start = round(left.y)
        if mid_y == y_start or (abs(vertices[1].y) == abs(vertices[2].y) and vertices[0].y < left.y):
            left = copy.deepcopy(vertices[1])
            right = copy.deepcopy(vertices[2])
            # delta_left, delta_right = delta_right, delta_left
            # if vertices[0].y < left.y:
            min_y = round(vertices[0].y)
        # print("start_y = ", y_start, ", mid_y = ", mid_y, ", min_y = ", min_y)
        # y_end = round(vertices[1].y)
        # if y_start > self._height or y_end < 0:
        #     y_start = y_end
        # else:
        #     y_start = max(y_start, 0)
        #     y_end = min(y_end, round(self._height))
        # if y_start < 0:
        #     tmp = right.vector + delta_right.vector * - y_start
        #     right.vector = tmp
        #     temp = left.vector + delta_left.vector * - y_start
        #     left.vector = temp
        #     y_start = 0
        for y in range(y_start, min_y, -1):
            cycle = True
            right.intense, left.intense = self.get_intenses(vertices, left.y)

            x_start = round(left.x-1)
            x_end = round(right.x + 1)
            delta_z = (right.z - left.z) / (x_end - x_start) if x_end != x_start else 0
            z = left.z
            # if x_start > self._width or x_end < 0:
            #     x_start = x_end
            # else:
            #     x_start = max(0, x_start)
            #     x_end = min(round(self._width), x_end)
            for x in range(x_start, x_end):
                if self._z_buf.check_pixel_on_scene([x, y, z]):
                    z += delta_z
                    t = (right.x - x) / (right.x - left.x) if abs(right.x - left.x) > self._eps else right.x - x
                    i = (1 - t) * right.intense + t * left.intense
                    # i = i if i < 1 else 1
                    # i = i if i > 0 else 0
                    # print("changed (", x, ";, ", y, ")")
                    # print("i = ", i, ", add_color = ", add_color)
                    self._z_buf.analyse_pixel([x, y, z], i)
            if y == mid_y:
                delta_left, delta_right, vertices = self.count_sides_steps(vertices, y - 1)
            tmp = right.vector + delta_right.vector
            right.vector = tmp
            temp = left.vector + delta_left.vector
            left.vector = temp


    def multiply_color(self, color, i):
        for j in range(color.shape[0]):
            color[j] = round(color[j] * i)
        return color

    def get_intenses(self, vertices, y):
        # if back:
        #     start = vertices[1]
        #     left = vertices[2] if not swap else vertices[0]
        #     right = vertices[0] if not swap else vertices[2]
        # else:
        #     start = vertices[0]
        #     left = vertices[1] if not swap else vertices[2]
        #     right = vertices[2] if not swap else vertices[1]
        start = vertices[0]
        left = vertices[1]
        right = vertices[2]
        t1 = (y - right.y) / (start.y - right.y) if abs(start.y - right.y) > self._eps else y - right.y
        t2 = (y - left.y) / (start.y - left.y) if abs(start.y - left.y) > self._eps else y - left.y
        right_intense = (1 - t1) * right.intense + t1 * start.intense
        left_intense = (1 - t2) * left.intense + t2 * start.intense
        return right_intense, left_intense

