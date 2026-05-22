class Order:
    def __init__(self, id_o, id_status, status_name, id_pick_up_point, pick_up_point_name, date_order, date_delivery, id_client):
        self.id = id_o
        self.id_status = id_status
        self.status_name = status_name
        self.id_pick_up_point = id_pick_up_point
        self.pick_up_point_name = pick_up_point_name
        self.date_order = date_order
        self.date_delivery = date_delivery
        self.id_client = id_client
