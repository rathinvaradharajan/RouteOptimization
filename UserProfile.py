from neo4j import Driver
from UserService import UserService
from Address import Address


class UserProfile:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.userService = UserService(driver)

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

    def _place_order(self, user_details):
        return

    def _view_order(self, user_details):
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

    @staticmethod
    def _view_profile(user_details):
        user = user_details["user"]
        address = user_details["address"]
        print("-----------------------    -----------------------")
        print(f"User_id: {user['user_id']}\nName: {user['name']}\nAddress:\n\t"
              + f"{address['street']},\n\t{user_details['apt']},\n\t{address['city']},\n\t"
              + f"{address['state']} - {address['zip']}")

    def run(self):
        user_details = self._greet_user()
        if user_details is None:
            return
        print(f"----------------------- Welcome {user_details['user']['name']} -----------------------")
        print("1. Place an Order")
        print("2. View past orders")
        print("3. Update address")
        print("4. View profile")
        print("5. Exit")
        ops = input("Enter your operation: ")
        if ops == "1":
            self._place_order(user_details)
        elif ops == "2":
            self._view_order(user_details)
        elif ops == "3":
            self._update_address(user_details['user'])
        elif ops == "4":
            self._view_profile(user_details)
        elif ops == "5":
            return 0
        else:
            print("Invalid Input")
