# coding: utf-8
"""
@File        :   generate_ts.py
@Time        :   2024/10/16 15:20:54
@Author      :   Usercyk
@Description :   Gernerate translation files
"""
import subprocess

FILES = ["app/views/main_window.py",
         "app/views/interfaces/setting_interface.py",
         "app/views/interfaces/home_interface.py",
         "app/views/interfaces/judge_interface.py",
         "app/utils/test_code.py"]
TARGET = ["app/resources/i18n/oj_plus.zh_CN.ts",
          "app/resources/i18n/oj_plus.zh_HK.ts"]

for t in TARGET:
    subprocess.run(["pyside6-lupdate", *FILES, "-ts", t], check=False)
