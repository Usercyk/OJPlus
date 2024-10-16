# coding: utf-8
"""
@File        :   language.py
@Time        :   2024/10/16 13:08:03
@Author      :   Usercyk
@Description :   Offer internationalization config
"""
from enum import Enum
from typing import override

from PySide6.QtCore import QLocale
from qfluentwidgets import ConfigSerializer


class Language(Enum):
    """
    The enum for supported language
    """
    CHINESE_SIMPLIFIED = QLocale(
        QLocale.Language.Chinese, QLocale.Country.China)
    CHINESE_TRADITIONAL = QLocale(
        QLocale.Language.Chinese, QLocale.Country.HongKong)
    ENGLISH = QLocale(QLocale.Language.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """
    The serializer of `Language`
    Specificly, deal with `Language.AUTO`
    """
    # pylint: disable=W0237
    @override
    def serialize(self, language: Language) -> str:
        return language.value.name() if language != Language.AUTO else "Auto"

    @override
    def deserialize(self, value: str) -> Language:
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO

# set all
__all__ = ["Language", "LanguageSerializer"]
