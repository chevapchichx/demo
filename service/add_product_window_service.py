from PyQt6.QtGui import QIcon, QPixmap, QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox

from service.db_service import DBService
from view.add_product_window_ui import Ui_AddProductWindow


class AddProductWindowService(QWidget, Ui_AddProductWindow):
    """Окно добавления товара. Открывается при клике на кнопку добавления товара в окне списка товаров."""
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("data/Icon.png"))

        self.user = user
        self.photo_path = None
        types_dict, suppliers_dict, producers_dict, categories_dict = DBService().get_products_details_db()

        # Заполнение комбобоксов уникальными значениями (id-name) из словарей
        self.type_cbx.setPlaceholderText("Наименование")
        for type_id, type_name in types_dict.items():
            self.type_cbx.addItem(type_name, type_id)

        self.category_cbx.setPlaceholderText("Категория")
        for category_id, category_name in categories_dict.items():
            self.category_cbx.addItem(category_name, category_id)

        self.producer_cbx.setPlaceholderText("Производитель")
        for producer_id, producer_name in producers_dict.items():
            self.producer_cbx.addItem(producer_name, producer_id)

        self.supplier_cbx.setPlaceholderText("Поставщик")
        for supplier_id, supplier_name in suppliers_dict.items():
            self.supplier_cbx.addItem(supplier_name, supplier_id)

        # Установка валидаторов для числовых полей ввода
        validator_float = QDoubleValidator(0.0, 9999.0, 2)
        validator_int = QIntValidator(0, 1000)

        self.price_le.setValidator(validator_float)
        self.amount_le.setValidator(validator_int)
        self.discount_le.setValidator(validator_int)

        self.go_back_btn.clicked.connect(lambda: self.open_products_window(self.user))
        self.add_product_btn.clicked.connect(lambda: self.add_product())


    def add_product(self):
        """Добавляет товар в базу данных после валидации полей ввода."""
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
            return QMessageBox.warning(self, "Ошибка добавления товара", "Не все поля заполнены")
        # Преобразование строк в числовые типы для валидации и сохранения в БД
        price, amount_in_warehouse, current_discount = float(price), int(amount_in_warehouse), int(current_discount)
        if current_discount > 100:
            return QMessageBox.warning(self, "Ошибка добавления товара", "Скидка должна быть не больше 100%")


        result = DBService().add_product_db(id_type, id_category, description, id_producer, id_supplier, price,
                                            unit_of_measurement, amount_in_warehouse, current_discount, self.photo_path)
        if result:
            QMessageBox.information(self, "Успех", f"Товар добавлен")
            self.open_products_window(self.user)
        return None


    def mousePressEvent(self, event):
        # Обработка клика по области фото для загрузки изображения товара
        if self.photo_l.geometry().contains(event.pos()):
            self.photo_path = QFileDialog.getOpenFileName()[0]
            self.photo_l.setPixmap(QPixmap(self.photo_path).scaled(self.photo_l.size()))


    def open_products_window(self, user):
        """Открывает окно списка товаров."""
        from service.products_window_service import ProductsWindowService
        self.window = ProductsWindowService(user)
        self.window.show()
        self.close()
