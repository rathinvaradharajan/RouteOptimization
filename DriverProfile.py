from neo4j import Driver
from OrderService import OrderService
from Address import Address
from Routes import compute_best_route


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


def create_address_for_warehouse(location):
    address = Address(location['street'], '', location['city'], location['state'], location['zip'])
    return address


def create_address(order):
    location = order['delivery_location']
    apt = ''
    if 'apt' in location:
        apt = location['apt']
    address = Address(location['street'], apt, location['city'], location['state'], location['zip'])
    address.id = order['order_id']
    return address


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
        locations_dict = {}
        for order in orders:
            for item in order['items']:
                location = item['warehouse_location']
                if location['location_id'] not in locations_dict:
                    locations_dict[location['location_id']] = create_address_for_warehouse(location)
        locations = []
        for _, value in locations_dict.items():
            locations.append(value)
        return locations

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
        filled_order_ids = [order['order_id'] for order in filled_orders]
        # compute pickup and delivery location
        pickup_address = self._get_pick_up_locations(filled_orders)
        delivery_address = [create_address(order) for order in filled_orders]
        warehouses = len(pickup_address)

        # compute delivery route
        best_route = compute_best_route(pickup_address, delivery_address)
        i = 0
        while i < warehouses:
            print("Driver to Warehouse to pickup items: ")
            print(f"\t {best_route[i].to_address_str()}\n")
            op = input("Pick up done? (Y/N): ")
            if op == 'Y' or op == 'y':
                i += 1
        # update order status and warehouse count
        self.order_service.update_order_status(filled_order_ids, 'In Transit')
        self.order_service.update_item_counts(filled_order_ids)

        print("\n-----------------------------------------------------------")
        print("\nDrive to perform deliveries...\n")
        print(i, best_route)
        while i < len(best_route):
            curr_delivery = best_route[i]
            print(f"Driver following location and deliver order #: {curr_delivery.id}")
            print(f"\t {curr_delivery.to_address_str()}")
            op = input("Deliver done? (Y/N)")
            if op == 'y' or op == 'Y':
                i += 1
                # update order status
                self.order_service.update_order_status([curr_delivery.id], 'Completed')
        print("\n-----------------------------------------------------------\nDelivery done for the day. Yay!!")

    def run(self):
        print("--------------------- Welcome ---------------------")
        print("1. Start a delivery")
        print("2. Exit\n")
        ops = input("Enter your operation: ")
        if ops == '1':
            self._start_delivery()
        else:
            return
