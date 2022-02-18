"""   
    @update: 2021.05.14
"""

import sys, time, os
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QListWidget,QListWidgetItem,QListView,QWidget,QApplication,QHBoxLayout,QLabel
from PyQt5.QtCore import *
import datetime
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s [%(filename)s:%(lineno)d] - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


logger = logging.getLogger(__name__)
PhotoDir = os.path.expanduser('photo')

class ImageListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super(ImageListWidget, self).__init__()
        self.setFlow(QtWidgets.QListView.Flow(1))#0: left to right,1: top to bottom
        self.setIconSize(QSize(80,60))

    def add_image_items(self,image_paths=[]):
        self.clear()
        for img_path in image_paths:
            if os.path.isfile(img_path):
                img_name = os.path.splitext(os.path.basename(img_path))[0]
                item = QListWidgetItem(QIcon(img_path),img_name)
                self.addItem(item)

class ShowLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.full = False
        self.resize(550,400)
        self.__width = self.width()
        self.__height = self.height()

    def mouseDoubleClickEvent(self, event):
        print('double_click {}'.format(event))
        if self.full is False:
            print('full')
            self.full = True
            # self.setWindowFlags(Qt.Dialog)
            self.setWindowFlags(Qt.Window)
            # self.show()
            self.showFullScreen()
        else:
            print('normal')
            self.full = False
            # self.setWindowFlag(Qt.Window, False)
            self.setWindowFlags(Qt.SubWindow)
            self.showNormal()
            self.resize(self.__width, self.__height)
            # self.show()

class ImageViewerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.list_widget = ImageListWidget()
        self.list_widget.setMinimumWidth(250)
        self.show_label = ShowLabel()
        self.image_paths = []
        self.currentImgIdx = 0
        self.currentImg = None

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.show_label)
        self.layout.addWidget(self.list_widget)

        self.list_widget.itemSelectionChanged.connect(self.loadImage)

    def load_from_paths(self,img_paths=[]):
        self.image_paths = img_paths
        self.list_widget.add_image_items(img_paths)

    def loadImage(self):
        self.currentImgIdx = self.list_widget.currentIndex().row()
        if self.currentImgIdx in range(len(self.image_paths)):
            self.currentImg = QPixmap(self.image_paths[self.currentImgIdx]).scaledToHeight(400)
            self.show_label.setPixmap(self.currentImg)

def load_image_dir(dir_path, exts=['jpg']):
    files = os.listdir(dir_path)
    files.sort()
    paths = []
    for f in files:
        for ext in exts:
            if ext in f:
                paths.append(os.path.join(dir_path, f))
    return paths

class EventTypes:
    """Stores a string name for each event type.

    With PySide2 str() on the event type gives a nice string name,
    but with PyQt5 it does not. So this method works with both systems.
    """

    def __init__(self):
        """Create mapping for all known event types."""
        self.string_name = {}
        for name in vars(QEvent):
            attribute = getattr(QEvent, name)
            if type(attribute) == QEvent.Type:
                self.string_name[attribute] = name

    def as_string(self, event: QEvent.Type) -> str:
        """Return the string name for this event."""
        try:
            return self.string_name[event]
        except KeyError:
            return f"UnknownEvent:{event}"


# Example Usage
event_str = EventTypes().as_string(QEvent.UpdateRequest)

def eventFilter(obj, event, **kwargs):
    if event.type() != 12 and event.type() != 77 and event.type() != 76:
        print(obj.objectName(), EventTypes().as_string(event.type()))
    return False

if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.eventFilter = eventFilter
    # app.installEventFilter(app)
    # win = MainWindow()
    # win.show()
    photo_widget = ImageViewerWidget()
    img_paths = load_image_dir(PhotoDir)
    photo_widget.load_from_paths(img_paths)
    photo_widget.show()
    sys.exit(app.exec_())
