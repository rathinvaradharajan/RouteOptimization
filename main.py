from neo4j import GraphDatabase
from ItemController import ItemController
from UserService import UserService
from Address import Address
from Warehouse import Warehouse
from Item import Item
from UserProfile import UserProfile
from WarehouseController import WarehouseController
import logging


def connect(uri, username, password):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver

def main():
    username = 'neo4j'
    password = '_0ctfmLWjOEH8hcEMPNKYQ0MSX8pZb4_aLDhV8pTnMY'
    uri = 'neo4j+s://98ff9419.databases.neo4j.io'
    driver = connect(uri, username, password)
    # user = UserService(driver)
    # user_address = Address(street="463 Park Dr", apt="4", state="MA",
    #                        city="Boston", zip_code="02215")
    # # user.create_user(user_id="ratz19", name="Rathin", address=user_address)
    # print(user.find_one("ratz19"))
    #
    # # Creating warehouse
    # warehouse = Warehouse(driver)
    # warehouse_address = Address(street="45 Lyman St", apt="1", state="MA",
    #                             city=", Westborough", zip_code="01581")
    # warehouse.create(warehouse_id="wareh01", name="Brainstorm Inc", address=warehouse_address)
    # print(warehouse.find_one("wareh01"))
    # user_profile = UserProfile(driver)
    # user_profile.run()

    # Creating item
    #item = Item(driver)
    # val = item.create(item_id="it02", name="Samsung Galaxy S10", description="Phone", size="12",
    #             quantity="55", warehouse_id="wareh01")
    # if val:
    #     print(item.find_one("it01"))
    # else:
    #     print("Warehouse not found")

    #print(item.find_all())

    # Warehouse Controller
    # warehouse_controller = WarehouseController(driver)
    # warehouse_controller.run()

    # Item Controller
    # item_controller = ItemController(driver)
    # item_controller.run()

    driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
