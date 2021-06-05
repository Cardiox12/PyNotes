from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2.QtWidgets import QMainWindow

import sys

from package.main_window import MainWindow

if __name__ == '__main__':
    app_ctx = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow(app_ctx)

    window.show()
    exit_code = app_ctx.app.exec_()      # 2. Invoke app_ctx.app.exec_()
    sys.exit(exit_code)
