import os

import cv2
import numpy as np
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog

from app.image_utilities import (load_cascade, extract_faces,
                                 convert_to_colorspace)
from model.classifier import Classifier
from model.model import Model


class EmuWindow(QMainWindow):
    """
    Main class that handles graphical interface of a machine learning model
    and preprocessing of images to be classified.
    """

    __EMOTIONS = ["Anger", "Disgust", "Fear", "Happiness", "Sadness",
                  "Surprise", "Neutral"]
    __CASCADE_PATH = "data/cascades/haarcascade_frontalface_default.xml"
    __META_PATH = "data/gui/model/model.meta"
    __MODEL_PATH = "data/gui/model/model"
    __BACKGROUND_IMAGE_PATH = "data/gui/png/drop.png"

    def __init__(self):
        super().__init__()

        self.__init_model()
        self.__init_window()
        self.__init_image_frame()
        self.__init_infos()
        self.__init_buttons()
        self.__set_featured_image(path=self.__BACKGROUND_IMAGE_PATH)

    def __init_model(self):
        self.__classifier = Classifier(self.__META_PATH, self.__MODEL_PATH)
        self.__cascade = load_cascade(self.__CASCADE_PATH)
        self.__input = None
        # TODO error message

    def __init_window(self):
        self.setGeometry(300, 300, 900, 600)
        self.setWindowTitle('Emu')
        self.setAcceptDrops(True)

    def __init_image_frame(self):
        self.__image = QLabel(self)
        self.__image_url = None
        self.__image_frame = QMimeData()

    def __init_infos(self):
        self.__emotions_title = QLabel(self)
        self.__emotions_title.setText('<h2>Emotions</h2>')
        self.__emotions_title.move(650, 15)

        self.__emotions_labels = [None] * len(self.__EMOTIONS)
        self.__emotions_scores = [None] * len(self.__EMOTIONS)

        for i, emotion in enumerate(self.__EMOTIONS):
            self.__emotions_labels[i] = QLabel(self)
            self.__emotions_scores[i] = QLabel(self)
            self.__emotions_labels[i].setText('<h3>' + emotion + '</h3>')
            self.__emotions_labels[i].move(655, 45 + 20 * i)
            self.__emotions_scores[i].move(785, 45 + 20 * i)

        self.__print_scores([0.0] * len(self.__EMOTIONS))

    def __init_buttons(self):
        self.__choose_button = QPushButton('Choose image', self)
        self.__choose_button.resize(self.__choose_button.sizeHint())
        self.__choose_button.clicked.connect(self.__read_image)
        self.__choose_button.move(660, 532)

    def __load_image(self, path):
        if path:
            try:
                if not path or not os.path.exists(path):
                    raise FileNotFoundError(
                        "No such file {}".format(path))

                try:
                    image = cv2.imread(path)
                except:
                    raise ValueError("Couldn't load image")

                if image is False:
                    raise ValueError("Couldn't load image")

                self.__image_path = path
                faces = extract_faces(image)
                if len(faces) == 0:
                    raise ValueError("Couldn't find face on an image")

                # Set face as featured image in gui.
                featured_face = cv2.resize(faces[0], (512, 512))
                self.__set_featured_image(featured_face)

                # Set input for the neural net.
                self.__input = convert_to_colorspace([faces[0]], "grayscale")[0]
                self.__input = cv2.resize(self.__input, Model.INPUT_SIZE)
                self.__input = np.expand_dims(self.__input, -1)
            except Exception as e:
                self.__print_message(e)

    def __set_featured_image(self, image=None, path=None):
        if path:
            try:
                image = cv2.imread(path)
            except:
                self.__print_message("Couldn't load image")
                return

        self.__image.setGeometry(94, 40, 512, 512)
        q_image = self.__image_to__q_image(image)
        self.__image.setPixmap(QPixmap.fromImage(q_image))
        self.__print_scores([0] * len(self.__EMOTIONS))

    def __read_image(self):
        image_path = QFileDialog.getOpenFileName()[0]
        self.__analyse_image(image_path)

    def __analyse_image(self, image_path):
        self.__load_image(image_path)
        if self.__input is not None:
            scores = self.__classifier.infer([self.__input])[0]
            self.__print_scores(scores)
        else:
            # TODO error message
            pass

    def __image_to__q_image(self, image):
        height, width, _ = image.shape
        bytes_per_line = 3 * width
        return QImage(image.data, width, height, bytes_per_line,
                      QImage.Format_RGB888)

    def __print_scores(self, scores):
        for label, score in zip(self.__emotions_scores, scores):
            label.setText('<h3>' + str('%.2f' % (score * 100) + ' %</h3>'))

    def __print_message(self, message):
        #TODO gui label with messages
        print(message)

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.__draw_frame(painter)
        painter.end()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasImage():
            event.accept()
        else:
            print(event.mimeData())
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage():
            pass
        else:
            path = event.mimeData().urls()[0].toLocalFile()
            self.__analyse_image(path)

    def __draw_frame(self, painter):
        col = QColor(0, 0, 0)
        painter.setPen(col)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(89, 35, 522, 522)
        painter.drawRect(94, 40, 512, 512)

    def closeEvent(self, event):
        self.__classifier.close()
        event.accept()
