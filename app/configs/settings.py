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
VERSION = __version__
AUTHOR = __author__

# path setting
CONFIG_PATH = "app/config.json"

# window
SIZE = (960, 780)
MIN_WIDTH = 760
ICON_SIZE = (106, 106)
INTERFACE_SIZE = (1000, 800)

# set all
__all__ = ["VERSION", "AUTHOR", "CONFIG_PATH",
           "SIZE", "MIN_WIDTH", "ICON_SIZE", "INTERFACE_SIZE"]
