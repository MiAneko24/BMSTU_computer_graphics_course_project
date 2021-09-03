from math import cos, sin

import numpy as np
from PolygonalModels.Sphere import Sphere
from PolygonalModels.Vertex import Vertex
from ObjectType import ObjectType
from TransformMatrix import TransformMatrix


class SceneObject:

    def __init__(self, params):
        self._polygons = np.array([])
        self._vertices = np.array([])
        self._normals = np.array([])
        self._sphere = Sphere()
        self._color = np.array([0.0, 0.0, 0.0])
        self._r = params[0]
        self._h = params[1]
        self._n = params[2]
        self._transparency = params[3]
        self._specular = params[4]
        self._refraction = params[5]
        self._reflectivity = params[6]
        self._color = params[7]
        self._transform_matrix = TransformMatrix.ScaleMatrix()
        self._type = ObjectType.cone

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
        self._reflectivity = params['reflectivity'] if 'reflectivity' in params.keys() else self._reflectivity
        self._refraction = params['refraction'] if 'refraction' in params.keys() else self._refraction
        self._color = params['color'] if 'color' in params.keys() else self._color
        return restruct_needed


    @property
    def reflectivity(self):
        return self._reflectivity

    @reflectivity.setter
    def reflectivity(self, rf):
        self._reflectivity = rf

    @property
    def refraction(self):
        return self._refraction

    @refraction.setter
    def refraction(self, rf):
        self._refraction = rf

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, cl):
        self._color = cl

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
        return self._specular

    @specular.setter
    def specular(self, sp):
        if 0 <= sp <= 1:
            self._specular = sp
        else:
            raise ObjectException()

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
        return self._normals

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
        center = np.array([0, 0, 0])
        for i in range(len(self.vertices)):
            center = center + np.array(self.vertices[i].vector)
        center = center / len(self.vertices)
        normals = []
        for poly in self._polygons:
            first_edge = self.vertices[poly[1]].vector - self.vertices[poly[0]].vector
            second_edge = self.vertices[poly[2]].vector - self.vertices[poly[0]].vector
            normals.append(np.cross(first_edge, second_edge))
            test_vector = center - self.vertices[poly[0]].vector
            if np.dot(normals[-1], test_vector) > 0:
                normals[-1] *= -1
            normals[-1] /= np.linalg.norm(normals[-1])
        self.normals = np.array(normals)
        for i in range(len(self.vertices)):
            normals = []
            for j in range(len(self.polygons)):
                if i in self.polygons[j]:
                    normals.append(np.array(self.normals[j]))
            self.vertices[i].get_normal(normals)

    def transform(self, matrix, rotate=False):
        rotate_mat = matrix
        if rotate:
            center = self._get_center_coords()
            move_mat = TransformMatrix.MoveMatrix(-center.x, -center.y, -center.z)
            rotate_mat = move_mat.dot(matrix)
            move_mat = TransformMatrix.MoveMatrix(center.x, center.y, center.z)
            rotate_mat.dot(move_mat)

        self._transform_matrix = self._transform_matrix.dot(rotate_mat)

    def _get_center_coords(self):
        center = Vertex()
        for vertex in self._vertices:
            center.vector += vertex.vector
        amount = len(self._vertices)
        center.vector /= amount
        return center

    def accept(self, visitor):
        visitor.visit(self)



class ObjectException(Exception):
    def __init__(self, message="Пустая модель недопустима"):
        self.message = message
        super().__init__(self.message)
