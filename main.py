import sys
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PyQt5.QtWidgets import QApplication

from MainWindow import mywindow
from PolygonalModels.Cylinder import Cylinder
from PolygonalModels.Cone import Cone


# def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # cone = Cone(2, 5, [2, 5, -2])
    # Pyramid(2, 3, 5, [1, 5, -1])
    # Cylinder(2, 5, [2, 5, -2])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')

    app = QApplication([])
    app.setStyle('Fusion')
    application = mywindow()
    application.draw_z()
    application.show()
    app.exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
