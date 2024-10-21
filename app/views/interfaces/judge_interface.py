# coding: utf-8
"""
@File        :   judge_interface.py
@Time        :   2024/10/19 14:33:34
@Author      :   Usercyk
@Description :   The judge machine interface
"""

from PySide6.QtWidgets import (QWidget, QLabel, QHBoxLayout,
                               QVBoxLayout, QFileDialog, QSizePolicy)
from PySide6.QtCore import Qt
from qfluentwidgets import (ScrollArea, ExpandLayout, BodyLabel,
                            ComboBox, LineEdit, PrimaryPushButton)

from configs import INTERFACE_SIZE, SUPPORT_LANGUAGE, cfg
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

        self.language_file_widget = QWidget(self.setting_widget)
        self.language_file_layout = QHBoxLayout(self.language_file_widget)
        self.choose_language_label = BodyLabel(
            self.tr("Language: "), self.language_file_widget)
        self.choose_language_combobox = ComboBox(self.language_file_widget)
        self.choose_file_label = BodyLabel(
            self.tr("Code File: "), self.language_file_widget)
        self.choose_file_combobox = ComboBox(self.language_file_widget)
        self.choose_file_button = PrimaryPushButton(
            self.tr("Choose file"), self.language_file_widget)

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

        self.choose_language_combobox.addItems(SUPPORT_LANGUAGE)
        self.choose_file_combobox.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.choose_file_combobox.addItem(self.tr("Submit with plain text"))
        self.choose_file_combobox.addItem(self.tr("<Empty File>"))

        self.input_directory_edit.setText(cfg.get(cfg.input_directory))
        self.output_directory_edit.setText(cfg.get(cfg.output_directory))

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

        self.language_file_layout.setSpacing(10)
        self.language_file_layout.setContentsMargins(0, 0, 0, 5)
        self.language_file_layout.addWidget(self.choose_language_label)
        self.language_file_layout.addWidget(self.choose_language_combobox)
        self.language_file_layout.addSpacing(5)
        self.language_file_layout.addWidget(self.choose_file_label)
        self.language_file_layout.addWidget(self.choose_file_combobox)
        self.language_file_layout.addWidget(self.choose_file_button)

        self.setting_layout.addWidget(self.input_directory_widget)
        self.setting_layout.addWidget(self.output_directory_widget)
        self.setting_layout.addWidget(self.language_file_widget)

        self.setting_widget.adjustSize()

        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.setting_widget)

    def __connect_signal(self) -> None:
        """
        Connect signals to slots
        """
        self.choose_file_button.clicked.connect(
            self.__on_choose_file_button_clicked
        )
        self.input_directory_button.clicked.connect(
            self.__on_input_directory_button_clicked)
        self.output_directory_button.clicked.connect(
            self.__on_output_directory_button_clicked)
        self.input_directory_edit.textChanged.connect(
            lambda x: cfg.set(cfg.input_directory, x))
        self.output_directory_edit.textChanged.connect(
            lambda x: cfg.set(cfg.output_directory, x))

    def __on_choose_file_button_clicked(self) -> None:
        """
        Open dialogue when click button
        """
        path = QFileDialog.getOpenFileName(
            self, self.tr("Choose code file"),
            "./", self.tr("Code Files")+"(*.py *.c *.cpp);;"+self.tr("All files")+"(*)")[0]
        if path == "":
            return
        self.choose_file_combobox.setItemText(1, path)
        self.choose_file_combobox.setCurrentIndex(1)

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
