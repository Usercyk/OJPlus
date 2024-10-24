# coding: utf-8
"""
@File        :   deploy.py
@Time        :   2024/10/24 09:43:55
@Author      :   Usercyk
@Description :   Deploy the app
"""
import os

argu = ["nuitka",
        "--onefile",
        "--standalone",
        "--windows-console-mode=disable",
        "--mingw64",
        "--plugin-enable=pyside6,upx",
        "--output-dir=app/deployment",
        "--output-filename=ojplus",
        "--upx-binary=D:/upx-4.2.4-win64",
        "--windows-icon-from-ico=app/resources/images/favicon.png",
        "app/main.py"]

os.system(" ".join(argu))
