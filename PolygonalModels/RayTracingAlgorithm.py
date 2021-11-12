import numpy as np
from numba import jit

from Ray import Ray


class RayTracingAlgorithm:
    def __init__(self, width, height, cam):
        self.__width = width
        self.__height = height
        self.__color_buf = np.array([[np.array([0.9, 0.9, 0.9, 1], dtype=np.float32)] * height] * width)
        self.__camera = cam


    def sort_vertices(self, vertices):
        s = []
        print("verts = ", [v.vector for v in vertices])
        tmp = vertices[0]
        for i in vertices:
            tmp = i if i.y >= tmp.y and i.x <= tmp.x else tmp
        s.append(tmp)
        vertices.remove(tmp)
        if abs(tmp.x - vertices[0].x) < 1e-5 or abs(tmp.x -vertices[1].x) < 1e-5:
            left = vertices[0] if vertices[0].x < vertices[1].x else vertices[1]
        else:
            k1 = (vertices[0].y - tmp.y) / (vertices[0].x - tmp.x)
            k2 = (vertices[1].y - tmp.y) / (vertices[1].x - tmp.x)
            left = vertices[0] if k1 > k2 else vertices[1]
        vertices.remove(left)
        s.append(left)
        s.extend(vertices)
        print("sorted = ", [v.vector for v in s])
        return s


    def start_algorithm(self, objects, light):
        self.__color_buf = np.array([[np.array([0.9, 0.9, 0.9, 1], dtype=np.float32)] * self.__height] * self.__width)
        # width, height = self.__camera.get_near_sizes()
        # f_y = int(-height // 2)
        # s_y = -f_y + 1
        f_y = 0
        s_y = self.__height
        # f_y = 0
        # s_y = self.__height
        # f_x = int(-width // 2)
        # s_x = -f_x + 1
        f_x = 0
        s_x = self.__width
        # f_x = 0
        # s_x = self.__width
        # delta_w = self.__width // 2
        # delta_h = self.__height // 2
        # delta_w = 10
        # delta_h = 10
        # cur_coords = np.array([0., 0., 0., 0])
        for poly in objects[0].polygons:
            self.sort_vertices([objects[0].vertices[i] for i in poly])
        for y in np.arange(f_y, s_y):
            for x in np.arange(f_x, s_x):
                if x == 150 and y == 70:
                    print("Heyo")
                ray = self.__camera.cast_ray(np.array([x, y, 1., 1.]))
                self.__color_buf[x][y] = ray.trace(objects, light)
            # print(y)

    def apply(self, drawer):
        drawer.apply(self.__color_buf)
