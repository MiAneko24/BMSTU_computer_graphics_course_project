import copy
from math import cos, sin
from time import time

import numpy as np
from numba import jit

from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex
from PolygonalModels.ObjectType import ObjectType
from PolygonalModels.TransformMatrix import TransformMatrix


class SceneObject:

    def __init__(self, params):
        self._eps = 1e-5
        self._polygons = np.array([])
        self._vertices = np.array([])
        self._normals = np.array([])
        self._sphere = Sphere()
        # self._color = np.array([0.0, 0.0, 0.0])
        self._r = params[0]
        self._h = params[1]
        self._n = params[2]
        self._transparency = params[3]
        self._specular = params[4]
        # self._specular = 1
        # self._specular = np.array([0.5019, 0.5019, 0.5019, 1])
        self._specular_exp = params[5]
        self._diffuse = params[6]
        self._color = params[7]
        # self._reflectivity = np.array([0, 0.5098, 0.5098,1])
        self._transform_matrix = TransformMatrix.ScaleMatrix()
        self._type = ObjectType.cone
        self._specularity = params[8]
        self._reflection = params[9]
        print("Diffuse = ", self._diffuse)
        self._refraction = params[10]
        # self._specular_exp = 10
        # self._ambient = 0.3

    @property
    def refraction(self):
        return self._refraction

    def change(self, params):
        restruct_needed = False
        if 'r' in params.keys():
            self._r = params['r']
            restruct_needed = True
        if 'h' in params.keys():
            self._h = params['h']
            restruct_needed = True
        if 'n' in params.keys():
            self._n = params['n']
            restruct_needed = True
        self._transparency = params['transparency'] if 'transparency' in params.keys() else self._transparency
        self._specular = params['specular'] if 'specular' in params.keys() else self._specular
        print("Specular exp = ", self._specular_exp)
        self._specular_exp = params['specular_exp'] if 'specular_exp' in params.keys() else self._specular_exp
        self._diffuse = params['diffuse'] if 'diffuse' in params.keys() else self._diffuse
        self._color = params['color'] if 'color' in params.keys() else self._color
        self._specularity = params['specularity'] if 'specularity' in params.keys() else self._specularity
        self._reflection = params['reflection'] if 'reflection' in params.keys() else self._reflection
        self._refraction = params['refraction'] if 'refraction' in params.keys() else self._refraction

        print("Diffuse = ", self._diffuse)
        return restruct_needed
    #
    # @property
    # def specularity(self):
    #     return self._specularity

    @property
    def diffuse(self):
        return self._diffuse

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, cl):
        self._color = cl

    @property
    def reflection(self):
        return self._reflection

    @property
    def transparency(self):
        return self._transparency

    @transparency.setter
    def transparency(self, vs):
        if 0 <= vs <= 1:
            self._transparency = vs
        else:
            raise ObjectException()

    @property
    def specular(self):
        return self._specular * self._specularity

    @specular.setter
    def specular(self, sp):
        if 0 <= sp <= 1:
            self._specular = sp
        else:
            raise ObjectException()

    @property
    def specular_exp(self):
        return self._specular_exp

    @property
    def polygons(self):
        return self._polygons

    @polygons.setter
    def polygons(self, pol):
        if pol.size > 0:
            self._polygons = pol
        else:
            raise ObjectException()

    @property
    def vertices(self):
        vertices = []
        single_mat = np.array([[1.0 if i == j else 0.0 for i in range(4)] for j in range(4)])
        if not np.allclose(single_mat, self._transform_matrix):
            for vertex in self._vertices:
                vertices.append(vertex.transform(self._transform_matrix))
        else:
            vertices = self._vertices
        return vertices

    @vertices.setter
    def vertices(self, vertex):
        self._vertices = vertex
        # TODO: add check params in setters

    @property
    def normals(self):
        mat = np.linalg.inv(self._transform_matrix)
        normals = copy.deepcopy(self._normals)
        for i in range(len(normals)):
            n = normals[i].dot(mat.transpose()[:3, :3])
            if np.linalg.norm(n) != 0:
                n = n / np.linalg.norm(n)
            normals[i] = n
        return normals


        # return self._normals

    @normals.setter
    def normals(self, norms):
        self._normals = norms

    @property
    def sphere(self):
        return self._sphere

    @sphere.setter
    def sphere(self, sp):
        self._sphere = sp

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t):
        if t in ObjectType:
            self._type = t

    def calculate_normals(self):
        center = np.array([0, 0, 0.])
        for i in range(len(self._vertices)):
            center = center + np.array(self._vertices[i].vector)
        center = center / len(self._vertices)
        normals = []
        for poly in self._polygons:
            first_edge = self._vertices[poly[1]].vector - self._vertices[poly[0]].vector
            second_edge = self._vertices[poly[2]].vector - self._vertices[poly[0]].vector
            normals.append(np.cross(first_edge, second_edge))
            test_vector = center - self._vertices[poly[0]].vector
            if np.dot(normals[-1], test_vector) > 0:
                normals[-1] *= -1
            normals[-1] /= np.linalg.norm(normals[-1])
        self._normals = np.array(normals)
        for i in range(len(self._vertices)):
            normals = []
            for j in range(len(self.polygons)):
                if i in self.polygons[j]:
                    normals.append(np.array(self._normals[j]))
            self._vertices[i].get_normal(normals)
            print(self._vertices[i].normal)

    def transform(self, matrix, rotate=False):
        rotate_mat = matrix
        if rotate:
            center = self._get_center_coords()
            print(center.vector)
            move_mat = TransformMatrix.MoveMatrix(-center.x, -center.y, -center.z)
            rotate_mat = move_mat.dot(matrix)
            move_mat = TransformMatrix.MoveMatrix(center.x, center.y, center.z)
            rotate_mat = rotate_mat.dot(move_mat)

        self._transform_matrix = self._transform_matrix.dot(rotate_mat)

    def _get_center_coords(self):
        center = Vertex()
        for vertex in self.vertices:
            center.transform_vector += vertex.transform_vector
        amount = len(self.vertices)
        center.transform_vector = center.transform_vector / amount
        print("center = ", center.transform_vector)
        return center

    def accept(self, visitor):
        visitor.visit(self)

    # @jit
    def cross(self, v1, v2):
        res = np.array([v1[i-2] * v2[i-1] - v1[i-1] * v2[i-2] for i in np.arange(len(v1))])
        return res

    def dot(self, v1, v2):
        return sum(v1[i]*v2[i] for i in np.arange(len(v1)))

    def __get_intersection_coefficient(self, O, D, vertices):

        # s_t = time()
        v0 = vertices[0].vector
        E1 = vertices[1].vector - v0
        E2 = vertices[2].vector - v0
        P = self.cross(D, E2)
        det = self.dot(P, E1)
        if abs(det) < self._eps:
            return np.inf, 0., 0.
        inv_det = 1./det
        # print("E1 = ", E1, ", D = ", D, ", E2 = ", E2, ", P = ", P)
        T = O - v0
        u = self.dot(T, P) * inv_det
        if u < 0 or u > 1:
            # tt = time()-s_t
            # if tt>0:
            #     print("wrong u in ", tt)
            return np.inf, 0., 0.
        Q = self.cross(T, E1)
        v = self.dot(D, Q) * inv_det
        if v < 0 or (u + v) > 1:
            # tt = time()-s_t
            # if tt>0:
            #     print("wrong v in ", tt)
            return np.inf, 0., 0.
        # coeffs = 1 / P.dot(E1) * np.array([Q.dot(E2), P.dot(T), Q.dot(D)])
        t = self.dot(E2, Q) * inv_det


        # if not (0 <= u <= 1 and 0 <= v <= 1 and 0 <= (1 - u - v) <= 1):
        #     res_t = time() - s_t
        #     if (res_t > 0):
        #         print("got wrong coeffs in ", time() - s_t)
        #         print("coeffs = ", coeffs, ", v0 = ", vertices[0].vector, ", v1 = ", vertices[1].vector, ", v2 = ", vertices[2].vector )

        # return np.inf, 0., 0.
        # tt = time()-s_t
        # if tt>0:
        #     print("got coeffs in ", tt)
        return t, u, v

    # @jit
    def get_intersection(self, O, D):
        # s_time = time()
        t_min = np.inf
        u_min = 0
        v_min = 0
        i_min = 0
        if not self.sphere.is_intersected(O, D):
            return t_min, u_min, v_min, i_min
        # print("we look for an intersection")
        norms = self.normals
        verts = self.vertices
        for i, norm, polygon in zip(np.arange(0, len(norms)), norms, self.polygons):
            s_t = time()
            if D.dot(norm) > 0:
                continue
            vertices = [verts[j] for j in polygon]
            t, u, v = self.__get_intersection_coefficient(O, D, vertices)
            if t < t_min:
                t_min = t
                i_min = i
                v_min = v
                u_min = u
            # rt = time() - s_t
            # if rt > 0:
            #     print("iter cycle ended in ", rt)
        # print("we got it")
        # e_time = time()

        # print("Cert obj get inter = ", e_time-s_time)
        return t_min, u_min, v_min, i_min

    def get_color(self, point, light_src, index, cam_pos):
        light_dir = light_src.coordinates.vector - point
        light_dir = light_dir / np.linalg.norm(light_dir)
        norm = copy.deepcopy(self.normals[index])
        ambient_intensity = self._ambient * self.color * light_src.ambient_light
        diff_coeff = light_dir.dot(norm)
        if diff_coeff < 0:
            diffuse_light_intensity = np.array([0.,0.,0.,1])
        else:
            diffuse_light_intensity = (self.reflectivity * self.color * diff_coeff * light_src.diffuse_light)
        print(light_dir.dot(norm))
        # print("index = ", index, " src diff = ", light_src.diffuse_light, ", l_dir * norm = ", light_dir.dot(norm), ", norm = ", norm, ", intense = ", diffuse_light_intensity * self.reflectivity)
        # self.
        # cam_dir = -cam_pos + point
        # cam_dir = cam_dir / np.linalg.norm(cam_dir)
        # V = light_dir + cam_dir
        # V = V/np.linalg.norm(V)
        # specular_light_intensity = pow(V.dot(norm), self._specular_exp) * (self._specular * self._color * light_src.specular_light)
        reflected_light = self.reflect(light_dir, norm)
        reflected_light = reflected_light / np.linalg.norm(reflected_light)
        coeff = reflected_light.dot(cam_pos)
        if coeff < 0:
            specular_light_intensity = np.array([0.,0.,0.,1])
        else:
            specular_light_intensity = pow(coeff, 10) * (self._specular * self.color * light_src.specular_light)
        # color = self.reflectivity * (self.color) + (diffuse_light_intensity * light_src.color)
        color = diffuse_light_intensity + ambient_intensity + specular_light_intensity
        print(color)
        color[3] = 1
        return color

    def get_shadow_color(self, light_src):
        return light_src.ambient_light * self.color

class ObjectException(Exception):
    def __init__(self, message="Пустая модель недопустима"):
        self.message = message
        super().__init__(self.message)
