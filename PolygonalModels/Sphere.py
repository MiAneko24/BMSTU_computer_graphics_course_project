
class Sphere:
    def __init__(self):
        self.__radius = 0
        self.__center = []

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, r):
        self.__radius = r
        # TODO: add radius check in setter

    @property
    def center(self):
        return self.__center

    @center.setter
    def center(self, cent):
        self.__center = cent

    def is_intersected(self, ray):
        # TODO: add Ray class & intersection wth sphere algorithm. Maybe create an intersection method in ray itself?
        pass
