# coding: utf-8
"""
@File        :   main_window.py
@Time        :   2024/10/16 13:44:22
@Author      :   Usercyk
@Description :   The main window
"""
from typing import override
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, QTimer
from PySide6.QtWidgets import QApplication
from qfluentwidgets import (FluentWindow, SplashScreen,
                            SystemThemeListener, NavigationItemPosition, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF

from views.interfaces import SettingInterface
from configs import SIZE, MIN_WIDTH, ICON_SIZE, cfg
from utils import signal_bus
from resources import resource_rc  # pylint: disable=W0611


class MainWindow(FluentWindow):
    """
    The main window
    """

    def __init__(self) -> None:
        # super
        super().__init__()
        # init window
        self.init_window()
        # create theme listener
        self.theme_listener = SystemThemeListener(self)
        # create sub interface
        self.create_sub_interface()
        # set acrylic effect
        self.navigationInterface.setAcrylicEnabled(
            cfg.get(cfg.navigationAcrylicEnabled))
        # connect signals
        self.connect_signals()
        # init sub interfaces
        self.init_navigations()
        # finish splash screen
        self.splash_screen.finish()
        # start theme listener
        self.theme_listener.start()

    def connect_signals(self) -> None:
        """
        Create signals to slots
        """
        signal_bus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signal_bus.navigationAcrylicEnableChanged.connect(
            self.navigationInterface.setAcrylicEnabled)

    def create_sub_interface(self) -> None:
        """
        Create and set sub interface
        """
        self.setting_interface = SettingInterface(self)

    def init_navigations(self) -> None:
        """
        Init navigations, the sub interfaces
        """
        self.addSubInterface(self.setting_interface, FIF.SETTING, self.tr(
            'Settings'), NavigationItemPosition.BOTTOM)

    def init_window(self) -> None:
        """
        Init layouts and widgets
        """
        # basic setting
        self.setWindowTitle(self.tr("OJ Plus"))
        self.resize(*SIZE)
        self.setMinimumWidth(MIN_WIDTH)
        self.setWindowIcon(QIcon(":/oj_plus/images/favicon.png"))

        # bug-fix: auto set mica true
        self.reset_mica_effect()

        # init splash screen
        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(*ICON_SIZE))
        self.splash_screen.raise_()

        # move to center
        self.move_to_center()

        # show the splash screen first
        # finish the splash screen and process that event later
        self.show()
        QApplication.processEvents()

    def move_to_center(self) -> None:
        """
        Move the main window to the center of the first screen
        """
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    @override
    def resizeEvent(self, e):
        """
        Resize the splash screen
        """
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splash_screen.resize(self.size())

    @override
    def closeEvent(self, e):
        """
        Stop listener when closing
        """
        self.theme_listener.terminate()
        self.theme_listener.deleteLater()
        super().closeEvent(e)

    @override
    def _onThemeChangedFinished(self):
        """
        Set mica effect every time the theme changes
        """
        super()._onThemeChangedFinished()

        # retry
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(
                self.winId(), isDarkTheme()))

    def reset_mica_effect(self) -> None:
        """
        Reset mica effect
        """
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))
