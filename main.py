from neo4j import GraphDatabase
from User import User
from Address import Address
from Warehouse import Warehouse
import logging


def connect(uri, username, password):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver

def main():
    username = 'neo4j'
    password = '_0ctfmLWjOEH8hcEMPNKYQ0MSX8pZb4_aLDhV8pTnMY'
    uri = 'neo4j+s://98ff9419.databases.neo4j.io'
    driver = connect(uri, username, password)
    user = User(driver)
    user_address = Address(street="463 Park Dr", apt="4", state="MA",
                           city="Boston", zip_code="02215")
    # user.create_user(user_id="ratz19", name="Rathin", address=user_address)
    print(user.find_one("ratz19"))

    # Creating warehouse
    warehouse = Warehouse(driver)
    warehouse_address = Address(street="45 Lyman St", apt="1", state="MA",
                                city="Westborough", zip_code="01581")
    #warehouse.create(warehouse_id="wareh01", name="Brainstorm Inc", address=warehouse_address)
    print(warehouse.find_one("wareh01"))

    driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
