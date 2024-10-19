# coding: utf-8
"""
@File        :   home_interface.py
@Time        :   2024/10/18 16:09:18
@Author      :   Usercyk
@Description :   Home Interface
"""
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import (ScrollArea, ExpandLayout)

from configs import INTERFACE_SIZE
from utils import StyleSheet


class HomeInterface(ScrollArea):
    """
    The home interface
    """

    def __init__(self, parent) -> None:
        # super
        super().__init__(parent)
        # create widgets
        self.__create_widgets()
        # set up widgets
        self.__setup_widgets()

    def __create_widgets(self) -> None:
        """
        Create widgets
        """
        # central widgets and layout
        self.scroll_widget = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widget)

        # home label
        self.home_label = QLabel(self.tr("Home"), self)

    def __setup_widgets(self) -> None:
        """
        Set up widgets
        """
        self.resize(*INTERFACE_SIZE)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)
        self.setObjectName('homeInterface')

        # initialize style sheet
        self.scroll_widget.setObjectName('scrollWidget')
        self.home_label.setObjectName('homeLabel')
        StyleSheet.HOME_INTERFACE.apply(self)

        # init layout
        self.__init_layout()
        self.__connect_signal()

    def __init_layout(self) -> None:
        """
        Init layout
        """
        self.home_label.move(36, 30)

        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)

    def __connect_signal(self) -> None:
        """
        Connect signals to slots
        """
