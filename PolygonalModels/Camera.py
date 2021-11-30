import copy
from math import tan, radians

import numpy as np

from PolygonalModels.InvisiblePolygonsClipper import InvisiblePolygonsClipper
from PolygonalModels.Ray import Ray
from PolygonalModels.TransformMatrix import TransformMatrix
from PolygonalModels.Vertex import Vertex


class Camera:
    def __init__(self, width, height, pos=np.array([0., 0., 0.]), up=np.array([0., 1., 0.]), center=np.array([0., 0., 299.]), fov=90, near=1, far=300):
        self.eps = 1e-5
        self.__eye = pos
        self.__up = up
        self.__lookat = center
        self.__fov = radians(fov)
        self.__z_near = near
        self.__z_far = far
        self.__aspect_ratio = width / height
        self.__width = width
        self.__height = height
        self.__transform_matrix = TransformMatrix.ScaleMatrix()
        self.__lookat_mat = self.lookat()
        self.__viewport_mat = self.viewport()
        self.__clipper = InvisiblePolygonsClipper(tan(radians(fov / 2)), near, far)
        self.__projection_matrix = TransformMatrix.ProjectionMatrix(self.__fov, self.__aspect_ratio, near, far)
        self.__canvas_to_world_mat = self.__canvas_to_world_matrix()
        self.__up_down_angle = 0
        self.__left_right_angle = 0

        print("projection matrix is: ", self.__projection_matrix)
        print("lookat matrix is: ", self.__lookat_mat)
        print("dot (l x p): ", self.__lookat_mat.dot(self.__projection_matrix))

    def lookat(self):
        # lookat = Vertex(self.__lookat).transform(self.__transform_matrix).vector
        # eye = Vertex(self.__eye).transform(self.__transform_matrix).vector
        # eye = eye.dot(self.__transform_matrix)
        # up = Vertex(self.__up).transform(self.__transform_matrix).vector
        # up = up / np.linalg.norm(up)

        w = self.__lookat - self.__eye
        # w = w[:3]
        w = w / np.linalg.norm(w) if np.linalg.norm(w) != 0 else np.array([0., 0., 0.])
        u = np.cross(w, self.__up)
        u = u / np.linalg.norm(u) if np.linalg.norm(u) != 0 else np.array([0., 0., 0.])
        v = - np.cross(w, u)
        v = v / np.linalg.norm(v) if np.linalg.norm(v) != 0 else np.array([0., 0., 0.])
        minv = np.array([[1. if i == j else 0. for i in range(4)] for j in range(4)])
        # tr = np.array([[1 if i == j else 0 for i in range(4)] for j in range(4)])
        x0 = - np.dot(self.__eye, u)
        y0 = - np.dot(self.__eye, v)
        z0 = - np.dot(self.__eye, w)
        print("X0 = ", x0, ", y= ", y0, ", z0 = ", z0)

        for i in range(3):
            minv[i][0] = u[i]
            minv[i][1] = v[i]
            minv[i][2] = w[i]
            # tr[i][3] = -self.__center[i]
        minv[3][0] = x0
        minv[3][1] = y0
        minv[3][2] = z0
        minv[3][3] = 1
        # modelview = np.dot(minv, tr)
        # print("________________\nlookat matrix:\n", minv, "\n")
        return minv

    def camera_inside_of_object(self, polygons, normals):
        inside = True
        for i in range(len(polygons)):
            test_v = polygons[i][0].vector - self.__eye
            if test_v.dot(normals[i]) < 0:
                inside = False
                break
        return inside

    def get_visible_polygons(self, polygons, normals):
        if self.camera_inside_of_object(polygons, normals):
            return []
        normals = copy.deepcopy(normals)
        normals = list(normals)
        i = 0
        while i < len(polygons):
            if not self.polygon_is_visible(normals[i], polygons[i][0]):# or self.__clipper.triangle_is_trivial_invisible(polygons[i]):
                polygons.pop(i)
                normals.pop(i)
                continue
            i += 1
        return polygons

    def get_projection(self, vertex):
        # vertex.y *= -1
        # return self.__orthogonal_projection(vertex)
        return self.__perspective_projection(vertex)

    def polygon_is_visible(self, normal, vert):
        look = vert.vector - self.__eye
        dot = look.dot(normal)

        return False if dot >= 0 else True
        # return False if dot > - self.eps else True

    # def __check_section_visibility(self, start, end, tg):



    def __canvas_to_world_matrix(self):
        g = np.linalg.inv(self.__lookat_mat)
        ky = tan(self.__fov / 2)
        kx = ky * self.__aspect_ratio
        fov_mat = TransformMatrix.ScaleMatrix(kx=kx, ky=ky)
        # viewport_inv = np.linalg.inv(self.__viewport_mat)
        # viewport_inv = np.linalg.inv(self.__viewport_mat)
        viewport_inv = TransformMatrix.ScaleMatrix(kx = 2/self.__width, ky = -2/self.__height)
        viewport_inv[3][0] = -1
        viewport_inv[3][1] = 1
        # mat =
        # fov_mat = self.__projection_matrix
        # fov_mat[2][2] = 1
        # fov_
        return np.linalg.inv(self.__lookat_mat.dot(self.__projection_matrix.dot(self.__viewport_mat)))
        # return viewport_inv.dot(fov_mat.dot(g))
        # return g.dot(viewport_inv.dot(fov_mat))

    def __perspective_projection(self, vertex):
        v = vertex.transform(self.__lookat_mat)
        v = v.transform(self.__projection_matrix)
        v = v.transform(self.__viewport_mat)
        if v.z < 0 and v.transform_vector[-1] < 0:
            v.z *= -1
        v.make_decart_coords()
        return v


    def __orthogonal_projection(self, vertex):
        return copy.deepcopy(vertex)

    def viewport(self):
        mat = TransformMatrix.MoveMatrix(dx=(self.__width / 2), dy=(self.__height / 2))
        mat[0][0] = self.__width / 2
        mat[1][1] = -self.__height / 2
        mat[2][2] = 1
        # mat = np.array([[0 for i in range(TransformMatrix.dimensions)] for j in
        #                 range(TransformMatrix.dimensions)])

        # mat[3][0] = self.__width / 2
        # mat[3][1] = self.__height / 2

        return mat

    def get_canvas_and_world_coords(self, coords):
        # m = self.lookat()

        coords[2] = self.__z_near
        coords = coords.dot(self.__canvas_to_world_mat)
        # coords.dot(np.linalg.inv(self.__lookat_mat))
        coords = coords[:3] / coords[-1]
        # coords = coords / 10000
        # coords = coords[:3]
        # coords[2] = self.__z_near

        return coords

    # def get_canv_coords(self, x, y, new_w, new_h):
    #     canv_coords = np.array([x, y, self.__z_near, 1])
    #     kx = self.__width / new_w
    #     ky = self.__height / new_h
    #     mat = self.__viewport_mat
    #     mat[0][0] = kx
    #     mat[1][1] = ky
    #     canv_coords = np.array(canv_coords.dot(mat)[:2], dtype=np.int)
    #     return canv_coords[0], canv_coords[1]

    def cast_ray(self, pixel):
        # pixel[0] = (2 * (pixel[0] + 0.5) / self.__width - 1) * tan(self.__fov / 2.) * self.__aspect_ratio;
        # float
        # pixel[1] = -(2 * (pixel[1] + 0.5) / self.__height - 1) * tan(self.__fov / 2.);
        ray_to = self.get_canvas_and_world_coords(pixel)
        return Ray(self.__eye, end_point=ray_to)

    # def get_near_sizes(self):
    #     width = 2 * tan(self.__fov / 2)
    #     height = width / self.__aspect_ratio
    #     return width, height

    def move(self, params):
        dx = params['right'] if "right" in params.keys() else -params['left'] if "left" in params.keys() else 0.
        dz = params['forward'] if "forward" in params.keys() else -params['back'] if "back" in params.keys() else 0.
        dy = params['up'] if "up" in params.keys() else -params['down'] if "down" in params.keys() else 0.
        print(params)
        mat = self.__lookat_mat.dot(TransformMatrix.MoveMatrix(dx, dy, dz)).dot(np.linalg.inv(self.__lookat_mat))
        # mat = TransformMatrix.MoveMatrix(dx, dy, dz)
        print("before eye = ", self.__eye, ", lookat = ",self.__lookat)
        # v = Vertex()
        # v.vector = self.__up
        # self.__up = Vertex(self.__up).transform(TransformMatrix.MoveMatrix(dx, dy, dz)).vector
        self.__eye = Vertex(self.__eye).transform(mat).vector
        self.__lookat = Vertex(self.__lookat).transform(mat).vector
        # self.__transform_matrix = self.__transform_matrix.dot(mat)

        print("after eye = ", self.__eye, ", lookat = ",self.__lookat)
        self.__lookat_mat = self.lookat()
        print(self.__lookat_mat)
        self.__canvas_to_world_mat = self.__canvas_to_world_matrix()

    def rotate(self, params):
        new_up_d = params['up'] if "up" in params.keys() else -params['down'] if "down" in params.keys() else 0.
        self.__up_down_angle += new_up_d
        print(params)
        warning = self.__up_down_angle > 90 or self.__up_down_angle < -90
        self.__up_down_angle = np.clip(-90, self.__up_down_angle, 90)
        new_l_r = params['right'] if "right" in params.keys() else -params['left'] if "left" in params.keys() else 0.
        self.__left_right_angle += new_l_r
        if new_up_d != 0 and -90 <= self.__left_right_angle <= 90:
            mat = self.__lookat_mat.dot(TransformMatrix.RotateMatrix(angle_x=new_up_d).dot(np.linalg.inv(self.__lookat_mat)))
            # mat = TransformMatrix.RotateMatrix(angle_x=new_up_d)
            # self.__transform_matrix = self.__transform_matrix.dot(mat)
            print("Before ", self.__up)
            v = Vertex()
            v.vector = self.__up
            self.__up = v.transform(mat).vector
            print("After ", self.__up)
        # if new_up_d != 0:
        print("Before ", self.__lookat)
        print(new_up_d)
        mat = self.__lookat_mat.dot(TransformMatrix.RotateMatrix(angle_y=new_l_r, angle_x=new_up_d).dot(np.linalg.inv(self.__lookat_mat)))
        self.__lookat = Vertex(self.__lookat).transform(mat).vector
        print("After ", self.__lookat)
        self.__up = self.__up / np.linalg.norm(self.__up)

        self.__lookat_mat = self.lookat()
        self.__canvas_to_world_mat = self.__canvas_to_world_matrix()
        return warning
