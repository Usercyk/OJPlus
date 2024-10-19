# coding: utf-8
"""
@File        :   judge_interface.py
@Time        :   2024/10/19 14:33:34
@Author      :   Usercyk
@Description :   The judge machine interface
"""

from PySide6.QtWidgets import (QWidget, QLabel, QHBoxLayout,
                               QVBoxLayout, QFileDialog)
from PySide6.QtCore import Qt
from qfluentwidgets import (ScrollArea, ExpandLayout, BodyLabel,
                            ComboBox, LineEdit, PrimaryPushButton)

from configs import INTERFACE_SIZE, SUPPORT_LANGUAGE
from utils import StyleSheet


class JudgeInterface(ScrollArea):
    """
    The judge interface
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

        # judge label
        self.judge_label = QLabel(self.tr("Judge"), self)

        # setting
        self.setting_widget = QWidget(self.scroll_widget)
        self.setting_layout = QVBoxLayout(self.setting_widget)

        self.choose_language_widget = QWidget(self.setting_widget)
        self.choose_language_layout = QHBoxLayout(self.choose_language_widget)
        self.choose_language_label = BodyLabel(
            self.tr("Language: "), self.choose_language_widget)
        self.choose_language_combobox = ComboBox(self.choose_language_widget)

        self.input_directory_widget = QWidget(self.setting_widget)
        self.input_directory_layout = QHBoxLayout(self.input_directory_widget)
        self.input_directory_label = BodyLabel(
            self.tr("Input directory:    "), self.input_directory_widget)
        self.input_directory_edit = LineEdit(self.input_directory_widget)
        self.input_directory_button = PrimaryPushButton(
            self.tr("Choose folder"), self.input_directory_widget)

        self.output_directory_widget = QWidget(self.setting_widget)
        self.output_directory_layout = QHBoxLayout(
            self.output_directory_widget)
        self.output_directory_label = BodyLabel(
            self.tr("Output directory: "), self.output_directory_widget)
        self.output_directory_edit = LineEdit(self.output_directory_widget)
        self.output_directory_button = PrimaryPushButton(
            self.tr("Choose folder"), self.output_directory_widget)

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
        self.setObjectName('judgeInterface')

        # set up sub widgets
        self.setting_widget.setMaximumHeight(210)

        self.choose_language_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.choose_language_combobox.addItems(SUPPORT_LANGUAGE)

        # initialize style sheet
        self.scroll_widget.setObjectName('scrollWidget')
        self.judge_label.setObjectName('judgeLabel')
        StyleSheet.JUDGE_INTERFACE.apply(self)

        # init layout
        self.__init_layout()
        self.__connect_signal()

    def __init_layout(self) -> None:
        """
        Init layout
        """
        self.judge_label.move(36, 30)

        self.input_directory_layout.setSpacing(10)
        self.input_directory_layout.setContentsMargins(0, 0, 0, 5)
        self.input_directory_layout.addWidget(self.input_directory_label)
        self.input_directory_layout.addWidget(self.input_directory_edit)
        self.input_directory_layout.addWidget(self.input_directory_button)

        self.output_directory_layout.setSpacing(10)
        self.output_directory_layout.setContentsMargins(0, 0, 0, 5)
        self.output_directory_layout.addWidget(self.output_directory_label)
        self.output_directory_layout.addWidget(self.output_directory_edit)
        self.output_directory_layout.addWidget(self.output_directory_button)

        self.choose_language_layout.setSpacing(10)
        self.choose_language_layout.setContentsMargins(0, 0, 0, 5)
        self.choose_language_layout.addWidget(self.choose_language_label)
        self.choose_language_layout.addWidget(self.choose_language_combobox)

        self.setting_layout.addWidget(self.input_directory_widget)
        self.setting_layout.addWidget(self.output_directory_widget)
        self.setting_layout.addWidget(self.choose_language_widget)

        self.setting_widget.adjustSize()

        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.setting_widget)

    def __connect_signal(self) -> None:
        """
        Connect signals to slots
        """
        self.input_directory_button.clicked.connect(
            self.__on_input_directory_button_clicked)
        self.output_directory_button.clicked.connect(
            self.__on_output_directory_button_clicked)

    def __on_input_directory_button_clicked(self) -> None:
        """
        Set text when press button
        """
        cur = self.input_directory_edit.text()
        path = QFileDialog.getExistingDirectory(
            self, self.tr("Choose input directory"), cur)
        if not path:
            return
        self.input_directory_edit.setText(path)

    def __on_output_directory_button_clicked(self) -> None:
        """
        Set text when press button
        """
        cur = self.output_directory_edit.text()
        path = QFileDialog.getExistingDirectory(
            self, self.tr("Choose output directory"), cur)
        if not path:
            return
        self.output_directory_edit.setText(path)
