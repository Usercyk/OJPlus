# coding: utf-8
"""
@File        :   style_sheet.py
@Time        :   2024/10/16 15:44:49
@Author      :   Usercyk
@Description :   Style sheet function used to apply qss
"""

from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """
    Style sheet
    """
    SETTING_INTERFACE = "setting_interface"
    HOME_INTERFACE = "home_interface"
    JUDGE_INTERFACE = "judge_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/oj_plus/qss/{theme.value.lower()}/{self.value}.qss"


__all__ = ["StyleSheet"]
