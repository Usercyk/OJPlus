# coding: utf-8
"""
@File        :   icons.py
@Time        :   2024/10/17 19:39:15
@Author      :   Usercyk
@Description :   Provide more icons
"""
from enum import Enum
from qfluentwidgets import FluentIconBase, Theme, getIconColor


class AppIcon(FluentIconBase, Enum):
    """
    Provide more icons
    """
    ACRYLIC = "acrylic"
    PYTHON = "python"
    C = "c"
    CPP = "cpp"

    def path(self, theme=Theme.AUTO):
        """
        Get the icon's path
        """
        # getIconColor() return "white" or "black" according to current theme
        return f':oj_plus/images/icons/{self.value}_{getIconColor(theme)}.svg'


__all__ = ["AppIcon"]
