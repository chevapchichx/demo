from PyQt6.QtWidgets import QApplication
from service.auth_window_service import AuthWindowService

import sys


app = QApplication(sys.argv)
window = AuthWindowService()
window.show()
sys.exit(app.exec())
