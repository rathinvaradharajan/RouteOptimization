from neo4j import Driver
from Warehouse import Warehouse
from Item import Item


class ItemController:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.itemService = Item(driver)

    def _view_all_items(self):
        items = self.itemService.find_all()
        if len(items) != 0:
            i = 1
            print("S.NO\t", end="", flush=True)
            print("Item ID\t\t", end="", flush=True)
            print("Size\t\t", end="", flush=True)
            print("Name\t\t\t\t\t\t\t", end="", flush=True)
            print("Description")
            for item in items:
                print(f"{i}. ", end="\t\t", flush=True)
                print(item['u']['item_id'], end="\t\t", flush=True)
                print(item['u']['size'], end="\t\t\t", flush=True)
                print(item['u']['name'], end="\t\t\t\t", flush=True)
                print(item['u']['description'])
                i = i + 1
            return 1
        else:
            print('No items available')
            return None

    def _add_item(self):
        while True:
            item_id = input("Enter the item id: ")
            item = self.itemService.find_one(item_id, False)
            if item is None:
                name = input("Enter the name for the item: ")
                size = input("Enter the size for the item: ")
                description = input("Enter the description for the item: ")
                return self.itemService.create_item(item_id, name, description, size)
            else:
                inp = input('Item ID already exists. Do you want to retry? (Y/N): ')
                if inp.lower() == 'y':
                    continue
                else:
                    return None

    def _update_item(self):
        while True:
            item_id = input("Enter the item id: ")
            item = self.itemService.find_one(item_id, False)
            print(item)
            if item is None:
                inp = input('Invalid item ID. Do you want to re-enter? (Y/N): ')
                if inp.lower() == 'y':
                    continue
                else:
                    return None
            else:
                name = input("Enter the name for the item: ")
                size = input("Enter the size for the item: ")
                description = input("Enter the description for the item: ")
                return self.itemService.update_item(item_id, name, description, size)

    def _remove_item(self):
        while True:
            item_id = input("Enter the item id: ")
            item = self.itemService.find_one(item_id, False)
            if item is None:
                inp = input('Invalid item ID. Do you want to re-enter? (Y/N): ')
                if inp.lower() == 'y':
                    continue
                else:
                    return None
            else:
                inp = input("Removing this item will remove all of its relationship as well. "
                            "Are you sure (Y/N): ")
                if inp.lower() == 'y':
                    return self.itemService.delete_item(item_id)
                else:
                    return None

    def run(self):
        while True:
            print(f"\n----------------------- Welcome to Item's Menu -----------------------")
            print("1. View all items")
            print("2. Create an item")
            print("3. Update an item")
            print("4. Delete an item")
            print("5. Exit")
            ops = input("\nEnter your operation: ")
            if ops == "1":
                self._view_all_items()
            elif ops == "2":
                ret = self._add_item()
                if ret is not None:
                    print("Item added successfully")
            elif ops == "3":
                ret = self._update_item()
                if ret is not None:
                    print("Item updated successfully")
            elif ops == "4":
                ret = self._remove_item()
                if ret is not None:
                    print("Item deleted successfully")
            elif ops == "5":
                return
            else:
                print("Invalid Input.")
