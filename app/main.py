# coding: utf-8
"""
@File        :   main.py
@Time        :   2024/10/16 12:14:34
@Author      :   Usercyk
@Description :   The entypoint of the program
"""
import os
from typing import Sequence

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QLocale, QTranslator
from qfluentwidgets import FluentTranslator

from views.main_window import MainWindow
from configs import cfg, Language


class EntryPoint:
    """
    Start the whole program
    """
    @classmethod
    def set_dpi(cls):
        """
        Set the dpi scale according to the configurations
        """
        if cfg.get(cfg.dpiScale) != "Auto":
            os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
            os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    @classmethod
    def run(cls, argv: Sequence[str]) -> None:
        """
        Run the program

        Args:
            argv (Sequence[str]): The parameters offered to `QApplication`
        """
        # The environment setting
        cls.set_dpi()

        # The qt app
        # ! cannot sepearte into different method
        app = QApplication(argv)
        app.setAttribute(
            Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

        # load translator into the app
        # current language and locale
        language: Language = cfg.get(cfg.language)
        locale: QLocale = language.value

        # the translator of `qfluentwidget`
        fluent_translator = FluentTranslator(locale)
        # the translator of `oj plus`
        oj_plus_translator = QTranslator()
        oj_plus_translator.load(locale, "oj_plus", ".", ":/oj_plus/i18n")

        # install translator
        app.installTranslator(fluent_translator)
        app.installTranslator(oj_plus_translator)

        # main window
        w = MainWindow()
        w.show()

        # exit when close the window
        app.exec()


if __name__ == "__main__":
    EntryPoint.run([])
