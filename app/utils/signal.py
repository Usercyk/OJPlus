# coding: utf-8
"""
@File        :   signal_bus.py
@Time        :   2024/10/16 23:39:08
@Author      :   Usercyk
@Description :   The signal bus to connect signal from different widgets
"""
from PySide6.QtCore import QObject, Signal


class _SignalBus(QObject):
    """
    Signal bus
    """
    micaEnableChanged = Signal(bool)


signal_bus = _SignalBus()

__all__ = ["signal_bus"]
