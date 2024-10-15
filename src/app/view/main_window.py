# coding: utf-8
"""
@File        :   main_window.py
@Time        :   2024/10/15 11:38:15
@Author      :   Usercyk
@Description :   The main window
"""

from PySide6.QtGui import QIcon
from qfluentwidgets import FluentWindow

from ..common.setting import MIN_WIDTH, SIZE
from ..common.config import cfg
from ..resources import resource_rc  # pylint: disable=W0611


class MainWindow(FluentWindow):
    """
    The main window of the projects.
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_window()

    def init_window(self) -> None:
        """
        Init window with settings like title, size, etc.
        """
        # basic setup
        self.setWindowTitle(self.tr("OJ Plus"))
        self.resize(*SIZE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setWindowIcon(QIcon(":/oj_plus/images/favicon.png"))

        # mica
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
