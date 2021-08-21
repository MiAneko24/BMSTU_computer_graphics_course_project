import numpy as np
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QBrush, QColor, QPalette
from PyQt5.QtWidgets import QGraphicsScene, QColorDialog, QVBoxLayout

from Camera import Camera
from Cone import Cone
from Cylinder import Cylinder
from LightSource import LightSource
from ObjectType import ObjectType
from PolygonalModels.Pyramid import Pyramid
from PyQt5 import QtWidgets
from PolygonalModels.interface import Ui_MainWindow
from SceneManager import SceneManager
from TransformMatrix import TransformMatrix
from Vertex import Vertex
from ZBufAlgorithm import ZBufAlgorithm


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.__manager = SceneManager()
        self.ui.setupUi(self)
        self.__scene = QGraphicsScene(self)
        self.__scene.setSceneRect(QRectF(0, 0, 1355, 905))
        self.ui.graphicsView.setScene(self.__scene)
        # self.ui.graphicsView.fitInView(QRectF(0, 0, 530, 540))
        self.__brush = QBrush(Qt.black)
        self.ui.pushButton.clicked.connect(self.click_color_btn)
        self.__algorithm = ZBufAlgorithm(self.__scene, self.__brush, LightSource(Vertex([-15, -50, 500]), diffuse_light=1,
                                                                          specular_light=0.1,
                                                                          color=np.array([90, 90, 90])),
                                  Camera(width=self.__scene.width(), height=self.__scene.height(),
                                         pos=np.array([0., 0., 50.])))
        self.color = QColor(0., 0., 255.)
        # lay = QVBoxLayout(self)
        # lay.addWidget(self.ui.pushButton)
        self.palette = self.ui.pushButton.palette()
        self.palette.setColor(QPalette.Button, self.color)
        self.ui.pushButton.setPalette(self.palette)
        self.color_dialog = QColorDialog(self)
        self.color_dialog.currentColorChanged.connect(self.change_color)
        self.ui.pushButton_2.clicked.connect(self.add_object)

    def click_color_btn(self):
        self.color_dialog.exec()
        self.palette.setColor(QPalette.Button, self.color)
        self.ui.pushButton.setPalette(self.palette)

    def change_color(self, color):
        self.color = color

        # self.ui.comboBox.


    def add_object(self):
        obj_type = self.ui.comboBox.currentIndex()
        obj_type = ObjectType(obj_type)
        print(obj_type is ObjectType.cone)
        params = []
        try:
            params.append(float(self.ui.lineEdit.text()))
            if params[-1] <= 0:
                raise ValueError
            print("passed 1")
            params.append(float(self.ui.lineEdit_2.text()))
            if params[-1] <= 0:
                raise ValueError

            print("passed 2")
            print(self.ui.lineEdit_3.text())
            params.append(int(self.ui.lineEdit_3.text()))
            if params[-1] < 0:
                raise ValueError
            print("passed 3")
            params.append(float(self.ui.lineEdit_4.text()))
            if params[-1] < 0 or params[-1] > 1:
                raise ValueError
            print("passed 4")
            params.append(float(self.ui.lineEdit_5.text()))
            if params[-1] < 0 or params[-1] > 1:
                raise ValueError
            print("passed 5")
            params.append(float(self.ui.lineEdit_6.text()))
            if params[-1] < 0 or params[-1] > 1:
                raise ValueError
            print("passed 6")
            params.append(float(self.ui.lineEdit_7.text()))
            if params[-1] < 0 or params[-1] > 1:
                raise ValueError

            print("passed 7")
            params.append(np.array(self.color.getRgbF()) * 255)
            print(params[-1])
        except ValueError:
            return


        # Ввод и проверка данных! Ну и мб исчезновение строки ввода длины стороны/радиуса в зависимости от фигуры
        self.__manager.add_object(obj_type, params)
        self.draw_z()





    def draw_z(self):
        # obj = []

        # obj.append(Cone(150, 200, [-120.0, 3.0, -50.0], color=np.array([210, 0, 0])))
        # obj[-1].transparency = 0.1
        # obj[-1].reflectivity = 0.6
        # obj[-1].specular = 0.8
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_x=-40))

        # obj.append(Pyramid([300, 3, 150, 0.4, 0.0, 0.0, 1, np.array([0, 189, 0])]))
        # obj[-1].transparency = 0.4
        # obj[-1].reflectivity = 1
        # obj[-1].specular = 0.0
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_z=121, angle_x=50))

        # obj.append(Cylinder(150, 200, [0.0, 130.0, 10.0], color = np.array([200, 150, 0])))
        #
        # obj[-1].transparency = 0.7
        # obj[-1].reflectivity = 0.89
        # obj[-1].specular = 0.5
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_y=140, angle_z=200, angle_x=160))

        self.__algorithm.clear()
        for i in self.__manager.objects:
            i.accept(self.__algorithm)
        self.__algorithm.draw()
        # algorithm.draw(obj)


