from neo4j import GraphDatabase
from UserProfile import UserProfile
from WarehouseController import WarehouseController


def connect(uri, username, password):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver


def main():
    username = 'neo4j'
    password = '_0ctfmLWjOEH8hcEMPNKYQ0MSX8pZb4_aLDhV8pTnMY'
    uri = 'neo4j+s://98ff9419.databases.neo4j.io'
    try:
        driver = connect(uri, username, password)

        user_profile = UserProfile(driver)
        warehouse_cnt = WarehouseController(driver)

        print("------------------------------ Welcome ------------------------------")
        print("Login as\n1. User\n2. Driver\n3. Warehouse Manager\n")
        op = input("Enter the option: ")
        if op == '1':
            user_profile.run()
        elif op == '2':
            pass
        elif op == '3':
            warehouse_cnt.run()

        driver.close()
    except Exception as e:
        print("Unable to connect to DB. ", e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
