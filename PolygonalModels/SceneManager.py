from Cone import Cone
from Cylinder import Cylinder
from ObjectType import ObjectType
from Pyramid import Pyramid
from TransformMatrix import TransformMatrix


class SceneManager:
    def __init__(self):
        self.__objects = []

    def add_object(self, type_obj, params):
        if len(self.__objects) == 3:
            print("Max elems are on scene")
            # raise
            return
        self.__objects.append(Cone(params) if type_obj is ObjectType.cone else
                              Cylinder(params) if type_obj is ObjectType.cylinder else Pyramid(params))
        print("added obj ", type_obj)

    def change_object(self, params, index=-1):
        if abs(index) > len(self.__objects):
            print("Incorrect index")
            return
        if index == -1:
            for obj in self.__objects:
                obj.change(params)
        else:
            self.__objects[index].change(params)

    def rotate(self, ox, oy, oz, index):
        if abs(index) > len(self.__objects):
            print("Incorrect index")
            return
        matrix = TransformMatrix.RotateMatrix(ox, oy, oz)
        self.__objects[index].transform(matrix)

    def move(self, dx, dy, dz, index):
        if abs(index) > len(self.__objects):
            print("Incorrect index")
            return
        matrix = TransformMatrix.MoveMatrix(dx, dy, dz)
        self.__objects[index].transform(matrix)

    def scale(self, kx, ky, kz, index):
        if abs(index) > len(self.__objects):
            print("Incorrect index")
            return
        matrix = TransformMatrix.ScaleMatrix(kx, ky, kz)
        self.__objects[index].transform(matrix)

    @property
    def objects(self):
        return self.__objects

    def get_amount_of_objects(self):
        return len(self.__objects)


