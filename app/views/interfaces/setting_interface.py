# coding: utf-8
"""
@File        :   setting_interface.py
@Time        :   2024/10/16 23:36:01
@Author      :   Usercyk
@Description :   The setting interface
"""
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import (ScrollArea, ExpandLayout, SettingCardGroup, SwitchSettingCard,
                            OptionsSettingCard, CustomColorSettingCard, ComboBoxSettingCard,
                            InfoBar, setTheme, setThemeColor)
from qfluentwidgets import FluentIcon as FIF

from configs import cfg, INTERFACE_SIZE, is_win11
from utils import StyleSheet, signal_bus


class SettingInterface(ScrollArea):
    """
    The setting interface
    """

    def __init__(self, parent) -> None:
        # super
        super().__init__(parent)
        # create widgets
        self.__create_widgets()
        # set up widgets
        self.__setup_widgets()
        # fix bugs
        self.fix_wheel_events()

    def __create_widgets(self) -> None:
        """
        Create widgets
        """
        # central widgets and layout
        self.scroll_widget = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widget)

        # setting label
        self.setting_label = QLabel(self.tr("Settings"), self)

        self.personal_group = SettingCardGroup(
            self.tr('Personalization'), self.scroll_widget)

        self.mica_card = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr('Mica effect'),
            self.tr('Apply semi transparent to windows and surfaces'),
            cfg.micaEnabled,
            self.personal_group
        )
        self.navigation_acrylic_card = SwitchSettingCard(
            FIF.TRANSPARENT,
            self.tr("Navigation acrylic effect"),
            self.tr("Apply acrylic to the side navigation bar"),
            cfg.navigationAcrylicEnabled,
            self.personal_group
        )
        self.theme_card = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personal_group
        )
        self.theme_color_card = CustomColorSettingCard(
            cfg.themeColor,
            FIF.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personal_group
        )
        self.zoom_card = OptionsSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                self.tr("Use system setting")
            ],
            parent=self.personal_group
        )
        self.language_card = ComboBoxSettingCard(
            cfg.language,
            FIF.LANGUAGE,
            self.tr('Language'),
            self.tr('Set your preferred language for UI'),
            texts=['简体中文', '繁體中文', 'English', self.tr('Use system setting')],
            parent=self.personal_group
        )

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
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scroll_widget.setObjectName('scrollWidget')
        self.setting_label.setObjectName('settingLabel')
        StyleSheet.SETTING_INTERFACE.apply(self)

        # disable the card setting
        self.mica_card.setEnabled(is_win11())

        # init layout
        self.__init_layout()
        self.__connect_signal()

    def __init_layout(self) -> None:
        """
        Init layout
        """
        self.setting_label.move(36, 30)

        self.personal_group.addSettingCard(self.mica_card)
        self.personal_group.addSettingCard(self.navigation_acrylic_card)
        self.personal_group.addSettingCard(self.theme_card)
        self.personal_group.addSettingCard(self.theme_color_card)
        self.personal_group.addSettingCard(self.zoom_card)
        self.personal_group.addSettingCard(self.language_card)

        # add setting card group to layout
        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.personal_group)

    def __connect_signal(self) -> None:
        """
        Connect signals to slots
        """
        cfg.appRestartSig.connect(self.__show_restart_tooltip)

        # personalization
        cfg.themeChanged.connect(setTheme)
        self.theme_color_card.colorChanged.connect(setThemeColor)
        self.mica_card.checkedChanged.connect(signal_bus.micaEnableChanged)
        self.navigation_acrylic_card.checkedChanged.connect(
            signal_bus.navigationAcrylicEnableChanged)

    def __show_restart_tooltip(self) -> None:
        """
        Show restart tooltip
        """
        InfoBar.success(
            self.tr('Updated successfully'),
            self.tr('Configuration takes effect after restart'),
            duration=1500,
            parent=self
        )

    def fix_wheel_events(self) -> None:
        """
        Fix wheel events
        """
        self.theme_card.wheelEvent = self.scroll_widget.wheelEvent
        self.theme_color_card.wheelEvent = self.scroll_widget.wheelEvent
        self.zoom_card.wheelEvent = self.scroll_widget.wheelEvent


# set all
__all__ = ["SettingInterface"]
