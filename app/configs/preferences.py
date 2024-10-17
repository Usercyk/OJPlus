# coding: utf-8
"""
@File        :   preferences.py
@Time        :   2024/10/16 12:59:49
@Author      :   Usercyk
@Description :   The configs that the users can change
"""
import sys

from qfluentwidgets import (QConfig, qconfig, ConfigItem,
                            OptionsConfigItem, BoolValidator, OptionsValidator, Theme)

from .settings import CONFIG_PATH
from .language import Language, LanguageSerializer


def is_win11() -> bool:
    """
    Check if the platform is win 11 to enable the mica effect
    """
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class _Config(QConfig):
    # excutable paths
    pythonPath = ConfigItem("Executable", "PythonPath", "python")
    cPath = ConfigItem("Executable", "CPath", "gcc")
    cppPath = ConfigItem("Executable", "CppPath", "g++")

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled",
                             is_win11(), BoolValidator())
    navigationAcrylicEnabled = ConfigItem(
        "MainWindow", "MicaEnabled", True, BoolValidator())
    dpiScale = OptionsConfigItem("MainWindow", "DpiScale", "Auto", OptionsValidator(
        [1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem("MainWindow", "Language", Language.AUTO, OptionsValidator(
        Language), LanguageSerializer(), restart=True)


cfg = _Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(CONFIG_PATH, cfg)

# set all
__all__ = ["cfg", "is_win11"]
