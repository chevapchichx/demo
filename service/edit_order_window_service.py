from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox, QLabel

from service.db_service import DBService
from view.edit_order_window_ui import Ui_EditOrderWindow


class EditOrderWindowService(QDialog, Ui_EditOrderWindow):
    """Окно редактирования заказа. Открывается при клике на заказ в списке заказов.
    Позволяет редактировать заказ, а также удалять заказ из базы данных."""
    def __init__(self, order):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.order = order
        statuses_dict, pick_up_points_dict = DBService().get_orders_details_db()

        self.products_list = DBService().get_products_info_db()

        self.id_le.setText(f"Номер заказа: {self.order.id}")
        self.date_order_de.setDate(self.order.date_order)
        self.date_delivery_de.setDate(self.order.date_delivery)

        # Заполнение комбобоксов уникальными значениями (id-name) из словарей
        for status_id, status_name in statuses_dict.items():
            self.status_cbx.addItem(status_name, status_id)

        for pick_up_point_id, pick_up_point_name in pick_up_points_dict.items():
            self.pick_up_point_cbx.addItem(pick_up_point_name, pick_up_point_id)

        self.products_in_order = DBService().get_products_in_order_db(self.order.id)

        text = ""
        for product in self.products_in_order:
            text += f"Артикул: {product[0]}, количество: {product[1]}\n"

        self.products_in_order_l.setText(f"Товары в заказе:\n{text}")

        self.status_cbx.setCurrentText(self.order.status_name)
        self.pick_up_point_cbx.setCurrentText(self.order.pick_up_point_name)

        # self.tovar_cbx_1.setCurrentText(self.order.)

        self.go_back_btn.clicked.connect(lambda: self.close())
        self.save_order_btn.clicked.connect(lambda: self.save_order())
        self.delete_order_btn.clicked.connect(lambda: self.delete_order())


    def save_order(self):
        id_status = self.status_cbx.currentData()
        id_pick_up_point = self.pick_up_point_cbx.currentData()
        date_order = self.date_order_de.date().toPyDate()
        date_delivery = self.date_delivery_de.date().toPyDate()

        if not id_status or not id_pick_up_point or not date_order or not date_delivery:
            return QMessageBox.warning(self, "Ошибка редактирования заказа", "Не все поля заполнены")
        if date_delivery < date_order:
            return QMessageBox.warning(self, "Ошибка редактирования заказа",
                                       "Дата доставки не может быть раньше даты заказа")

        result = DBService().edit_order_db(self.order.id, id_status, id_pick_up_point, date_order, date_delivery)
        if result:
            QMessageBox.information(self, "Успех", f"Заказ {self.order.id} отредактирован")
            self.close()
        return None


    def delete_order(self):
        reply = QMessageBox.question(self, "Удаление заказа", "Вы точно хотите удалить заказ?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if  DBService().delete_order_db(self.order.id):
                QMessageBox.information(self, "Успех", f"Заказ удален")
                self.close()
