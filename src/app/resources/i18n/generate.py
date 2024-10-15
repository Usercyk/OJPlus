# pylint: skip-file
import subprocess

TARGET = r"src\app\resources\i18n\oj_plus.zh_CN.ts"
SOURCES = [r"src\app\view\main_window.py"]

for file in SOURCES:
    subprocess.run(['pyside6-lupdate', file, '-ts', TARGET], check=False)
