# coding: utf-8
"""
@File        :   judge_interface.py
@Time        :   2024/10/19 14:33:34
@Author      :   Usercyk
@Description :   The judge machine interface
"""
from typing import override
from PySide6.QtWidgets import (QWidget, QLabel, QHBoxLayout,
                               QVBoxLayout, QFileDialog, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QDir, QFileInfo
from PySide6.QtGui import QKeyEvent
from qfluentwidgets import (ScrollArea, ExpandLayout, BodyLabel,
                            ComboBox, LineEdit, PrimaryPushButton,
                            TextBrowser)

from configs import INTERFACE_SIZE, SUPPORT_LANGUAGE, cfg
from utils import StyleSheet, CodeTester
from views.components import CodeEdit


class JudgeInterface(ScrollArea):
    """
    The judge interface
    """
    run_signal = Signal(str, str, str, str, bool)

    def __init__(self, parent) -> None:
        # super
        super().__init__(parent)
        # create widgets
        self.__create_widgets()
        # set up widgets
        self.__setup_widgets()
        # code tester
        self.__create_code_tester()

    def __create_code_tester(self) -> None:
        """
        Create code tester
        """
        self.code_tester = CodeTester()
        self.code_tester.result_ready.connect(self.handle_result)
        self.code_tester.error_occurred.connect(self.handle_error)
        self.code_tester.compilation_started.connect(
            self.handle_compilation_start)
        self.code_tester.compilation_finished.connect(
            self.handle_compilation_finish)
        self.code_tester.validation_error.connect(self.handle_validation_error)
        self.run_signal.connect(self.code_tester.start_testing)

    def handle_compilation_start(self) -> None:
        """
        Show compilation process
        """
        self.result_browser.setMarkdown(self.tr("Start compiling..."))

    def handle_compilation_finish(self, success: bool, message: str):
        """
        Show compilation process
        """
        if success:
            self.result_browser.append(
                self.tr("Compile succeed. Start Testing..."))
        else:
            self.result_browser.append(self.tr("Compile error: ")+"\n"+message)

    def handle_validation_error(self, error_msg):
        """
        Validation error
        """
        self.result_browser.append(self.tr("Invalid paths: ")+error_msg)

    def handle_result(self, test_name: str, result: bool, output: str):
        """
        Result
        """
        status = self.tr("Accepted") if result else self.tr("Wrong Answer")
        self.result_browser.append(self.tr("Test ")+f"{test_name}: {status}")
        # if not result:
        #     self.result_browser.append(
        #         self.tr("Your output: ")+f"\n{output}")

    def handle_error(self, test_name, error_msg):
        """
        Error
        """
        self.result_browser.append(
            self.tr("Test ")+test_name+self.tr(" error: ")+f"\n{error_msg}")

    def validate_paths(self, file_path, input_path, output_path, is_file=False):
        """
        Validate all paths
        """
        if is_file and (not QFileInfo(file_path).exists() or not QFileInfo(file_path).isFile()):
            return False, self.tr("Invalid file: ")+file_path

        if not QDir(input_path).exists():
            return False, self.tr("Invalid directory: ")+input_path

        if not QDir(output_path).exists():
            return False, self.tr("Invalid directory: ")+output_path

        return True, ""

    def __create_widgets(self) -> None:
        """
        Create widgets
        """
        # central widgets and layout
        self.scroll_widget = QWidget()
        self.expand_layout = ExpandLayout(self.scroll_widget)

        # judge label
        self.judge_label = QLabel(self.tr("Judge"), self)

        # sub widgets
        self.sub_widget = QWidget(self.scroll_widget)
        self.sub_v_layout = QVBoxLayout(self.sub_widget)

        # set code language and code file
        self.language_file_widget = QWidget(self.sub_widget)
        self.language_file_layout = QHBoxLayout(self.language_file_widget)
        self.choose_language_label = BodyLabel(
            self.tr("Language: "), self.language_file_widget)
        self.choose_language_combobox = ComboBox(self.language_file_widget)
        self.choose_file_label = BodyLabel(
            self.tr("Code File: "), self.language_file_widget)
        self.choose_file_combobox = ComboBox(self.language_file_widget)
        self.choose_file_button = PrimaryPushButton(
            self.tr("Choose file"), self.language_file_widget)

        # choose input directory
        self.input_directory_widget = QWidget(self.sub_widget)
        self.input_directory_layout = QHBoxLayout(self.input_directory_widget)
        self.input_directory_label = BodyLabel(
            self.tr("Input directory:    "), self.input_directory_widget)
        self.input_directory_edit = LineEdit(self.input_directory_widget)
        self.input_directory_button = PrimaryPushButton(
            self.tr("Choose folder"), self.input_directory_widget)

        # choose output directory
        self.output_directory_widget = QWidget(self.sub_widget)
        self.output_directory_layout = QHBoxLayout(
            self.output_directory_widget)
        self.output_directory_label = BodyLabel(
            self.tr("Output directory: "), self.output_directory_widget)
        self.output_directory_edit = LineEdit(self.output_directory_widget)
        self.output_directory_button = PrimaryPushButton(
            self.tr("Choose folder"), self.output_directory_widget)

        # edit code
        self.code_result_widget = QWidget(self.sub_widget)
        self.code_result_layout = QHBoxLayout(self.code_result_widget)
        self.code_edit = CodeEdit(self.code_result_widget)
        self.result_browser = TextBrowser(self.code_result_widget)

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
        self.sub_widget.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.choose_language_combobox.addItems(SUPPORT_LANGUAGE)
        self.choose_file_combobox.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.choose_file_combobox.addItem(self.tr("Submit with plain text"))
        self.choose_file_combobox.addItem(self.tr("<Empty File>"))

        self.input_directory_edit.setText(cfg.get(cfg.input_directory))
        self.output_directory_edit.setText(cfg.get(cfg.output_directory))

        self.code_edit.setPlaceholderText(
            self.tr("Type your code here if you submit your code with plain text."))
        self.result_browser.setText(
            self.tr("Waiting to submit... \nPress shift+Enter to submit."))
        self.code_result_widget.setMinimumHeight(450)

        # initialize style sheet
        self.scroll_widget.setObjectName('scrollWidget')
        self.judge_label.setObjectName('judgeLabel')
        self.sub_widget.setObjectName('subWidget')
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

        self.code_result_layout.setSpacing(10)
        self.code_result_layout.setContentsMargins(0, 0, 0, 5)
        self.code_result_layout.addWidget(self.code_edit)
        self.code_result_layout.addWidget(self.result_browser)

        self.sub_v_layout.addWidget(self.input_directory_widget)
        self.sub_v_layout.addWidget(self.output_directory_widget)
        self.sub_v_layout.addWidget(self.language_file_widget)
        self.sub_v_layout.addWidget(self.code_result_widget)

        self.sub_widget.adjustSize()

        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.sub_widget)

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

    def __test_code(self) -> None:
        """
        Test code
        """
        if not self.code_tester.isRunning():
            self.result_browser.clear()
            self.result_browser.append(self.tr("Start validate paths"))
            is_file = self.choose_file_combobox.currentIndex() == 1

            file_path = self.choose_file_combobox.currentText(
            ) if is_file else self.code_edit.toPlainText()
            input_path = self.input_directory_edit.text()
            output_path = self.output_directory_edit.text()

            is_valid, error_message = self.validate_paths(
                file_path, input_path, output_path, is_file)
            if not is_valid:
                self.result_browser.append(
                    self.tr("Validation error: \n")+error_message)
                return

            language = self.choose_language_combobox.currentText()

            self.result_browser.append(
                self.tr("Validation succeed. Start running..."))
            self.run_signal.emit(language, file_path,
                                 input_path, output_path, is_file)
        else:
            self.result_browser.append(self.tr("Already running a test..."))

    @override
    def keyPressEvent(self, e: QKeyEvent):
        if e.modifiers() == Qt.KeyboardModifier.ShiftModifier and e.key() == Qt.Key.Key_Return:
            self.__test_code()
