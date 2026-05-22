from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox, QComboBox

from service.db_service import DBService
from view.add_order_window_ui import Ui_AddOrderWindow


class AddOrderWindowService(QWidget, Ui_AddOrderWindow):
    """Окно добавления заказа. Открывается при клике на кнопку добавления заказа в окне списка заказов."""
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.user = user
        self.products_list = DBService().get_products_info_db()
        statuses_dict, pick_up_points_dict = DBService().get_orders_details_db()

        # Заполнение комбобоксов уникальными значениями (id-name) из словарей
        self.status_cbx.setPlaceholderText("Статус")
        for status_id, status_name in statuses_dict.items():
            self.status_cbx.addItem(status_name, status_id)

        self.pick_up_point_cbx.setPlaceholderText("Пункт выдачи")
        for pick_up_point_id, pick_up_point_name in pick_up_points_dict.items():
            self.pick_up_point_cbx.addItem(pick_up_point_name, pick_up_point_id)


        self.product_cbx_1.addItem("Не выбрано", 0)
        products_dict = {product.id : f"{product.article}, {product.type_name}" for product in self.products_list}
        for product_id, name in products_dict.items():
            self.product_cbx_1.addItem(name, product_id)

        self.product_cbx_2.addItem("Не выбрано", 0)
        products_dict = {product.id: f"{product.article}, {product.type_name}" for product in self.products_list}
        for product_id, name in products_dict.items():
            self.product_cbx_2.addItem(name, product_id)


        self.go_back_btn.clicked.connect(lambda: self.open_orders_window(self.user))
        self.add_order_btn.clicked.connect(lambda: self.add_order())


    def add_order(self):
        """Добавляет заказ в базу данных после валидации полей."""
        id_status = self.status_cbx.currentData()
        id_pick_up_point = self.pick_up_point_cbx.currentData()
        date_order = self.date_order_de.date().toPyDate()
        date_delivery = self.date_delivery_de.date().toPyDate()
        id_product_1 = self.product_cbx_1.currentData()
        id_product_2 = self.product_cbx_2.currentData()


        if not id_status or not id_pick_up_point or not date_order or not date_delivery:
            return QMessageBox.warning(self, "Ошибка добавления заказа", "Не все поля заполнены")

        if id_product_1 == 0 and id_product_2 == 0:
            return QMessageBox.warning(self, "Ошибка добавления заказа", "Надо выбрать хотя бы один товар")

        if date_delivery < date_order:
            return QMessageBox.warning(self, "Ошибка добавления заказа",
                                       "Дата доставки не может быть раньше даты заказа")

        result = DBService().add_order_db(id_product_1, id_product_2, id_status, id_pick_up_point, date_order, date_delivery)
        if result:
            QMessageBox.information(self, "Успех", f"Заказ добавлен")
            self.create_check(result)
            self.open_orders_window(self.user)
        return None


    def open_orders_window(self, user):
        """Открытие окна списка заказов."""
        from service.orders_window_service import OrdersWindowService
        self.window = OrdersWindowService(user)
        self.window.show()
        self.close()


    def create_check(self, order):
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(f"output_{order[0][0]}.pdf")
        c.drawString(100, 750, f"{order[0]}")
        c.save()

