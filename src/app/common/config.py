# coding: utf-8
"""
@File        :   config.py
@Time        :   2024/10/15 11:44:04
@Author      :   Usercyk
@Description :   The configurations that users can modify
"""
import sys

from enum import Enum
from typing import override

from PySide6.QtCore import QLocale
from qfluentwidgets import (ConfigSerializer, QConfig, ConfigItem,
                            BoolValidator, OptionsConfigItem, OptionsValidator, qconfig)


class Language(Enum):
    """
    The language support.
    """
    CHINESE_SIMPLIFIED = QLocale(
        QLocale.Language.Chinese, QLocale.Country.China)
    CHINESE_TRADITIONAL = QLocale(
        QLocale.Language.Chinese, QLocale.Country.HongKong)
    ENGLISH = QLocale(QLocale.Language.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """
    The serializer for languages.
    """
    # pylint: disable=W0237
    @override
    def serialize(self, language: Language) -> str:
        return language.value.name() if language != Language.AUTO else "Auto"

    @override
    def deserialize(self, value: str) -> Language:
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def is_win11() -> bool:
    """
    Check whether the platform is win 11
    """
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class _Config(QConfig):
    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled",
                             is_win11(), BoolValidator())
    dpiScale = OptionsConfigItem("MainWindow", "DpiScale", "Auto", OptionsValidator(
        [1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem("MainWindow", "Language", Language.AUTO, OptionsValidator(
        Language), LanguageSerializer(), restart=True)


cfg = _Config()
qconfig.load('app/config/config.json', cfg)
