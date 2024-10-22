# coding: utf-8
"""
@File        :   settings.py
@Time        :   2024/10/16 13:02:31
@Author      :   Usercyk
@Description :   The configs that user cannot change
"""

__version__ = "0.1.0"
__author__ = "UserCyk"

# basic info
from typing import Dict, Literal


VERSION = __version__
AUTHOR = __author__
YEAR = 2024

# path setting
CONFIG_PATH = "app/config.json"

# executables
SUPPORT_LANGUAGE = ["Python", "C++", "C"]
SupportLanguageAlias = Literal["Python", "C++", "C"]
SupportLanguageSuffix = Literal[".py", ".cpp", ".c"]
LANGUAGE_SUFFIX: Dict[SupportLanguageAlias, SupportLanguageSuffix] = {
    "Python": ".py", "C++": ".cpp", "C": ".c"}
NEED_COMPILE = ["C", "C++"]

# urls
REPO_RELEASE_URL = "https://github.com/Usercyk/OJPlus/releases"
REPO_WIKI_URL = "https://github.com/Usercyk/OJPlus/wiki"

# window
SIZE = (960, 780)
MIN_WIDTH = 760
ICON_SIZE = (106, 106)
INTERFACE_SIZE = (1000, 800)

# set all
__all__ = ["VERSION", "AUTHOR", "CONFIG_PATH", "SIZE",
           "MIN_WIDTH", "ICON_SIZE", "INTERFACE_SIZE",
           "YEAR", "REPO_RELEASE_URL", "REPO_WIKI_URL",
           "SUPPORT_LANGUAGE", "SupportLanguageAlias", "LANGUAGE_SUFFIX",
           "SupportLanguageSuffix", "NEED_COMPILE"]
