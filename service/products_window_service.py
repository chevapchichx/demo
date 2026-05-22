from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel

from service.db_service import DBService
from view.products_window_ui import Ui_ProductsWindow


class ProductsWindowService(QWidget, Ui_ProductsWindow):
    def __init__(self, user=None):
        super().__init__()
        self.setupUi(self)


        self.setWindowIcon(QIcon("data/Icon.png"))
        self.logo_l.setPixmap(QPixmap("data/Icon.png"))

        self.user = user
        self.products_list = DBService().get_products_info_db()

        # Если список товаров не пустой, он выводится в scrollArea
        if self.products_list:
            self.display_products(self.products_list)

            types_dict, suppliers_dict, producers_dict, categories_dict = DBService().get_products_details_db()

            # Добавление в выпадающий список фильтрации уникальных пар id_supplier-supplier_name
            self.filter_cbx.addItem("Все поставщики", 0)
            for supplier_id, supplier_name in suppliers_dict.items():
                self.filter_cbx.addItem(supplier_name, supplier_id)

            self.sort_cbx.addItem("Без сортировки", 0)
            self.sort_cbx.addItem("По возрастанию", 1)
            self.sort_cbx.addItem("По убыванию", 2)

        # Если пользователь авторизован, его имя отображается в правом верхнем углу окна
        if self.user:
            self.user_name_l.setText(f"{self.user.last_name} {self.user.first_name} {self.user.patronymic}")

        # Если пользователь не авторизован или не является администратором или менеджером,
        # то ему недоступна сортировка, фильтрация, поиск и окно со списком заказов
        if not self.user or not self.user.id_role in (1, 2):
            self.filter_cbx.hide()
            self.sort_cbx.hide()
            self.search_le.hide()
            self.open_orders_window_btn.hide()

        # Кнопка добавления товара доступна только администратору (id_role = 1)
        if not self.user or not self.user.id_role == 1:
            self.open_add_product_window_btn.hide()

        self.go_back_btn.clicked.connect(lambda: self.open_auth_window())

        self.sort_cbx.currentIndexChanged.connect(lambda: self.search_filter_sort())
        self.filter_cbx.currentIndexChanged.connect(lambda: self.search_filter_sort())
        self.search_le.textChanged.connect(lambda: self.search_filter_sort())

        self.open_add_product_window_btn.clicked.connect(lambda: self.open_add_product_window(self.user))

        self.open_orders_window_btn.clicked.connect(lambda: self.open_orders_window(self.user))


    def display_products(self, products_list):
        """Отображает список товаров в scrollArea.
        Если список уже отображается, то старый удаляется и отображается новый."""
        self.scrollWidget.deleteLater()

        self.scrollWidget = QWidget()
        self.scrollArea.setWidget(self.scrollWidget)

        self.products_layout = QVBoxLayout()
        self.scrollWidget.setLayout(self.products_layout)

        for product in products_list:
            product_widget = QWidget()
            product_layout = QHBoxLayout()
            product_widget.setLayout(product_layout)
            self.products_layout.addWidget(product_widget)

            # Условия для выделения строки с товаром цветом: скидка больше 15% — зеленый, товара нет на складе — голубой
            if product.current_discount > 15:
                product_widget.setStyleSheet("background-color: #2E8B57")

            if product.amount_in_warehouse == 0:
                product_widget.setStyleSheet("background-color: aqua")

            # Условие для выделения цены, если скидка больше 0%
            if product.current_discount > 0:
                discounted_price = round(product.price * (1 - product.current_discount / 100), 2)
                price_text = f"<s style='color:red'>{product.price}</s> {discounted_price}"
            else:
                price_text = str(product.price)

            product_photo_l = QLabel()
            product_photo_l.setFixedSize(200, 200)
            product_photo_l.setStyleSheet("border: 1px solid black")
            photo = product.photo if product.photo else QPixmap("data/picture.png")
            product_photo_l.setPixmap(photo.scaled(product_photo_l.size()))
            product_layout.addWidget(product_photo_l)

            product_info_l = QLabel(f"{product.category_name} | {product.type_name}<br>"
                f"Описание товара: {product.description}<br>"
                f"Производитель: {product.producer_name}<br>"
                f"Поставщик: {product.supplier_name}<br>"
                f"Цена: {price_text}<br>"
                f"Единица измерения: {product.unit_of_measurement}<br>"
                f"Количество на складе: {product.amount_in_warehouse}")

            product_info_l.setWordWrap(True)
            product_info_l.setFixedHeight(200)
            product_info_l.setStyleSheet("border: 1px solid black")
            product_layout.addWidget(product_info_l)

            product_discount_l = QLabel(f"Действующая скидка:\n{product.current_discount}%")
            product_discount_l.setWordWrap(True)
            product_discount_l.setFixedHeight(200)
            product_discount_l.setStyleSheet("border: 1px solid black")
            product_discount_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            product_layout.addWidget(product_discount_l)

            # Сохранение ссылки на данные товара в объект виджета для доступа в обработчике событий
            product_widget.product_data = product
            product_widget.installEventFilter(self)


    def search_filter_sort(self):
        """Применяет поиск, фильтрацию по поставщику и сортировку по количеству на складе."""
        search_words = self.search_le.text().lower().split()
        filter_option = self.filter_cbx.currentData()
        sort_option = self.sort_cbx.currentData()

        filtered_products = self.products_list

        # Поиск: проверка наличия всех слов в строковом представлении товара
        if search_words:
            filtered_products = [p for p in filtered_products if all(word in
                   f"{p.article} {p.type_name} {p.unit_of_measurement} {p.supplier_name} {p.producer_name} "
                   f"{p.category_name} {p.description}".lower() for word in search_words)]

        # Фильтрация по поставщику (0 - "Все поставщики")
        if filter_option != 0:
            filtered_products = [product for product in filtered_products if
                                 product.id_supplier == filter_option]

        # Сортировка по количеству товара: 1 — возрастание, 2 — убывание
        if sort_option != 0:
            filtered_products = sorted(filtered_products, key=lambda product: product.amount_in_warehouse,
                                       reverse=False if sort_option == 1 else True)

        self.display_products(filtered_products)


    def eventFilter(self, obj, event):
        """Обработчик событий для виджетов продуктов. Двойной клик открывает окно редактирования товара."""
        if self.user and self.user.id_role == 1 and event.type() == QEvent.Type.MouseButtonDblClick:
            product = obj.product_data
            if product:
                self.open_edit_product_window(product)
                return True
        return super().eventFilter(obj, event)


    def open_auth_window(self):
        """Открытие окна авторизации."""
        from service.auth_window_service import AuthWindowService
        self.window = AuthWindowService()
        self.window.show()
        self.close()


    def open_add_product_window(self, user):
        """Открытие окна добавления нового товара."""
        from service.add_product_window_service import AddProductWindowService
        self.window = AddProductWindowService(user)
        self.window.show()
        self.close()


    def open_edit_product_window(self, product):
        """Открытие окна редактирования товара с последующим обновлением списка товаров."""
        from service.edit_product_window_service import EditProductWindowService
        self.window = EditProductWindowService(product)
        self.window.exec()
        # После закрытия окна редактирования обновляется список товаров и фильтры
        self.products_list = DBService().get_products_info_db()
        self.display_products(self.products_list)
        self.search_filter_sort()


    def open_orders_window(self, user):
        """Открытие окна списка заказов."""
        from service.orders_window_service import OrdersWindowService
        self.window = OrdersWindowService(user)
        self.window.show()
        self.close()
