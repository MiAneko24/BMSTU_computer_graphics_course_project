import copy

import numpy as np


class Ray():
    def _get_nearest_obj(self, objects, O=None, D=None):
        if O is None:
            O = self.__origin
            D = self.__direction
        nearest_obj = None
        t_min = np.inf
        intersect_polygon_index = 0
        for obj in objects:
            t, polygon = obj.get_intersection(O, D)
            if 0 <= t < t_min:
                nearest_obj = obj
                t_min = t
                intersect_polygon_index = polygon
        return nearest_obj, t_min, intersect_polygon_index

    def __init__(self, start_point, end_point):
        self._eps = 1e-5
        if np.allclose(start_point, end_point):
            return
        self.__origin = start_point
        self.__direction = end_point - start_point
        self.__direction /= np.linalg.norm(self.__direction)
        self.__max_depth = 5

    def sort_vertices(self, vertices):
        s = []
        # print("verts = ", [v.vector for v in vertices])
        tmp = vertices[0]
        for i in vertices:
            tmp = i if i.y > tmp.y and i.x <= tmp.x else tmp
        s.append(tmp)
        vertices.remove(tmp)
        if abs(tmp.x - vertices[0].x) < self._eps or abs(tmp.x -vertices[1].x) < self._eps:
            left = vertices[0] if vertices[0].x < vertices[1].x else vertices[1]
        else:
            k1 = (vertices[0].y - tmp.y) / (vertices[0].x - tmp.x)
            k2 = (vertices[1].y - tmp.y) / (vertices[1].x - tmp.x)
            left = vertices[0] if k1 > k2 else vertices[1]
        vertices.remove(left)
        s.append(left)
        s.extend(vertices)
        # print("sorted = ", [v.vector for v in s])
        return s

        # for i in range(3):
        #     for j in range(3 - i - 1):
        #         if round(vertices[j].y) > round(vertices[j + 1].y) or (round(vertices[j].y) == round(vertices[j + 1].y) and vertices[j].x > vertices[j + 1].x):
        #             vertices[j], vertices[j + 1] = vertices[j + 1], vertices[j]
        # return vertices

    def calculate_color(self, norm, light_src, index, obj, light_dir):
        # light_dir = light_src.coordinates.vector - point
        # light_dir = light_dir / np.linalg.norm(light_dir)
        # vertices = self.sort_vertices([obj.vertices[i] for i in obj.polygons[index]])
        # for vert in vertices:
        # vertices = [obj.vertices[i] for i in obj.polygons[index]]
        # start = vertices[0]
        # right = vertices[1]
        # left = vertices[2]
        # t1 = (point[1] - right.y) / (start.y - right.y) if abs(start.y - right.y) > self._eps else point[1] - right.y
        # t2 = (point[1] - left.y) / (start.y - left.y) if abs(start.y - left.y) > self._eps else point[1] - left.y
        # right_norm = (1 - t1) * right.normal + t1 * start.normal
        # right_norm = right_norm / np.linalg.norm(right_norm)
        # left_norm = (1 - t2) * left.normal + t2 * start.normal
        # left_norm = left_norm / np.linalg.norm(left_norm)
        # t = (right.x - point[0]) / (right.x - left.x) if abs(right.x - left.x) > self._eps else right.x - point[0]
        # norm = (1 - t) * right_norm + t * left_norm
        # norm = norm / np.linalg.norm(norm)
        # norm = copy.deepcopy(obj.normals[index])
        ambient_intensity = obj.get_shadow_color(light_src)
        diff_coeff = norm.dot(light_dir)
        if diff_coeff < 0:
            diffuse_light_intensity = np.array([0., 0., 0., 1])
        else:
            # diffuse_light_intensity = np.clip(0, (obj.diffuse * diff_coeff * light_src.diffuse_light),
            #                                   1)
            diffuse_light_intensity = (obj.diffuse * diff_coeff * light_src.diffuse_light)
        reflected_light = obj.reflect(light_dir, norm)
        reflected_light = reflected_light / np.linalg.norm(reflected_light)
        coeff = reflected_light.dot(self.__direction)
        # if coeff < 0:
        specular_light_intensity = np.array([0., 0., 0., 1])
        # else:
        #     # specular_light_intensity = np.clip(0,
        #     #                                    pow(coeff, obj.specular_exp) * (obj.specular * light_src.specular_light),
        #     #                                    1)
        #     specular_light_intensity = pow(coeff, obj.specular_exp) * (obj.specular * light_src.specular_light)
        color = np.clip(0, diffuse_light_intensity + ambient_intensity + specular_light_intensity, 1)
        # print(color)
        color[3] = 1
        if np.allclose(color, 1):
            print("fullstack")
        else:
            print(color)
        return color

    def get_normal(self, point, obj, index):
        # vertices = [obj.vertices[i] for i in obj.polygons[index]]
        vertices = self.sort_vertices([obj.vertices[i] for i in obj.polygons[index]])
        start = vertices[0]
        left = vertices[1]
        right = vertices[2]
        if point[1] < left.y:
            start, right = right, start
        elif point[1] < right.y:
            start, left = left, start
        t1 = (point[1] - right.y) / (start.y - right.y) if abs(start.y - right.y) > self._eps else point[1] - right.y
        t2 = (point[1] - left.y) / (start.y - left.y) if abs(start.y - left.y) > self._eps else point[1] - left.y
        right_norm = (1 - t1) * right.normal + t1 * start.normal
        # right_norm = right_norm / np.linalg.norm(right_norm)
        left_norm = (1 - t2) * left.normal + t2 * start.normal
        # left_norm = left_norm / np.linalg.norm(left_norm)
        t = (right.x - point[0]) / (right.x - left.x) if abs(right.x - left.x) > self._eps else right.x - point[0]
        norm = (1 - t) * right_norm + t * left_norm
        norm = norm / np.linalg.norm(norm)
        return norm

    def trace(self, objects, light_src, depth=0):
        nearest_obj, t_min, intersect_polygon_index = self._get_nearest_obj(objects)
        if nearest_obj is not None:
            point = self.__origin + self.__direction * t_min
            light_D = light_src.coordinates.vector - point
            light_D = light_D / np.linalg.norm(light_D)
            # N = nearest_obj.normals[intersect_polygon_index]

            N = self.get_normal(point, nearest_obj, intersect_polygon_index)
            shifted_point = point - 1e-3 * N if light_D.dot(N) < 0 else point + 1e-3 * N
            _, light_t, _ = self._get_nearest_obj(objects, shifted_point, light_D)
            light_dist = np.linalg.norm(light_src.coordinates.vector - point)
            # print(point)
            min_dist = light_t if light_t == np.inf else np.linalg.norm(light_D * light_t)
            if min_dist >= light_dist:
                color = self.calculate_color(N, light_src, intersect_polygon_index, nearest_obj, light_D)
            else:
                color = nearest_obj.get_shadow_color(light_src)
                print("shadow's sometimes all i need: ", color)
                color[3] = 1
        else:
            color = np.array([0.9, 0.9, 0.9, 1.])
        # print(color)
        return color
    # if t_min != np.inf:
    #     print("Wel ", t_min)
    # if depth == self.__max_depth:
    #     pass
