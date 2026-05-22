from PyQt6.QtGui import QIcon, QPixmap, QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox

from service.db_service import DBService
from view.edit_product_window_ui import Ui_EditProductWindow


class EditProductWindowService(QDialog, Ui_EditProductWindow):
    """Окно редактирования товара. Открывается при клике на товар в списке товаров.
    Позволяет редактировать все поля товара, а также удалять товар из базы данных."""
    def __init__(self, product):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.product = product
        types_dict, suppliers_dict, producers_dict, categories_dict = DBService().get_products_details_db()

        # Если у товара есть фото, сохраняется полный путь, иначе None
        self.photo_path = None if not self.product.photo else f"data/{self.product.id}.jpg"

        # Загрузка фото товара или заглушки, если фото отсутствует
        self.photo = self.product.photo if self.product.photo else QPixmap(f"data/picture.png")
        self.photo_l.setPixmap(self.photo.scaled(self.photo_l.size()))

        self.id_le.setText(f"ID: {self.product.id}")
        self.description_le.setText(f"{self.product.description}")
        self.price_le.setText(f"{self.product.price}")
        self.unit_measure_le.setText(f"{self.product.unit_of_measurement}")
        self.amount_le.setText(f"{self.product.amount_in_warehouse}")
        self.discount_le.setText(f"{self.product.current_discount}")

        for type_id, type_name in types_dict.items():
            self.type_cbx.addItem(type_name, type_id)

        for category_id, category_name in categories_dict.items():
            self.category_cbx.addItem(category_name, category_id)

        for producer_id, producer_name in producers_dict.items():
            self.producer_cbx.addItem(producer_name, producer_id)

        for supplier_id, supplier_name in suppliers_dict.items():
            self.supplier_cbx.addItem(supplier_name, supplier_id)

        self.type_cbx.setCurrentText(self.product.type_name)
        self.category_cbx.setCurrentText(self.product.category_name)
        self.producer_cbx.setCurrentText(self.product.producer_name)
        self.supplier_cbx.setCurrentText(self.product.supplier_name)

        # Установка валидаторов для числовых полей ввода
        validator_float = QDoubleValidator(0.0, 9999.0, 2)
        validator_int = QIntValidator(0, 1000)

        self.price_le.setValidator(validator_float)
        self.amount_le.setValidator(validator_int)
        self.discount_le.setValidator(validator_int)

        self.go_back_btn.clicked.connect(lambda: self.close())
        self.save_product_btn.clicked.connect(lambda: self.save_product())
        self.delete_product_btn.clicked.connect(lambda: self.delete_product())


    def save_product(self):
        id_type = self.type_cbx.currentData()
        id_category = self.category_cbx.currentData()
        description = self.description_le.text()
        id_producer = self.producer_cbx.currentData()
        id_supplier = self.supplier_cbx.currentData()
        price = self.price_le.text().replace(",", ".")
        unit_of_measurement = self.unit_measure_le.text()
        amount_in_warehouse = self.amount_le.text()
        current_discount = self.discount_le.text()

        if (not id_type or not id_category or not description or not id_producer or not id_supplier
                or not price or not unit_of_measurement or not amount_in_warehouse or not current_discount):
            return QMessageBox.warning(self, "Ошибка редактирования товара", "Не все поля заполнены")
        price, amount_in_warehouse, current_discount = float(price), int(amount_in_warehouse), int(current_discount)
        if current_discount > 100:
            return QMessageBox.warning(self, "Ошибка редактирования товара", "Скидка должна быть не больше 100%")

        result = DBService().edit_product_db(self.product.id, id_type, id_category, description, id_producer, id_supplier, price,
                                            unit_of_measurement, amount_in_warehouse, current_discount, self.photo_path)
        if result:
            QMessageBox.information(self, "Успех", f"Товар {self.product.id} отредактирован")
            self.close()
        return None


    def delete_product(self):
        reply = QMessageBox.question(self, "Удаление товара", "Вы точно хотите удалить товар?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            if DBService().delete_product_db(self.product.id):
                QMessageBox.information(self, "Успех", f"Товар удален")
                self.close()


    def mousePressEvent(self, event):
        # Обработка клика по области фото для загрузки нового изображения товара
        if self.photo_l.geometry().contains(event.pos()):
            self.photo_path = QFileDialog.getOpenFileName()[0]
            self.photo_l.setPixmap(QPixmap(self.photo_path).scaled(self.photo_l.size()))
