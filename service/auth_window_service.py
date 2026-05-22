from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox

from service.db_service import DBService
from view.auth_window_ui import Ui_AuthorizationWindow


class AuthWindowService(QWidget, Ui_AuthorizationWindow):
    """Окно авторизации — первый экран, который видит пользователь при запуске."""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.auth_btn.clicked.connect(lambda: self.auth())
        # Вход без авторизации — переход к списку товаров в роли гостя
        self.guest_btn.clicked.connect(lambda: self.open_products_window())


    def auth(self):
        """Проверяет введенные логин и пароль через БД и открывает окно товаров при успехе."""
        login = self.login_le.text().strip()
        password = self.password_le.text().strip()

        if not login or not password:
            return QMessageBox.warning(None, "Ошибка авторизации", "Все поля должны быть заполнены")

        user = DBService().get_user_info_db(login, password)
        if user:
            self.open_products_window(user)
        return None


    def open_products_window(self, user=None):
        """Открывает окно списка товаров. user=None означает вход как гость."""
        from service.products_window_service import ProductsWindowService
        self.window = ProductsWindowService(user)
        self.window.show()
        self.close()
