from neo4j import Driver
from OrderService import OrderService


size_dict = {
    'S': 10,
    's': 10,
    'M': 20,
    'm': 20,
    'L': 50,
    'l': 50,
    'XL': 100,
    'xl': 100
}


class DriverProfile:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.order_service = OrderService(driver)

    @staticmethod
    def _fill_vehicle(orders, vehicle_size):
        selected_orders, curr = [], 0
        orders = sorted(orders, key=lambda x: x['total_size'])
        for order in orders:
            curr += order['total_size']
            if curr <= vehicle_size:
                selected_orders.append(order)
            else:
                break
        return selected_orders

    @staticmethod
    def _get_pick_up_locations(orders):
        pass

    def _start_delivery(self):
        # select a vehicle
        vehicle_size = input("Enter the vehicle size you are driving today (S/M/L/XL): ")
        size = size_dict[vehicle_size]
        # load the vehicle with items
        orders = self.order_service.find_orders_due()
        for order in orders:
            items = self.order_service.find_items_to_fill_order(order['order_id'])
            order['items'] = items
            order['total_size'] = sum([int(item['size']) for item in items])

        filled_orders = self._fill_vehicle(orders, size)
        if len(filled_orders) == 0:
            print("You need a bigger vehicle for today's delivery")
            return
        print(filled_orders)
        # compute pickup and delivery location

        # compute delivery route

        # start delivery route
        pass

    def run(self):
        print("--------------------- Welcome ---------------------")
        print("1. Start a delivery")
        print("2. Report a traffic incident")
        print("3. Exit\n")
        ops = input("Enter your operation: ")
        if ops == '1':
            self._start_delivery()
        elif ops == '2':
            pass
        elif ops == '3':
            return