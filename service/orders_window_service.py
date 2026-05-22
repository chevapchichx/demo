from datetime import date

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from service.db_service import DBService
from view.orders_window_ui import Ui_OrdersWindow


class OrdersWindowService(QWidget, Ui_OrdersWindow):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.user = user

        self.orders_list = DBService().get_orders_info_db()

        # Если список заказов не пустой, он выводится в scrollArea
        if self.orders_list:
            if self.user.id_role == 3: # 3 - роль клиента
                self.orders_list = [order for order in self.orders_list if order.id_client == self.user.id]

            self.display_orders(self.orders_list)

        # Кнопка добавления заказа доступна только администратору (id_role = 1)
        if not self.user.id_role == 1:
            self.open_add_order_window_btn.hide()

        self.go_back_btn.clicked.connect(lambda: self.open_products_window(self.user))

        self.open_add_order_window_btn.clicked.connect(lambda: self.open_add_order_window(self.user))


    def display_orders(self, orders_list):
        """Отображает список заказов в scrollArea.
        Если список уже отображается, то старый удаляется и отображается новый."""
        self.scrollWidget.deleteLater()

        self.scrollWidget = QWidget()
        self.scrollArea.setWidget(self.scrollWidget)

        self.orders_layout = QVBoxLayout()
        self.scrollWidget.setLayout(self.orders_layout)

        for order in orders_list:
            order_widget = QWidget()
            order_layout = QHBoxLayout()
            order_widget.setLayout(order_layout)
            self.orders_layout.addWidget(order_widget)

            order_info_l = QLabel(f"Номер заказа: {order.id}\n"
                                  f"Статус заказа: {order.status_name}\n"
                                  f"Адрес пункта выдачи: {order.pick_up_point_name}\n" 
                                  f"Дата заказа: {date.strftime(order.date_order, '%d.%m.%Y')}\n")

            order_info_l.setWordWrap(True)
            order_info_l.setFixedHeight(150)
            order_info_l.setStyleSheet("border: 1px solid black")
            order_layout.addWidget(order_info_l)

            order_date_delivery_l = QLabel(f"Дата доставки:\n{date.strftime(order.date_delivery, '%d.%m.%Y')}")
            order_date_delivery_l.setWordWrap(True)
            order_date_delivery_l.setFixedSize(100, 150)
            order_date_delivery_l.setStyleSheet("border: 1px solid black")
            order_date_delivery_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            order_layout.addWidget(order_date_delivery_l)

            # Сохранение ссылки на данные заказа в объект виджета для доступа в обработчике событий
            order_widget.order_data = order
            order_widget.installEventFilter(self)


    def eventFilter(self, obj, event):
        """Обработчик событий для виджетов заказов. Двойной клик открывает окно редактирования заказа."""
        if self.user.id_role == 1 and event.type() == QEvent.Type.MouseButtonDblClick:
            order = obj.order_data
            if order:
                self.open_edit_order_window(order)
                return True
        return super().eventFilter(obj, event)


    def open_products_window(self, user):
        """Открывает окно списка товаров."""
        from service.products_window_service import ProductsWindowService
        self.window = ProductsWindowService(user)
        self.window.show()
        self.close()


    def open_add_order_window(self, user):
        """Открытие окна добавления нового заказа."""
        from service.add_order_window_service import AddOrderWindowService
        self.window = AddOrderWindowService(user)
        self.window.show()
        self.close()


    def open_edit_order_window(self, order):
        """Открытие окна редактирования заказа с последующим обновлением списка заказов."""
        from service.edit_order_window_service import EditOrderWindowService
        self.window = EditOrderWindowService(order)
        self.window.exec()
        # После закрытия окна редактирования обновляется список заказов
        self.orders_list = DBService().get_orders_info_db()
        self.display_orders(self.orders_list)
