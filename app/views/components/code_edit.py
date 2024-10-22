# coding: utf-8
"""
@File        :   code_edit.py
@Time        :   2024/10/21 20:27:26
@Author      :   Usercyk
@Description :   Code edit
"""
from typing import override
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from qfluentwidgets import PlainTextEdit


class CodeEdit(PlainTextEdit):
    """
    Code edit
    """

    def __init__(self, parent):
        super().__init__(parent)

    @override
    def keyPressEvent(self, e: QKeyEvent):
        if e.modifiers() == Qt.KeyboardModifier.ShiftModifier and e.key() == Qt.Key.Key_Return:
            self.parent().setFocus()
            return e.ignore()
        return super().keyPressEvent(e)
