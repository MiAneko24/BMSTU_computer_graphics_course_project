import numpy as np
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QBrush, QColor, QPalette, QPen
from PyQt5.QtWidgets import QGraphicsScene, QColorDialog, QVBoxLayout

from Camera import Camera
from Cone import Cone
from Cylinder import Cylinder
from Drawer import Drawer
from LightSource import LightSource
from ObjectType import ObjectType
from PolygonalModels.Pyramid import Pyramid
from PyQt5 import QtWidgets
from PolygonalModels.interface import Ui_MainWindow
from RayTracingAlgorithm import RayTracingAlgorithm
from SceneManager import SceneManager
from Shader import Shader
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
        self.__scene.setSceneRect(QRectF(0, 0, 250, 250))
        self.ui.graphicsView.setScene(self.__scene)
        # self.ui.graphicsView.fitInView(QRectF(0, 0, 530, 540))
        self.__brush = QBrush(Qt.black)
        self.ui.pushButton.clicked.connect(self.click_adding_obj_color_btn)
        self.ui.pushButton_3.clicked.connect(self.click_new_color_btn)
        self.ui.pushButton_9.clicked.connect(self.move_camera)
        self.ui.pushButton_10.clicked.connect(self.rotate_camera)
        self.__z_buf = ZBufAlgorithm(self.__scene.width(), self.__scene.height())
        width = self.__scene.width()
        height = self.__scene.height()
        self.__cam = Camera(width=width, height=height,
                            pos=np.array([0., 0., 300.]))
        self.__light = LightSource(Vertex([0, 50,150]))
        self.__shader = Shader(self.__z_buf, self.__light, self.__cam, width, height)
        self.add_color = QColor(0., 0., 255.)
        self.new_color = QColor("white")
        self.diffuse_color = QColor("white")
        self.specular_color = QColor("white")
        self.ambient_color = QColor("white")
        self.diffuse_obj_color = QColor("white")
        self.specular_obj_color = QColor("white")
        self.new_diffuse_obj_color = QColor("white")
        self.new_specular_obj_color = QColor("white")

        # lay = QVBoxLayout(self)
        # lay.addWidget(self.ui.pushButton)
        self.palette = self.ui.pushButton.palette()
        self.palette.setColor(QPalette.Button, self.add_color)
        self.ui.pushButton.setPalette(self.palette)

        self.add_color_dialog = QColorDialog(self)
        self.add_color_dialog.currentColorChanged.connect(self.change_add_color)
        self.ui.pushButton_2.clicked.connect(self.add_object)

        self.new_palette = self.ui.pushButton_3.palette()
        self.new_palette.setColor(QPalette.Button, self.new_color)
        self.ui.pushButton_3.setPalette(self.new_palette)

        self.new_color_dialog = QColorDialog(self)
        self.new_color_dialog.currentColorChanged.connect(self.change_new_color)
        self.ui.pushButton_4.clicked.connect(self.change_params)

        self.diffuse_palette = self.ui.pushButton_12.palette()
        self.diffuse_palette.setColor(QPalette.Button, self.diffuse_color)
        self.ui.pushButton_12.setPalette(self.diffuse_palette)

        self.diffuse_light_dialog = QColorDialog(self)
        self.diffuse_light_dialog.currentColorChanged.connect(self.diffuse_light_color)
        self.ui.pushButton_12.clicked.connect(self.click_diffuse_light_color_btn)

        self.specular_palette = self.ui.pushButton_13.palette()
        self.specular_palette.setColor(QPalette.Button, self.specular_color)
        self.ui.pushButton_13.setPalette(self.specular_palette)

        self.specular_light_dialog = QColorDialog(self)
        self.specular_light_dialog.currentColorChanged.connect(self.specular_light_color)
        self.ui.pushButton_13.clicked.connect(self.click_specular_light_color_btn)

        self.ambient_palette = self.ui.pushButton_14.palette()
        self.ambient_palette.setColor(QPalette.Button, self.ambient_color)
        self.ui.pushButton_14.setPalette(self.ambient_palette)

        self.ambient_light_dialog = QColorDialog(self)
        self.ambient_light_dialog.currentColorChanged.connect(self.ambient_light_color)
        self.ui.pushButton_14.clicked.connect(self.click_ambient_light_color_btn)

        self.ui.pushButton_15.clicked.connect(self.change_light_params)

        self.diffuse_obj_palette = self.ui.pushButton_16.palette()
        self.diffuse_obj_palette.setColor(QPalette.Button, self.diffuse_obj_color)
        self.ui.pushButton_16.setPalette(self.diffuse_obj_palette)

        self.diffuse_obj_dialog = QColorDialog(self)
        self.diffuse_obj_dialog.currentColorChanged.connect(self.set_diffuse_obj_color)
        self.ui.pushButton_16.clicked.connect(self.click_diffuse_obj_color_btn)

        self.specular_obj_palette = self.ui.pushButton_17.palette()
        self.specular_obj_palette.setColor(QPalette.Button, self.specular_obj_color)
        self.ui.pushButton_17.setPalette(self.specular_obj_palette)

        self.specular_obj_dialog = QColorDialog(self)
        self.specular_obj_dialog.currentColorChanged.connect(self.set_specular_obj_color)
        self.ui.pushButton_17.clicked.connect(self.click_specular_obj_color_btn)

        self.new_diffuse_obj_palette = self.ui.pushButton_18.palette()
        self.new_diffuse_obj_palette.setColor(QPalette.Button, self.new_diffuse_obj_color)
        self.ui.pushButton_18.setPalette(self.new_diffuse_obj_palette)

        self.new_diffuse_obj_dialog = QColorDialog(self)
        self.new_diffuse_obj_dialog.currentColorChanged.connect(self.set_new_diffuse_obj_color)
        self.ui.pushButton_18.clicked.connect(self.click_new_diffuse_obj_color_btn)

        self.new_specular_obj_palette = self.ui.pushButton_19.palette()
        self.new_specular_obj_palette.setColor(QPalette.Button, self.new_specular_obj_color)
        self.ui.pushButton_19.setPalette(self.new_specular_obj_palette)

        self.new_specular_obj_dialog = QColorDialog(self)
        self.new_specular_obj_dialog.currentColorChanged.connect(self.set_new_specular_obj_color)
        self.ui.pushButton_19.clicked.connect(self.click_new_specular_obj_color_btn)

        self.ui.pushButton_5.clicked.connect(self.rotate)

        self.ui.pushButton_6.clicked.connect(self.scale)
        self.ui.pushButton_7.clicked.connect(self.move)
        self.ui.pushButton_8.clicked.connect(self.delete)
        self.ui.pushButton_11.clicked.connect(self.render)
        # self.__z_buf.apply(Drawer(self.__scene))

        self.__ray = RayTracingAlgorithm(round(self.__scene.width()), round(self.__scene.height()), self.__cam)
        # self.__manager.add_object(ObjectType.cone, [150, 200, 0, 0.1, 0.6, 0.8, 0.8,np.array([210, 0, 0])])

        # self.__manager.add_object(ObjectType.cone, [20, 10, 0, 0.0, 0.5, 0.0, 0.5, np.array([210, 0, 0])])
        self.add_object()
        # self.draw_z()

    def click_diffuse_obj_color_btn(self):
        self.diffuse_obj_dialog.exec()
        self.diffuse_obj_palette.setColor(QPalette.Button, self.diffuse_obj_color)
        self.ui.pushButton_16.setPalette(self.diffuse_obj_palette)

    def set_diffuse_obj_color(self, color):
        self.diffuse_obj_color = color

    def click_specular_obj_color_btn(self):
        self.specular_obj_dialog.exec()
        self.specular_obj_palette.setColor(QPalette.Button, self.specular_obj_color)
        self.ui.pushButton_17.setPalette(self.specular_obj_palette)

    def set_specular_obj_color(self, color):
        self.specular_obj_color = color

    def click_new_diffuse_obj_color_btn(self):
        self.new_diffuse_obj_dialog.exec()
        self.new_diffuse_obj_palette.setColor(QPalette.Button, self.new_diffuse_obj_color)
        self.ui.pushButton_18.setPalette(self.new_diffuse_obj_palette)

    def set_new_diffuse_obj_color(self, color):
        self.new_diffuse_obj_color = color

    def click_new_specular_obj_color_btn(self):
        self.new_specular_obj_dialog.exec()
        self.new_specular_obj_palette.setColor(QPalette.Button, self.new_specular_obj_color)
        self.ui.pushButton_19.setPalette(self.new_specular_obj_palette)

    def set_new_specular_obj_color(self, color):
        self.new_specular_obj_color = color


    def change_light_params(self):
        self.__light.diffuse_light = np.array(self.diffuse_color.getRgbF())
        self.__light.specular_light = np.array(self.specular_color.getRgbF())
        self.__light.ambient_light = np.array(self.ambient_color.getRgbF())
        self.draw_z()

    def click_diffuse_light_color_btn(self):
        self.diffuse_light_dialog.exec()
        self.diffuse_palette.setColor(QPalette.Button, self.diffuse_color)
        self.ui.pushButton_12.setPalette(self.diffuse_palette)

    def diffuse_light_color(self, color):
        self.diffuse_color = color

    def click_specular_light_color_btn(self):
        self.specular_light_dialog.exec()
        self.specular_palette.setColor(QPalette.Button, self.specular_color)
        self.ui.pushButton_13.setPalette(self.specular_palette)

    def specular_light_color(self, color):
        self.specular_color = color

    def click_ambient_light_color_btn(self):
        self.ambient_light_dialog.exec()
        self.ambient_palette.setColor(QPalette.Button, self.ambient_color)
        self.ui.pushButton_14.setPalette(self.ambient_palette)

    def ambient_light_color(self, color):
        self.ambient_color = color

    def render(self):
        self.__ray.start_algorithm(self.__manager.objects, self.__light)
        self.__ray.apply(Drawer(self.__scene))

    def move_camera(self):
        params = dict()
        try:
            forward = self.ui.lineEdit_24.text()
            if forward != "":
                forward = float(forward)
                if forward < 0:
                    raise ValueError
                if forward != 0:
                    params['forward'] = forward

            print("passed 1")

            back = self.ui.lineEdit_25.text()
            if back != "":
                back = float(back)
                if back < 0 or ('forward' in params.keys() and back !=0):
                    raise ValueError
                if back != 0:
                    params['back'] = back

            print("passed 2")

            right = self.ui.lineEdit_26.text()
            if right != "":
                right = float(right)
                if right < 0:
                    raise ValueError
                if right != 0:
                    params['right'] = right

            left = self.ui.lineEdit_27.text()
            if left != "":
                left = float(left)
                if left < 0 or ("right" in params.keys() and left != 0):
                    raise ValueError
                if left != 0:
                    params['left'] = left

            up = self.ui.lineEdit_28.text()
            if up != "":
                up = float(up)
                if up < 0:
                    raise ValueError
                if up != 0:
                    params['up'] = up

            down = self.ui.lineEdit_29.text()
            if down != "":
                down = float(down)
                if down < 0 or ("up" in params.keys() and down != 0):
                    raise ValueError
                if down != 0:
                    params['down'] = down

        except ValueError:
            return

        if len(params) > 0:
            self.__cam.move(params)
            self.draw_z()

    def rotate_camera(self):
        params = dict()
        try:
            right = self.ui.lineEdit_30.text()
            if right != "":
                right = float(right)
                if right < 0:
                    raise ValueError
                if right != 0:
                    params['right'] = right

            left = self.ui.lineEdit_31.text()
            if left != "":
                left = float(left)
                if left < 0 or ("right" in params.keys() and left != 0):
                    raise ValueError
                if left != 0:
                    params['left'] = left

            up = self.ui.lineEdit_32.text()
            if up != "":
                up = float(up)
                if up < 0:
                    raise ValueError
                if up != 0:
                    params['up'] = up

            down = self.ui.lineEdit_33.text()
            if down != "":
                down = float(down)
                if down < 0 or ("up" in params.keys() and down != 0):
                    raise ValueError
                if down != 0:
                    params['down'] = down

        except ValueError:
            return

        if len(params) != 0:
            self.__cam.rotate(params)
            self.draw_z()

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
        # cur_obj = self.ui.comboBox_2.currentIndex()
        # if cur_obj == -1:
        #     return
        # params = dict(color=np.array(self.new_color.getRgbF(), dtype=np.float32))
        # # params['color'] = np.concatenate((params['color'][-1:], params['color'][:-1]))
        # self.__manager.change_object(params, index=cur_obj)
        # self.draw_z()
        #send ColorCommand

    def change_new_color(self, color):
        self.new_color = color

    def delete(self):
        cur_obj = self.ui.comboBox_2.currentIndex()
        if cur_obj == -1:
            return
        objects = []
        for i in range(self.ui.comboBox_2.count()):
            if cur_obj != i:
                objects.append(self.ui.comboBox_2.itemText(i).removeprefix("Object " + str(i + 1)))
        self.ui.comboBox_2.clear()
        for i in range(len(objects)):
            self.ui.comboBox_2.addItem("Object " + str(self.ui.comboBox_2.count() + 1) + objects[i])
        self.__manager.delete(cur_obj)
        self.draw_z()

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
            params.append(np.array(self.specular_obj_color.getRgbF()))
            # if params[-1] < 0 or params[-1] > 1:
            #     raise ValueError
            print("passed 5")
            params.append(float(self.ui.lineEdit_6.text()))
            if params[-1] < 0 or params[-1] > 1:
                raise ValueError
            print("passed 6")
            params.append(np.array(self.diffuse_obj_color.getRgbF()))

            print("passed 7")
            params.append(np.array(self.add_color.getRgbF(), dtype=np.float32))
            print(params[-1])
        except ValueError:
            return

        str_type = "Конус" if obj_type is ObjectType.cone else "Цилиндр" if obj_type is ObjectType.cylinder else "Пирамида"
        label = "Object " + str(self.ui.comboBox_2.count() + 1) + "(" + str_type + ")"
        # Ввод и проверка данных! Ну и мб исчезновение строки ввода длины стороны/радиуса в зависимости от фигуры
        try:
            self.__manager.add_object(obj_type, params)
        except AttributeError:
            print("error")
            return
        self.ui.comboBox_2.addItem(label)
        self.draw_z()

    def change_params(self):
        cur_obj = self.ui.comboBox_2.currentIndex()
        if cur_obj == -1:
            print("No objects available")
            return
        d = dict()
        try:
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
                n = int(n)
                if n < 0:
                    raise ValueError
                d['n'] = n

            transparency = self.ui.lineEdit_11.text()
            if transparency != "":
                transparency = float(transparency)
                if transparency < 0 or transparency > 1:
                    raise ValueError
                d['transparency'] = transparency

            specular = np.array(self.new_specular_obj_color.getRgbF())
            d['specular'] = specular

            specular_exp = self.ui.lineEdit_13.text()
            if specular_exp != "":
                specular_exp = float(specular_exp)
                if specular_exp < 0 or specular_exp > 1:
                    raise ValueError
                d['specular_exp'] = 1 - specular_exp

            diffuse = np.array(self.new_diffuse_obj_color.getRgbF())
            d['diffuse'] = diffuse
            color = np.array(self.new_color.getRgbF())
            d['color'] = color
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

        # self.__algorithm.clear()


        print("Start")
        self.__z_buf.clear()
        for i in self.__manager.objects:
            i.accept(self.__shader)
        self.__z_buf.apply(Drawer(self.__scene))
        # for obj in self.__manager.objects:
        #     polygons = self.__shader.get_polygons_with_vertices(obj)
        #     # polygons = self.__cam.get_polygons_projection(polygons, obj.normals)
        #     for pol in polygons:
        #         # pol = polygons[0]
        #         pol = [self.__cam.get_projection(vert) for vert in pol]
        #         for k in range(3):
        #             self.__scene.addLine(pol[k - 1].x, pol[k - 1].y, pol[k].x, pol[k].y, QPen(QColor("red")))
        # #
        # self.ui.graphicsView.viewport().update()


        # algorithm.draw(obj)


