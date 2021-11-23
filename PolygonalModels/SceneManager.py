from PolygonalModels.Cone import Cone
from PolygonalModels.Cylinder import Cylinder
from PolygonalModels.ObjectType import ObjectType
from PolygonalModels.Prism import Prism
from PolygonalModels.Pyramid import Pyramid
from PolygonalModels.TransformMatrix import TransformMatrix


class SceneManager:
    def __init__(self):
        self.__objects = []
        self._max_amount = 4

    def add_object(self, type_obj, params):
        if len(self.__objects) == self._max_amount:
            print("Max elems are on scene")
            # raise
            return
        print(self.__objects)
        self.__objects.append(Cone(params) if type_obj is ObjectType.cone else
                              Cylinder(params) if type_obj is ObjectType.cylinder else Pyramid(params)
                              if type_obj is ObjectType.pyramid else Prism(params))
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
        self.__objects[index].transform(matrix, rotate=True)

    def move(self, dx, dy, dz, index):
        if abs(index) > len(self.__objects):
            print("Incorrect index")
            return
        matrix = TransformMatrix.MoveMatrix(dx, dy, dz)
        self.__objects[index].transform(matrix)

    def delete(self, index):
        if abs(index) > len(self.__objects) or abs(index) < 0:
            print("Incorrect index")
            return
        self.__objects.pop(index)

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


