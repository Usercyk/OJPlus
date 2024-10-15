# coding: utf-8
# OJ Plus
# Copyright (C) 2024 UserCyk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
@File        :   main.py
@Time        :   2024/10/15 11:27:43
@Author      :   Usercyk
@Description :   The entrypoint of the project
"""
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QLocale, QTranslator
from qfluentwidgets import FluentTranslator

from app.view.main_window import MainWindow
from app.common.config import Language, cfg


class EntryPoint:
    """
    The entrypoint of the project
    """
    @staticmethod
    def set_dpi() -> None:
        """
        Set the dpi according to the config
        """
        if cfg.get(cfg.dpiScale) != "Auto":
            os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
            os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    @staticmethod
    def run() -> None:
        """
        Run the project
        """
        # set dpi in the os environment
        EntryPoint.set_dpi()

        # initialize the qapp
        app = QApplication([])
        # only one main window in one program
        app.setAttribute(
            Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

        # set translator according to the language
        language: Language = cfg.get(cfg.language)
        locale: QLocale = language.value
        # the translator for fluent widgets
        fluent_translator = FluentTranslator(locale)
        # the translator for this project
        oj_plus_translator = QTranslator()
        oj_plus_translator.load(locale, "oj_plus", ".", ":/oj_plus/i18n")

        # install the translator
        app.installTranslator(fluent_translator)
        app.installTranslator(oj_plus_translator)

        # show the main window
        w = MainWindow()
        w.show()

        # exit when the qapp stops
        app.exec()


if __name__ == "__main__":
    EntryPoint.run()
