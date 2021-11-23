import numpy as np
import qimage2ndarray
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QBrush, QPen, QColor, QImage, QPixmap, qRgb
from PIL import Image
from PyQt5.QtWidgets import QGraphicsScene
from numpy import inf
import copy


eps = 0.1

# добавить пропуск фигур, не видимых при рендеринге в окне
# скалярное произведение вектора нормали и взгляда (полигон), если больше нуля - не отрисовывать

class ZBufAlgorithm:
    def __init__(self, width, height):
        self.__z_buf = []
        self.__color_buf = []
        self.__borders = [round(width), round(height)]
        self.clear()

    def check_pixel_on_scene(self, pixel):
        return 0 < pixel[0] < self.__borders[0] and 0 < pixel[1] < self.__borders[1]

    def analyse_pixel(self, pixel, color):
        if 0 <= pixel[2] < self.__z_buf[pixel[0]][pixel[1]]:
            self.__z_buf[pixel[0]][pixel[1]] = pixel[2]
            self.__color_buf[pixel[0]][pixel[1]] = color[:3]

    def clear(self):
        self.__z_buf = np.array([[1.] * self.__borders[1]] * self.__borders[0])
        self.__color_buf = np.array([[np.array([0.9, 0.9, 0.9], dtype=np.float32)] * self.__borders[1]] * self.__borders[0])


    def apply(self, drawer):
        print("apply")
        drawer.apply(self.__color_buf)
        # for i in range(round(self.__scene.width())):  # OK CODE
        #     for j in range(round(self.__scene.height())):
        #         # if not np.allclose(self.__color_buf[i][j], np.array([255., 255., 255., 255.])):
        #         color = self.__color_buf[i][j]
        #         color = QColor(color[0], color[1], color[2])
        #         # self.__brush.setColor(add_color)
        #         self.__scene.addLine(i, j, i, j, QPen(color))
        print("READY")

