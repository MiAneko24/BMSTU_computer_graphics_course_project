from Cone import Cone
from Cylinder import Cylinder
from ObjectType import ObjectType
from Pyramid import Pyramid


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

    @property
    def objects(self):
        return self.__objects

    def get_amount_of_objects(self):
        return len(self.__objects)


