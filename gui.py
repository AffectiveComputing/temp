"""
This module contains class responsible for graphics user interface.
"""


import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from os import path


__author__ = "Michał Górecki"


class Gui(tk.Frame):
    """
    Class, which represents modified tkinter gui frame.
    """

    # Window title.
    __WINDOW_TITLE = "Emotion recognition"
    # Window dimension constants.
    __WINDOW_WIDTH = 800
    __WINDOW_HEIGHT = 600
    # Image label constant size.
    __PREVIEW_WIDTH = 500
    __PREVIEW_HEIGHT = 500

    def __init__(self, master):
        super().__init__(master)
        self.master.wm_title(self.__WINDOW_TITLE)
        self.master.geometry(
            "{}x{}".format(self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT)
        )
        self.__setup_layout()
        self.__create_widgets()

    def __setup_layout(self):
        """
        Setups frames necessary to create layout and configures their sizes.
        :return: -
        """
        # Configure two columns of main frame.
        self.grid(row=0, column=0)
        self.grid_columnconfigure(0, minsize=0.75 * self.__WINDOW_WIDTH)
        self.grid_columnconfigure(1, minsize=0.25 * self.__WINDOW_WIDTH)
        self.grid_rowconfigure(0, minsize=self.__WINDOW_HEIGHT)
        # Create and configure side toolbox.
        self.__toolbox = tk.Frame(self)
        self.__toolbox.grid(column=1, sticky="news")
        self.__toolbox.grid_rowconfigure(
            0, minsize=0.25 * self.__WINDOW_HEIGHT
        )
        self.__toolbox.grid_rowconfigure(
            1, minsize=0.75 * self.__WINDOW_HEIGHT
        )
        self.__toolbox.grid_columnconfigure(
            0, minsize=0.25 * self.__WINDOW_WIDTH
        )
        # Create and configure buttons and results frames.
        self.__buttons = tk.Frame(self.__toolbox)
        self.__buttons.grid(row=0, sticky="news")
        self.__buttons.grid_rowconfigure(
            0, minsize=0.5 * 0.25 * self.__WINDOW_HEIGHT
        )
        self.__buttons.grid_rowconfigure(
            1, minsize=0.5 * 0.25 * self.__WINDOW_HEIGHT
        )
        self.__buttons.grid_columnconfigure(
            0, minsize=0.25 * self.__WINDOW_WIDTH
        )
        self.__results = tk.Frame(self.__toolbox)
        self.__results.grid(row=1, sticky="news")

    def __create_widgets(self):
        """

        :return:
        """
        # Create image label and fill it with empty image.
        self.__image = tk.Label(self, borderwidth=2, relief="solid")
        empty_image = ImageTk.PhotoImage(
            Image.new(
                "RGB", (self.__PREVIEW_WIDTH, self.__PREVIEW_HEIGHT),
                (255, 255, 255)
            )
        )
        self.__image.config(image=empty_image)
        self.__image.image = empty_image
        self.__image.grid(row=0, column=0)
        # Setup control buttons.
        self.__open_image_button = tk.Button(
            self.__buttons, text="Open Image", command=self.__open_image
        )
        self.__open_image_button.grid(row=0)
        self.__analyze_button = tk.Button(
            self.__buttons, text="Analyze", command=self.__analyze_image
        )
        self.__analyze_button.grid(row=1)
        # Setup results text.
        # ...

    def __open_image(self):
        """
        Handle open image button press.
        :return: -
        """
        image_path = askopenfilename()
        if image_path and path.isfile(image_path):
            image = self.__load_image(image_path)
            self.__image.config(image=image)
            self.__image.image = image

    def __load_image(self, path):
        """
        Load image from file with given path.
        :param path: path of source image file
        :return: loaded tk image
        """
        image = Image.open(path).resize(
            (self.__PREVIEW_WIDTH, self.__PREVIEW_HEIGHT), Image.ANTIALIAS
        )
        return ImageTk.PhotoImage(image)

    def __analyze_image(self):
        """
        Analyze loaded image with conv-net and display results.
        :return: -
        """
        pass

    def __set_results(self):
        """
        Set results labels to given values.
        :return: -
        """
        pass


def main():
    """
    Example usage of gui class.
    :return: -
    """
    root = tk.Tk()
    gui = Gui(master=root)
    gui.mainloop()


if __name__ == "__main__":
    main()