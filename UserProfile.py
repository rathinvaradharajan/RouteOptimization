from neo4j import Driver
from UserService import UserService
from Address import Address
from Item import Item
from OrderService import OrderService
from utils import format_date, date_diff_to_today


class UserProfile:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.userService = UserService(driver)
        self.itemService = Item(driver)
        self.orderService = OrderService(driver)

    def _create_user(self, user_name):
        print("----------------------- Creating new user -----------------------")
        print(f"user name: {user_name}")
        name = input("Name: ")
        print("Please enter your address")
        street = input("Street: ")
        apt = input("Apt: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip: ")
        address = Address(street=street, apt=apt, city=city, state=state, zip_code=zip_code)
        self.userService.create(user_id=user_name, name=name, address=address)
        return self.userService.find_one(user_name)

    def _greet_user(self):
        while True:
            user_name = input("Enter your username: ")
            user = self.userService.find_one(user_name)
            if user is None:
                print("User doesn't exists.")
                is_create_user = input("Do you want to create a new user? (Y/N) ")
                if is_create_user == "Y" or is_create_user == "y":
                    return self._create_user(user_name)
                else:
                    return None
            else:
                return user

    def _create_order_and_checkout(self, checkout_items, total_price, user):
        self.orderService.create(checkout_items, total_price, user['user_id'])

    def _place_order(self, user_details):
        # List all items
        items_arr = self.itemService.find_all()
        catalog = {}
        for it in items_arr:
            catalog[it['u']['item_id']] = {
                'name': it['u']['name'],
                'price': float(it['u']['price']),
                'size': it['u']['size'],
                'description': it['u']['description']
            }

        print("{:<8} {:<8} {:<20} {:<45} {:<10}".format('S.No', 'Item ID', 'Name', 'Description', 'Price'))
        for i, (item_id, item_attr) in enumerate(catalog.items()):
            print("{:<8} {:<8} {:<20} {:<45} $ {:<8}".format(
                i+1,
                item_id,
                item_attr['name'],
                item_attr['description'],
                "{:,}".format(item_attr['price'])
                )
            )

        # prompt user for items to add in cart
        cart = []
        print("Add items to your cart. Use '\\q' to finish adding items")
        while True:
            user_prompt = input("Enter the item to be added in your cart: ")
            if user_prompt == "\\q":
                break
            if user_prompt not in catalog:
                print("Invalid item id entered")
            else:
                cart.append(user_prompt)
                print(f"Cart: {cart}")

        # confirm order placement
        if len(cart) == 0:
            return
        print("\n\n----------------------- Checkout  -----------------------")
        checkout_cart = {}
        for cart_item in cart:
            if cart_item in checkout_cart:
                checkout_cart[cart_item]['quantity'] += 1
                checkout_cart[cart_item]['price'] += float(catalog[cart_item]['price'])
            else:
                checkout_cart[cart_item] = {
                    'name': catalog[cart_item]['name'],
                    'quantity': 1,
                    'price': float(catalog[cart_item]['price'])
                }
        total_price = 0
        for key, value in checkout_cart.items():
            print(f"{value['name']}\nQuantity: {value['quantity']} \tPrice: {value['price']} \n")
            total_price += value['price']
        print("Total Price: $ ", "{:,}".format(total_price))
        should_checkout = input("Confirm Order? (Y/N)")
        if should_checkout == 'Y' or should_checkout == 'y':
            # place order
            self._create_order_and_checkout(checkout_cart, total_price, user_details)
        return

    def _view_order_details(self, order_id):
        items = self.orderService.find_items_to_fill_order(order_id)
        print("{:<8} {:<15} {:<10} {:<10}".format('Item Id', 'Name', 'Quantity', 'Price'))
        for item in items:
            price = "$ " + "{:,}".format(float(item['price']))
            print("{:<8} {:<15} {:<10} {:<10}".format(
                item['item_id'],
                item['name'],
                item['quantity'],
                price
            ))
        return

    def _cancel_order(self, order):
        # check if cancel is possible
        if order['status'] == 'Completed':
            print("Can't cancel completed order!!")
            return
        if date_diff_to_today(order['delivery_date']) < 3:
            print("Can't cancel since delivery date is less than 3 days away")
            return
        self.orderService.cancel_order(order['order_id'])
        print("Order cancelled")

    def _view_order(self, user):
        orders = self.orderService.find_all(user['user_id'])
        print("{:<8} {:<40} {:<20} {:<20} {:<8}".format('S.No', 'Order Id', 'Order Date', 'Delivery Date', 'Status'))
        for i, order in enumerate(orders):
            print("{:<8} {:<40} {:<20} {:<20} {:<8}".format(
                i+1,
                order['order_id'],
                format_date(order['order_date']),
                format_date(order['delivery_date']),
                order['status']
                )
            )
        while True:
            print("\n1.View order details\n2. Cancel order\n3.Exit")
            op = input("Enter the operation: ")
            if op in ['1', '2']:
                idx = int(input("Enter the order no: ")) - 1
                if op == '1':
                    self._view_order_details(orders[idx]['order_id'])
                elif op == '2':
                    self._cancel_order(orders[idx])
                    break
            else:
                break
        return

    def _update_address(self, user):
        print("Please enter your new address")
        street = input("Street: ")
        apt = input("Apt: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip: ")
        address = Address(street=street, apt=apt, city=city, state=state, zip_code=zip_code)
        self.userService.update_address(user['user_id'], address)

    def _view_profile(self, user_detail):
        user_details = self.userService.find_one(user_detail["user"]['user_id'])
        user = user_details["user"]
        address = user_details["address"]
        print("----------------------- Profile -----------------------")
        print(f"User_id: {user['user_id']}\nName: {user['name']}\nAddress:\n\t"
              + f"{address['street']},\n\t{user_details['apt']},\n\t{address['city']},\n\t"
              + f"{address['state']} - {address['zip']}")

    def run(self):
        user_details = self._greet_user()
        if user_details is None:
            return
        while True:
            print(f"\n\n----------------------- Welcome {user_details['user']['name']} -----------------------")
            print("1. Place an Order")
            print("2. View past orders")
            print("3. Update address")
            print("4. View profile")
            print("5. Exit")
            ops = input("Enter your operation: ")
            if ops == "1":
                self._place_order(user_details['user'])
            elif ops == "2":
                self._view_order(user_details['user'])
            elif ops == "3":
                self._update_address(user_details['user'])
            elif ops == "4":
                self._view_profile(user_details)
            elif ops == "5":
                return 0
            else:
                print("Invalid Input")
