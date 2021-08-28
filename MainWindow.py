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
        self.ui.pushButton.clicked.connect(self.click_adding_obj_color_btn)
        self.ui.pushButton_3.clicked.connect(self.click_new_color_btn)
        self.__algorithm = ZBufAlgorithm(self.__scene, self.__brush, LightSource(Vertex([-15, -50, 500]), diffuse_light=1,
                                                                          specular_light=0.1,
                                                                          color=np.array([90, 90, 90])),
                                  Camera(width=self.__scene.width(), height=self.__scene.height(),
                                         pos=np.array([0., 0., 100.])))
        self.add_color = QColor(0., 0., 255.)
        self.new_color = QColor("white")
        # lay = QVBoxLayout(self)
        # lay.addWidget(self.ui.pushButton)
        self.palette = self.ui.pushButton.palette()
        self.palette.setColor(QPalette.Button, self.add_color)
        self.ui.pushButton.setPalette(self.palette)

        self.new_palette = self.ui.pushButton_3.palette()
        self.new_palette.setColor(QPalette.Button, self.new_color)
        self.ui.pushButton_3.setPalette(self.new_palette)

        self.add_color_dialog = QColorDialog(self)
        self.add_color_dialog.currentColorChanged.connect(self.change_add_color)
        self.ui.pushButton_2.clicked.connect(self.add_object)

        self.new_color_dialog = QColorDialog(self)
        self.new_color_dialog.currentColorChanged.connect(self.change_new_color)
        self.ui.pushButton_4.clicked.connect(self.change_params)

        self.ui.pushButton_5.clicked.connect(self.rotate)

        self.ui.pushButton_6.clicked.connect(self.scale)
        self.ui.pushButton_7.clicked.connect(self.move)


    def click_adding_obj_color_btn(self):
        self.add_color_dialog.exec()
        self.palette.setColor(QPalette.Button, self.add_color)
        self.ui.pushButton.setPalette(self.palette)

    def change_add_color(self, color):
        self.add_color = color

        # self.ui.comboBox.

    def click_new_color_btn(self):
        self.new_color_dialog.exec()
        self.new_palette.setColor(QPalette.Button, self.new_color)
        self.ui.pushButton_3.setPalette(self.new_palette)
        cur_obj = self.ui.comboBox_2.currentIndex()
        if cur_obj == -1:
            return
        params = dict(color=np.array(self.new_color.getRgbF()) * 255)
        self.__manager.change_object(params, index=cur_obj)
        self.draw_z()
        #send ColorCommand

    def change_new_color(self, color):
        self.new_color = color


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
            params.append(np.array(self.add_color.getRgbF()) * 255)
            print(params[-1])
        except ValueError:
            return

        str_type = "Конус" if obj_type is ObjectType.cone else "Цилиндр" if obj_type is ObjectType.cylinder else "Пирамида"
        label = "Object " + str(self.ui.comboBox_2.count() + 1) + "(" + str_type + ")"
        self.ui.comboBox_2.addItem(label)
        # Ввод и проверка данных! Ну и мб исчезновение строки ввода длины стороны/радиуса в зависимости от фигуры
        self.__manager.add_object(obj_type, params)
        self.draw_z()

    def change_params(self):
        cur_obj = self.ui.comboBox_2.currentIndex()
        if cur_obj == -1:
            print("No objects available")
            return
        d = dict()
        try:
            r = -1
            r = self.ui.lineEdit_8.text()
            if r != "":
                r = float(r)
                if r <= 0:
                    raise ValueError
                d['r'] = r
            h = self.ui.lineEdit_9.text()

            if h != "":
                h = float(h)
                if h <= 0:
                    raise ValueError
                d['h'] = h

            n = self.ui.lineEdit_10.text()

            if n != "":
                n = float(h)
                if n <= 0:
                    raise ValueError
                d['n'] = n

            transparency = self.ui.lineEdit_11.text()
            if transparency != "":
                transparency = float(transparency)
                if transparency < 0 or transparency > 1:
                    raise ValueError
                d['transparency'] = transparency

            specular = self.ui.lineEdit_12.text()
            if specular != "":
                specular = float(specular)
                if specular < 0 or specular > 1:
                    raise ValueError
                d['specular'] = specular

            refraction = self.ui.lineEdit_13.text()
            if refraction != "":
                refraction = float(refraction)
                if refraction < 0 or refraction > 1:
                    raise ValueError
                d['refraction'] = refraction

            reflectivity = self.ui.lineEdit_14.text()
            if reflectivity != "":
                reflectivity = float(reflectivity)
                if reflectivity < 0 or reflectivity > 1:
                    raise ValueError
                d['reflectivity'] = reflectivity
        except ValueError:
            print("Incorrect data")
            return
        if len(d) != 0:
            self.__manager.change_object(d, index=cur_obj)
            self.draw_z()
        # print("Heyo")

    def rotate(self):
        cur_obj = self.ui.comboBox_2.currentIndex()
        if cur_obj == -1:
            print("No objects available")
            return
        try:
            data = self.ui.lineEdit_15.text()
            ox = float(data) if data != "" else 0.0
            data = self.ui.lineEdit_16.text()
            oy = float(data) if data != "" else 0.0
            data = self.ui.lineEdit_17.text()
            oz = float(data) if data != "" else 0.0
        except ValueError:
            print("Incorrect data")
            return
        if ox != 0 or oy != 0 or oz != 0:
            self.__manager.rotate(ox, oy, oz, cur_obj)
            self.draw_z()


    def scale(self):
        cur_obj = self.ui.comboBox_2.currentIndex()
        if cur_obj == -1:
            print("No objects available")
            return
        try:
            data = self.ui.lineEdit_18.text()
            kx = float(data) if data != "" else 1.0
            data = self.ui.lineEdit_19.text()
            ky = float(data) if data != "" else 1.0
            data = self.ui.lineEdit_20.text()
            kz = float(data) if data != "" else 1.0
        except ValueError:
            print("Incorrect data")
            return
        if kx != 0 or ky != 0 or kz != 0:
            self.__manager.scale(kx, ky, kz, cur_obj)
            self.draw_z()

    def move(self):
        cur_obj = self.ui.comboBox_2.currentIndex()
        if cur_obj == -1:
            print("No objects available")
            return
        try:
            data = self.ui.lineEdit_21.text()
            dx = float(data) if data != "" else 0.0
            data = self.ui.lineEdit_22.text()
            dy = float(data) if data != "" else 0.0
            data = self.ui.lineEdit_23.text()
            dz = float(data) if data != "" else 0.0
        except ValueError:
            print("Incorrect data")
            return
        if dx != 0 or dy != 0 or dz != 0:
            self.__manager.move(dx, dy, dz, cur_obj)
            self.draw_z()

    def draw_z(self):
        # obj = []

        # obj.append(Cone(150, 200, [-120.0, 3.0, -50.0], add_color=np.array([210, 0, 0])))
        # obj[-1].transparency = 0.1
        # obj[-1].reflectivity = 0.6
        # obj[-1].specular = 0.8
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_x=-40))

        # obj.append(Pyramid([300, 3, 150, 0.4, 0.0, 0.0, 1, np.array([0, 189, 0])]))
        # obj[-1].transparency = 0.4
        # obj[-1].reflectivity = 1
        # obj[-1].specular = 0.0
        # obj[-1].transform(TransformMatrix.RotateMatrix(angle_z=121, angle_x=50))

        # obj.append(Cylinder(150, 200, [0.0, 130.0, 10.0], add_color = np.array([200, 150, 0])))
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


