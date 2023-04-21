from neo4j import Driver
from Warehouse import Warehouse
from Address import Address
from Item import Item


class WarehouseController:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.warehouseService = Warehouse(driver)
        self.itemService = Item(driver)

    def _create_warehouse(self, warehouse_id):
        print("----------------------- Creating new warehouse -----------------------")
        print(f"warehouse id: {warehouse_id}")
        name = input("Name: ")
        print("Please enter your address")
        street = input("Street: ")
        city = input("City: ")
        state = input("State: ")
        zip_code = input("Zip: ")
        address = Address(street=street, apt="apt", city=city, state=state, zip_code=zip_code)
        self.warehouseService.create(warehouse_id=warehouse_id, name=name, address=address)
        return self.warehouseService.find_one(warehouse_id)

    def _create_warehouse_main_menu(self):
        while True:
            warehouse_id = input("Enter the warehouse id: ")
            warehouse = self.warehouseService.find_one(warehouse_id)
            if warehouse is None:
                return self._create_warehouse(warehouse_id)
            else:
                inp = input('Warehouse ID already exists. Do you want to retry? (Y/N): ')
                if inp.lower() == 'y':
                    continue
                else:
                    return None

    def _enter_warehouse_main(self):
        while True:
            warehouse_id = input("Enter the warehouse id: ")
            warehouse = self.warehouseService.find_one(warehouse_id)
            if warehouse is None:
                print("Warehouse Not Found.")
                inp = input("Do you want to retry entering? (Y/N): ")
                if inp.lower() == 'y':
                    continue
                else:
                    return None
            else:
                return warehouse

    def _warehouse_init(self):
        while True:
            print("\n------------- Warehouse Main Menu --------------")
            print("1. Create warehouse")
            print("2. Enter existing warehouse")
            print("3. Exit warehouse menu")
            ops = input("\nEnter your operation: ")
            print('')

            if ops == "1":
                warehouse = self._create_warehouse_main_menu()
                if warehouse is None:
                    continue
                else:
                    print('\nWarehouse created')
                    return warehouse
            elif ops == "2":
                warehouse = self._enter_warehouse_main()
                if warehouse is None:
                    continue
                else:
                    return warehouse
            elif ops == '3':
                return None
            else:
                print("Invalid Input.")
                continue

    def _view_all_items(self, warehouse):
        items = self.itemService.find_all_item_in_a_warehouse(
            warehouse_id=warehouse['warehouse_id'])
        if len(items) != 0:
            i = 1
            print("S.NO\t", end="", flush=True)
            print("Item ID\t\t", end="", flush=True)
            print("Size\t\t", end="", flush=True)
            print("Quantity\t\t", end="", flush=True)
            print("Price\t\t", end="", flush=True)
            print("Item Name")
            for item in items:
                quantity = self.warehouseService.find_item_quantity(
                    warehouse_id=warehouse['warehouse_id'],
                    item_id=item['u']['item_id'])
                print(f"{i}. ", end="\t\t", flush=True)
                print(item['u']['item_id'], end="\t\t", flush=True)
                print(item['u']['size'], end="\t\t\t", flush=True)
                print(quantity, end="\t\t\t\t", flush=True)
                print(item['u']['price'], end="\t\t\t\t", flush=True)
                print(item['u']['name'])
                i = i + 1
            return 1
        else:
            print('No items found in this warehouse')
            return None

    def _update_item_qty(self, warehouse):
        if self._view_all_items(warehouse) is None:
            return
        else:
            while True:
                item_id = input("\nEnter the item ID you want to update quantity for: ")
                item = self.itemService.find_one(item_id, True)
                if item is None:
                    print('Invalid item')
                    retry = input('Do you want to retry? Y/N: ')
                    if retry.lower() == 'y':
                        continue
                    else:
                        break
                else:
                    qty = input('Enter the quantity: ')
                    print(qty, warehouse['warehouse_id'], item_id, qty)
                    quantity = self.itemService.update_item_quantity(warehouse['warehouse_id'],
                                                                     item_id, qty)
                    if quantity is not None:
                        print('Update successful')
                        return 1
                    else:
                        print('Update unsuccessful')
                        return 0

    def _remove_item_from_warehouse(self, warehouse):
        if self._view_all_items(warehouse) is None:
            return
        else:
            while True:
                item_id = input("\nEnter the item ID you want to remove from this warehouse: ")
                item = self.itemService.find_one(item_id, True)
                if item is None:
                    print('Invalid item')
                    retry = input('Do you want to retry? Y/N: ')
                    if retry.lower() == 'y':
                        continue
                    else:
                        break
                else:
                    ret = self.itemService.remove_item_from_warehouse(warehouse['warehouse_id'],
                                                                      item_id)
                    if ret is not None:
                        print('Update successful')
                        return 1
                    else:
                        print('Update unsuccessful')
                        return 0

    def _empty_warehouse(self, warehouse):
        if self._view_all_items(warehouse) is None:
            return
        inp = input(f"\nAre you sure you want to empty the warehouse - "
                    f"{warehouse['warehouse_id']} (Y/N)? ")
        if inp.lower() == 'y':
            ret = self.itemService.remove_all_item_from_warehouse(warehouse['warehouse_id'])
            if ret is not None:
                print('Update successful')
                return 1
            else:
                print('Update unsuccessful')
                return 0
        else:
            return

    def _check_details_of_warehouse(self, warehouse):
        warehouse = self.warehouseService.find_one(warehouse['warehouse']['warehouse_id'])
        warehouse_data = warehouse['warehouse']
        warehouse_address = warehouse['address']
        print('Warehouse Details')
        print(f"ID: {warehouse_data['warehouse_id']}\n"
              f"Name: {warehouse_data['name']}\n"
              f"Address: {warehouse_address['street']}, {warehouse_address['city']}, "
              f"{warehouse_address['state']} - {warehouse_address['zip']}\n")

    def _update_this_warehouse_name(self, warehouse):
        while True:
            name = input('Enter name of this warehouse: ')
            if len(name) == 0:
                print('Name is empty. Renter')
            else:
                _ = self.warehouseService.update_warehouse_name(warehouse['warehouse_id'], name)
                print('Warehouse name updated successfully')
                return

    def _delete_warehouse(self, warehouse):
        inp = input(f"Deleting this warehouse will delete all of its relationships as well."
                    f" Are you sure: "
                    f"(Y/N)? ")
        if inp.lower() == 'y':
            _ = self.itemService.remove_all_item_from_warehouse(warehouse['warehouse_id'])
            _ = self.warehouseService.remove_warehouse(warehouse['warehouse_id'])
            print('Warehouse deleted')
            return 1
        else:
            return 0

    def _add_item_to_warehouse(self, warehouse):
        while True:
            item_id = input("Enter the item ID you want to add to this warehouse: ")
            item = self.itemService.find_one(item_id, False)
            if item is None:
                print('Invalid item')
                retry = input('Do you want to retry? Y/N: ')
                if retry.lower() == 'y':
                    continue
                else:
                    break
            else:
                qty = input('Enter the quantity: ')
                quantity = self.itemService.add_item_to_warehouse(warehouse['warehouse_id'],
                                                                  item_id, qty)
                if quantity is not None:
                    print('Item added successfully')
                    return 1
                else:
                    print('Update unsuccessful')
                    return 0

    def run(self):
        while True:
            warehouse_details = self._warehouse_init()
            if warehouse_details is None:
                print('Exiting warehouse menu.')
                return
            while True:
                print(
                    f"\n----------------------- Welcome to warehouse {warehouse_details['warehouse']['name']} -----------------------")
                print("1. View all items in this warehouse")
                print("2. Add an item to this warehouse")
                print("3. Update an item quantity in this warehouse")
                print("4. Remove an item from this warehouse")
                print("5. Empty warehouse")
                print("6. Check this warehouse details")
                print("7. Update this warehouse name")
                print("8. Delete this warehouse")
                print("9. Back to warehouse main menu")
                print("10. Exit")
                ops = input("\nEnter your operation: ")
                print('')
                if ops == "1":
                    self._view_all_items(warehouse_details['warehouse'])
                elif ops == "2":
                    self._add_item_to_warehouse(warehouse_details['warehouse'])
                elif ops == "3":
                    self._update_item_qty(warehouse_details['warehouse'])
                elif ops == "4":
                    self._remove_item_from_warehouse(warehouse_details['warehouse'])
                elif ops == "5":
                    self._empty_warehouse(warehouse_details['warehouse'])
                elif ops == "6":
                    self._check_details_of_warehouse(warehouse_details)
                elif ops == "7":
                    self._check_details_of_warehouse(warehouse_details)
                    self._update_this_warehouse_name(warehouse_details['warehouse'])
                elif ops == "8":
                    ret = self._delete_warehouse(warehouse_details['warehouse'])
                    if ret == 1:
                        break
                elif ops == "9":
                    break
                elif ops == "10":
                    return
                else:
                    print("Invalid Input.")
