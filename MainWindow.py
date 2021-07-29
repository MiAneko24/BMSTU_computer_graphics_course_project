import numpy as np
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsScene

from Camera import Camera
from Cone import Cone
from Cylinder import Cylinder
from LightSource import LightSource
from PolygonalModels.Pyramid import Pyramid
from PyQt5 import QtWidgets
from PolygonalModels.interface import Ui_MainWindow
from TransformMatrix import TransformMatrix
from Vertex import Vertex
from ZBufAlgorithm import ZBufAlgorithm


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__scene = QGraphicsScene(self)
        self.__scene.setSceneRect(QRectF(0, 0, 1355, 905))
        self.ui.graphicsView.setScene(self.__scene)
        # self.ui.graphicsView.fitInView(QRectF(0, 0, 530, 540))
        self.__brush = QBrush(Qt.black)

    def draw_z(self):
        obj = []
        # obj.append(Cone(150, 200, [-120.0, 3.0, -50.0], color=np.array([210, 0, 0])))
        # obj[-1].transparency = 0.1
        # obj[-1].reflectivity = 0.6
        # obj[-1].specular = 0.8
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_x=-40))

        obj.append(Pyramid(300, 3, 150, [100., 50., 20.], color=np.array([0, 189, 0])))
        obj[-1].transparency = 0.4
        obj[-1].reflectivity = 1
        obj[-1].specular = 0.0
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_z=121, angle_x=50))

        # obj.append(Cylinder(150, 200, [0.0, 130.0, 10.0], color = np.array([200, 150, 0])))
        #
        # obj[-1].transparency = 0.7
        # obj[-1].reflectivity = 0.89
        # obj[-1].specular = 0.5
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_y=140, angle_z=200, angle_x=160))

        algorithm = ZBufAlgorithm(self.__scene, self.__brush, LightSource(Vertex([-15, -50, 500]), diffuse_light=1,
            specular_light=0.1, color=np.array([90, 90, 90])), Camera(width=self.__scene.width(), height=self.__scene.height(), pos=np.array([0, 0, 100])))
        algorithm.draw(obj)
