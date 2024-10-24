# coding: utf-8
"""
@File        :   test_code.py
@Time        :   2024/10/22 12:03:25
@Author      :   Usercyk
@Description :   Code Tester
"""
import os
import glob
from PySide6.QtCore import QThread, Signal, QProcess

from configs import cfg, LANGUAGE_SUFFIX, NEED_COMPILE


# pylint:disable=W0718
class CodeTester(QThread):
    """
    Test code
    """
    result_ready = Signal(str, bool, str)  # test_name, is_success, output
    error_occurred = Signal(str, str)  # test_name, error_message
    compilation_started = Signal()
    compilation_finished = Signal(bool, str)  # success, message
    validation_error = Signal(str)  # error_message
    test_finished = Signal()

    def __init__(self):
        super().__init__()
        self.language = "Python"
        self.file_path_or_text = ""
        self.file_path = ""
        self.input_path = ""
        self.output_path = ""
        self.is_file: bool = False
        self.time_out = 5000
        self.executable_path = None
        self.temp_code_path = None

    def validate_file_permissions(self):
        """
        Validate the permissions
        """
        try:
            if not self.is_file or self.language in NEED_COMPILE:
                temp_dir = cfg.get(cfg.temp_directory)
                if not os.access(temp_dir, os.W_OK):
                    return False, self.tr("No directory permission: ")+temp_dir

            if not self.is_file:
                file_path = os.path.join(
                    temp_dir, 'temp_code')+LANGUAGE_SUFFIX[self.language]
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.file_path_or_text)
                self.file_path = file_path
                self.temp_code_path = file_path
            else:
                self.file_path = self.file_path_or_text

            if not os.access(self.file_path, os.R_OK):
                return False, self.tr("No file permission: ")+self.file_path

            if not os.access(self.input_path, os.R_OK):
                return False, self.tr("No directory permission: ")+self.input_path

            if not os.access(self.output_path, os.R_OK):
                return False, self.tr("No directory permission: ")+self.output_path

            return True, ""

        except Exception as e:
            return False, self.tr("Unknown validation error: ")+str(e)

    def start_testing(self, language, file_path_or_text, input_path, output_path, is_file: bool):
        """
        Start testing the code
        """
        self.language = language
        self.file_path_or_text = file_path_or_text
        self.input_path = input_path
        self.output_path = output_path
        self.is_file = is_file
        self.start()

    def compile_source(self):
        """
        Compile the code file
        """
        if self.language not in NEED_COMPILE:
            return True, ""

        self.compilation_started.emit()

        temp_dir = cfg.get(cfg.temp_directory)
        self.executable_path = os.path.join(temp_dir, 'program_executable')
        if os.name == 'nt':
            self.executable_path += '.exe'

        compiler = cfg.get(
            cfg.cppPath) if self.language == "C++" else cfg.get(cfg.cPath)
        compiler_flags = ['-o', self.executable_path]

        process = QProcess()
        process.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels)

        process.start(compiler, [self.file_path] + compiler_flags)

        if not process.waitForFinished(30000):  # 30秒超时
            process.kill()
            self.compilation_finished.emit(
                False, self.tr("Compile Time Limit Error"))
            return False, self.tr("Compile Time Limit Error")

        exit_code = process.exitCode()
        output = process.readAll().data().decode()

        if exit_code != 0:
            self.compilation_finished.emit(False, output)
            return False, output

        self.compilation_finished.emit(True, self.tr("Compile Success"))
        return True, ""

    def run(self):
        permission_ok, error_msg = self.validate_file_permissions()
        if not permission_ok:
            self.validation_error.emit(error_msg)
            return

        if not self.compile_source()[0]:
            return

        for input_file in glob.glob(os.path.join(self.input_path, "*.in")):
            base_name = os.path.basename(input_file)
            test_name = os.path.splitext(base_name)[0]
            output_file = os.path.join(self.output_path, f"{test_name}.out")

            if not os.path.exists(output_file):
                self.error_occurred.emit(
                    test_name, self.tr("No output file: ")+output_file)
                continue

            try:
                with open(input_file, 'r', encoding="utf-8") as f:
                    input_data = f.read()
                with open(output_file, 'r', encoding="utf-8") as f:
                    expected_output = f.read().strip()

                process = QProcess()
                process.setProcessChannelMode(
                    QProcess.ProcessChannelMode.MergedChannels)

                if self.language == "Python":
                    process.start('python', [self.file_path])
                else:
                    process.start(self.executable_path)

                process.write(input_data.encode())
                process.closeWriteChannel()

                if not process.waitForFinished(self.time_out):
                    process.terminate()
                    if not process.waitForFinished(1000):
                        process.kill()
                        process.waitForFinished()
                    self.error_occurred.emit(test_name, self.tr("Timeout"))
                    continue

                exit_code = process.exitCode()
                output_data = process.readAll()

                if exit_code != 0:
                    error_output = output_data.data().decode()
                    self.error_occurred.emit(
                        test_name, self.tr("Runtime error (code: ")+f"{exit_code})\n{error_output}")
                    continue

                actual_output = output_data.data().decode().strip()
                self.result_ready.emit(
                    test_name, actual_output == expected_output, actual_output)

            except Exception as e:
                self.error_occurred.emit(
                    test_name, self.tr("Unknown error: ")+str(e))
            finally:
                if 'process' in locals():
                    if process.state() != QProcess.ProcessState.NotRunning:
                        process.terminate()
                        process.waitForFinished(1000)
                        if process.state() != QProcess.ProcessState.NotRunning:
                            process.kill()
                            process.waitForFinished()
                    process.deleteLater()

        if self.executable_path and os.path.exists(self.executable_path):
            try:
                os.remove(self.executable_path)
            except Exception:
                pass
        if self.temp_code_path and os.path.exists(self.temp_code_path):
            try:
                os.remove(self.temp_code_path)
            except Exception:
                pass
        self.test_finished.emit()
