import qimage2ndarray
from PyQt5.QtGui import QPixmap, QPixmapCache, QImage
from PyQt5.QtWidgets import QGraphicsPixmapItem


class Drawer:
    def __init__(self, scene):
        self.__scene = scene

    def apply(self, color_buf):
        # items = self.__scene.items()
        # pm = None
        # for item in items:
        #     if type(item) == QGraphicsPixmapItem:
        #         pm = item
        #         continue
        #     self.__scene.removeItem(item)
        self.__scene.clear()
        QPixmapCache.clear()


        # print(self.__color_buf[700][500])
        # buf = np.require(self.__color_buf, np.uint8, 'C')
        buf = color_buf.transpose(1, 0, 2)
        # buf = np.rot90(np.rot90(np.rot90(buf)))
        # img = Image.fromarray(self.__color_buf).convert('RGB')
        # img = QImage(buf, len(buf), len(buf[0]), len(buf) * 3 + 1, QImage.Format_RGB888)
        img = qimage2ndarray.array2qimage(buf, normalize=1)
        print(img.pixelColor(250, 170).getRgbF())
        print(img.save(".\\check.jpg"))
        # if not pm is None:
        #     pm = QPixmap.fromImage(img)
        #     self.__scene.update()

        # else:
        self.__scene.addItem(QGraphicsPixmapItem(QPixmap(QImage(img))))