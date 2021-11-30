import copy
from math import sqrt
from time import time

import numpy as np


class Ray():
    def _get_nearest_obj(self, objects, O=None, D=None):
        if O is None:
            O = self.__origin
            D = self.__direction
        # s_time = time()
        nearest_obj = None
        t_min = np.inf
        intersect_polygon_index = 0
        u_min = 0
        v_min = 0
        for obj in objects:
            t, u, v, polygon = obj.get_intersection(O, D)
            if 0 <= t < t_min:
                nearest_obj = obj
                t_min = t
                u_min = u
                v_min = v
                intersect_polygon_index = polygon
        # end_t = time()
        # print("Got obj in ", end_t-s_time)
        return nearest_obj, t_min, u_min, v_min, intersect_polygon_index

    def __init__(self, start_point, end_point=None, D=None):
        self._eps = 1e-5
        if (end_point is None and D is None):
            return
        elif (end_point is not None):
            if np.allclose(start_point, end_point):
                return
            self.__direction = end_point - start_point
            self.__direction /= np.linalg.norm(self.__direction)
        else:
            self.__direction = D
        self.__origin = start_point
        self.__max_depth = 2

    # def sort_vertices(self, vertices):
    #     s = []
    #     # print("verts = ", [v.vector for v in vertices])
    #     tmp = vertices[0]
    #     for i in vertices:
    #         tmp = i if i.y > tmp.y and i.x <= tmp.x else tmp
    #     s.append(tmp)
    #     vertices.remove(tmp)
    #     if abs(tmp.x - vertices[0].x) < self._eps or abs(tmp.x -vertices[1].x) < self._eps:
    #         left = vertices[0] if vertices[0].x < vertices[1].x else vertices[1]
    #     else:
    #         k1 = (vertices[0].y - tmp.y) / (vertices[0].x - tmp.x)
    #         k2 = (vertices[1].y - tmp.y) / (vertices[1].x - tmp.x)
    #         left = vertices[0] if k1 > k2 else vertices[1]
    #     vertices.remove(left)
    #     s.append(left)
    #     s.extend(vertices)
    #     # print("sorted = ", [v.vector for v in s])
    #     return s

        # for i in range(3):
        #     for j in range(3 - i - 1):
        #         if round(vertices[j].y) > round(vertices[j + 1].y) or (round(vertices[j].y) == round(vertices[j + 1].y) and vertices[j].x > vertices[j + 1].x):
        #             vertices[j], vertices[j + 1] = vertices[j + 1], vertices[j]
        # return vertices


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
        elif abs(tmp.y-vertices[0].y) < self._eps or abs(tmp.y-vertices[1].y) < self._eps:
            left = vertices[0] if vertices[0].y < vertices[1].y else vertices[1]
        else:
            k1 = (vertices[0].y - tmp.y) / (vertices[0].x - tmp.x)
            k2 = (vertices[1].y - tmp.y) / (vertices[1].x - tmp.x)
            s_k1 = self.sign(k1)
            s_k2 = self.sign(k2)
            first_is_left = (k1 > k2 and ((s_k1 > 0 and s_k2 <= 0) or (s_k1 <= 0 and s_k2 > 0))) or (k1 < k2 and (
                        s_k1 == s_k2 == 1 or s_k1 == s_k2 == -1 or (s_k1 == -1 and s_k2 == 0) or (
                            s_k2 == -1 and s_k1 == 0)))
            left = vertices[0] if first_is_left else vertices[1]
        vertices.remove(left)
        s.append(left)
        s.extend(vertices)
        # print("sorted = ", [v.vector for v in s])
        return s

    def refract(self, I, N, eta_2, eta_1=1.):
        cos_1 = - max(-1., min(1, I.dot(N)))
        if cos_1 < 0:
            self.refract(I, -N, eta_1, eta_2)
        #     cos_1 *= -1
        #     eta_1, eta_2 = eta_2, eta_1
        #     N = -N
        eta = eta_1/eta_2
        k = 1 - eta*eta*(1 - cos_1*cos_1)
        return np.array([0.,0,0]) if k < 0 else I * eta + N * (eta * cos_1 - sqrt(k))


    def reflect(self, I, N):
        return I - 2 * N * (I.dot(N))


    def calculate_color(self, norm, light_src, obj, light_dir):
        ambient_intensity = obj.get_shadow_color(light_src)
        diff_coeff = light_dir.dot(norm)
        diffuse_light_intensity = obj.diffuse_reflection * obj.diffuse * max(0., diff_coeff) * light_src.diffuse_light
        reflected_light = self.reflect(light_dir, norm)
        coeff = reflected_light.dot(self.__direction)
        # if coeff < 0:
        #     specular_light_intensity = np.array([0., 0., 0., 1])
        # else:
        # powed_coeff = pow(coeff, obj.specular_exp / 4)
            # if powed_coeff > 1e-5:
            #     print("Hooray! ", end='')
            # print("spec coff = ", powed_coeff)
            # powed_coeff = powed_coeff if coeff >= 0 else 0
        specular_light_intensity = pow(max(0., coeff), obj.specular_exp) * obj.specular * obj.specularity * light_src.specular_light
        color = diffuse_light_intensity + ambient_intensity + specular_light_intensity
        color[3] = 1
        return color

    def get_normal(self, obj, index, u, v):
        vertices = [obj.vertices[i] for i in obj.polygons[index]]
        # vertices = self.sort_vertices([obj.vertices[i] for i in obj.polygons[index]])
        n= (1 - u - v) * vertices[0].normal + v * vertices[1].normal + u * vertices[2].normal
        n = n / np.linalg.norm(n)
        return n

    def trace(self, objects, light_src, depth=0):
        if depth == self.__max_depth:
            return np.array([1,1,1,1])
        nearest_obj, t_min, v_min, u_min, intersect_polygon_index = self._get_nearest_obj(objects)
        if nearest_obj is not None:
            point = self.__origin + self.__direction * t_min
            light_D = light_src.coordinates.vector - point
            light_D = light_D / np.linalg.norm(light_D)
            # N = nearest_obj.normals[intersect_polygon_index]
            N = self.get_normal(nearest_obj, intersect_polygon_index, u_min, v_min)
            # N = self.get_normal(point, nearest_obj, intersect_polygon_index)
            shifted_point = point + 1e-6 * N if light_D.dot(N) < 0 else point - 1e-6 * N
            _, light_t, _, _, _ = self._get_nearest_obj(objects, shifted_point, light_D)
            light_dist = np.linalg.norm(light_src.coordinates.vector - point)
            # print(point)
            min_dist = light_t if light_t == np.inf else np.linalg.norm(point + light_D * light_t)
            if min_dist >= light_dist:
                color = self.calculate_color(N, light_src, nearest_obj, light_D)
                if len(objects) > 1:
                    reflected_dir = self.reflect(self.__direction, N)
                    rdl = np.linalg.norm(reflected_dir)
                    if rdl != 0:
                        reflected_dir = reflected_dir / rdl
                        # shifted_point = point + 1e-6 * N if reflected_dir.dot(N) < 0 else point - 1e-6 * N
                        reflected_ray = Ray(shifted_point, D=reflected_dir)
                        color = color + nearest_obj.reflection * reflected_ray.trace(objects, light_src, depth + 1)
                    # print("Nearest obj refr = ", nearest_obj.refraction)
                    if nearest_obj.refraction != 0:
                        refracted_dir = self.refract(self.__direction, N, copy.deepcopy(nearest_obj.refraction))
                        rdl = np.linalg.norm(refracted_dir)
                        if rdl != 0:
                            refracted_dir / rdl
                            # shifted_point = point + 1e-6 * N if refracted_dir.dot(N) < 0 else point - 1e-6 * N
                            refracted_ray = Ray(shifted_point, D=refracted_dir)
                            color = color + nearest_obj.transparency * refracted_ray.trace(objects, light_src, depth + 1)
            else:
                color = nearest_obj.get_shadow_color(light_src)
                # print("shadow's sometimes all i need: ", color)
                color[3] = 1
        else:
            # if depth == 0:
            color = np.array([1, 1, 1, 1])
            # else:
            #     color = np.array([0, 0, 0, 1.])
            # color = light_src.ambient_light
        # print(color)
        return color
    # if t_min != np.inf:
    #     print("Wel ", t_min)
