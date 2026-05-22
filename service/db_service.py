import os
import shutil
from unittest import result

import pymysql
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMessageBox

from data.order import Order
from data.user import User
from data.product import Product

class DBService:
    def __init__(self):
        self.conn = None
        try:
            # self.conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="boots_store")
            self.conn = pymysql.connect(host="MySQL-8.4", user="root", db="boots_store")
        except Exception as e:
            QMessageBox.warning(None, "Ошибка подключения к БД", f"Ошибка: {e}")

    def get_user_info_db(self, login, password):
        """Возвращает объект User по логину и паролю, или False при неправильных данных."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""select u.id_user, u.last_name, u.first_name, u.patronymic, 
                                      u.id_role, r.name from users u
                            join users_roles r on r.id_role = u.id_role
                            where u.login = %s and u.password = %s""", (str(login), str(password)))
                result = cur.fetchall()
                if result:
                    return User(*result[0])
                else:
                    QMessageBox.warning(None, "Ошибка авторизации", "Неверный логин или пароль")
                    return False
        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка: {e}")
            return False


    def get_products_info_db(self):
        """Возвращает список объектов Product из БД. Если фото отсутствует — сохраняется None"""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""select p.id_product, p.article, p.id_type, t.name, p.unit_of_measurement, p.price,
                 p.id_supplier, s.name, p.id_producer, pr.name, p.id_category,
                 c.name, p.current_discount, p.amount_in_warehouse, p.description, p.photo from products p
                                join product_type t on t.id_type = p.id_type
                                join suppliers s on s.id_supplier = p.id_supplier
                                join producers pr on pr.id_producer = p.id_producer
                                join product_category c on c.id_category = p.id_category""")
                result = cur.fetchall()

                products_list = []
                if result:
                    for product in result:
                        photo_pixmap = QPixmap(f"data/{product[15]}") if product[15] else None
                        products_list.append(Product(*product[:15], photo_pixmap))
                    return products_list
                else:
                    QMessageBox.warning(None, "Ошибка получения данных", "Товары не найдены")
                    return False
        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка: {e}")
            return False


    def get_dict_from_db(self, query):
        """Получает словарь {id: name} из БД."""
        with self.conn.cursor() as cur:
            cur.execute(query)
            return {row[0]: row[1] for row in cur.fetchall()}


    def get_products_details_db(self):
        """Возвращает словари наименований, поставщиков, производителей и категорий."""
        if not self.conn:
            return False
        try:
            types_dict = self.get_dict_from_db("select id_type, name from product_type")
            suppliers_dict = self.get_dict_from_db("select id_supplier, name from suppliers")
            producers_dict = self.get_dict_from_db("select id_producer, name from producers")
            categories_dict = self.get_dict_from_db("select id_category, name from product_category")

            return types_dict, suppliers_dict, producers_dict, categories_dict
        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка: {e}")
            return False


    def add_product_db(self, id_type, id_category, description, id_producer, id_supplier, price,
                       unit_of_measurement, amount_in_warehouse, current_discount, photo_path):
        """Добавляет новый товар в БД. Если photo_path не пустой, сохраняет название файла в БД и копирует файл в папку data."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""insert into products (id_type, id_category, description, id_producer, 
                                                     id_supplier, price, unit_of_measurement, amount_in_warehouse, 
                                                     current_discount) values
                                    (%s, %s, %s, %s, %s, %s,  %s, %s, %s)""",
                            (id_type, id_category, description, id_producer, id_supplier, price,
                             unit_of_measurement, amount_in_warehouse, current_discount))
                if photo_path:
                    id_product = cur.lastrowid
                    photo = f"{id_product}.jpg"
                    cur.execute("""update products set photo = %s
                                    where id_product = %s""", (photo, id_product))
                    shutil.copy(photo_path, f"data/{id_product}.jpg")
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(None, "Ошибка добавления данных", f"Ошибка: {e}")
            return False


    def edit_product_db(self, id_product, id_type, id_category, description, id_producer, id_supplier, price,
                                            unit_of_measurement, amount_in_warehouse, current_discount, photo_path):
        """Редактирует данные товара в БД. Если photo_path не пустой, сохраняет название файла в БД и копирует файл в папку data.
         Если photo_path пустой, удаляет старое фото из папки data и очищает поле photo в БД."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""update products set  id_type = %s, id_category = %s, description = %s, id_producer = %s, 
                                                     id_supplier = %s, price = %s, unit_of_measurement = %s, amount_in_warehouse = %s, 
                                                     current_discount =  %s
                                                    where id_product = %s""",
                            (id_type, id_category, description, id_producer, id_supplier, price,
                             unit_of_measurement, amount_in_warehouse, current_discount, id_product))
                if photo_path:
                    photo = f"{id_product}.jpg"
                    if f"data/{id_product}.jpg" not in photo_path:
                        shutil.copy(photo_path, f"data/{id_product}.jpg")
                else:
                    photo = None
                    if os.path.exists(f"data/{id_product}.jpg"):
                        os.remove(f"data/{id_product}.jpg")
                cur.execute("""update products set photo = %s
                                    where id_product = %s""", (photo, id_product))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(None, "Ошибка изменения данных", f"Ошибка: {e}")
            return False


    def delete_product_db(self, id_product):
        """Удаляет товар из БД. Если товар используется в заказах, удаление невозможно. Также удаляет фото товара из папки data."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""select id_product from products_in_orders
                            where id_product = %s""", (id_product))
                result = cur.fetchone()
                if not result:
                    cur.execute("delete from products where id_product = %s", (id_product))
                    if os.path.exists(f"data/{id_product}.jpg"):
                        os.remove(f"data/{id_product}.jpg")
                    self.conn.commit()
                    return True
                else:
                    QMessageBox.warning(None, "Ошибка удаления",
                                        f"Товар, который присутствует в заказе, удалить нельзя")
                    return False
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(None, "Ошибка удаления данных", f"Ошибка: {e}")
            return False


    def get_orders_info_db(self):
        """Возвращает список объектов Order из БД"""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""select o.id_order, o.id_status, s.name, o.id_pick_up_point, 
                                      concat_ws(" ", p.index_address, p.city, p.street, p.house) as pick_up_point_name, 
                                      o.date_order, o.date_delivery, o.id_client from orders o
                               join order_status s on s.id_status = o.id_status
                               join pick_up_points p on p.id_point = o.id_pick_up_point""")
                result = cur.fetchall()

                orders_list = []
                if result:
                    for order in result:
                        orders_list.append(Order(*order))
                    return orders_list
                else:
                    QMessageBox.warning(None, "Ошибка получения данных", "Заказы не найдены")
                    return False
        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка: {e}")
            return False


    def get_orders_details_db(self):
        """Возвращает словари статусов и пунктов выдачи."""
        if not self.conn:
            return False
        try:
            statuses_dict = self.get_dict_from_db("select id_status, name from order_status")
            pick_up_points_dict = self.get_dict_from_db("""select id_point, concat_ws(" ", p.index_address, p.city, p.street, p.house)
                                                        from pick_up_points p""")

            return statuses_dict, pick_up_points_dict
        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка: {e}")
            return False

    def get_products_in_order_db(self, id_order):
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""select p.article, p_o.amount_product from products_in_orders p_o
                                join products p on p.id_product = p_o.id_product
                            where p_o.id_order = %s""", (id_order))
                result = cur.fetchall()

                if result:
                    return result
        except Exception as e:
            QMessageBox.warning(None, "Ошибка получения данных", f"Ошибка: {e}")
            return False

    def add_order_db(self, id_product_1, id_product_2, id_status, id_pick_up_point, date_order, date_delivery):
        """Добавляет новый заказ в БД."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""insert into orders (id_status, id_pick_up_point, date_order, date_delivery) values
                                    (%s, %s, %s, %s)""",
                            (id_status, id_pick_up_point, date_order, date_delivery))

                order_id = cur.lastrowid
                if order_id:
                    if id_product_1 != 0:
                        cur.execute("""insert into products_in_orders (id_order, id_product, amount_product) values
                                    (%s, %s, 1)""", (order_id, id_product_1))
                    if id_product_2 != 0:
                        cur.execute("""insert into products_in_orders (id_order, id_product, amount_product) values
                                    (%s, %s, 1)""", (order_id, id_product_2))
                self.conn.commit()

                cur.execute("select * from orders where id_order = %s", (order_id))
                result = cur.fetchall()
                return result
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(None, "Ошибка добавления данных", f"Ошибка: {e}")
            return False


    def edit_order_db(self, id_order, id_status, id_pick_up_point, date_order, date_delivery):
        """Редактирует данные заказа в БД."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("""update orders set id_status = %s, id_pick_up_point = %s, 
                                                 date_order = %s, date_delivery = %s
                                    where id_order = %s""", (id_status, id_pick_up_point, date_order,
                                                             date_delivery, id_order))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(None, "Ошибка изменения данных", f"Ошибка: {e}")
            return False


    def delete_order_db(self, id_order):
        """Удаляет заказ из БД."""
        if not self.conn:
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("delete from orders where id_order = %s", (id_order))
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            QMessageBox.warning(None, "Ошибка удаления данных", f"Ошибка: {e}")
            return False
