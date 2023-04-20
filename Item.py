from neo4j import Driver, ManagedTransaction
from utils import to_array


class Item:
    def __init__(self, driver: Driver):
        self.driver = driver

    @staticmethod
    def _find_warehouse(tnx: ManagedTransaction, warehouse_id):
        query = (
            "MATCH (a: Warehouse {warehouse_id: $warehouse_id})"
            "RETURN a"
        )
        result = tnx.run(query, warehouse_id=warehouse_id)
        return to_array(result)

    @staticmethod
    def _create_item(tnx: ManagedTransaction, item_id, description, size):
        query = (
            "CREATE (p: Item {item_id: $item_id, description: $description, size: $size})"
            "RETURN p"
        )
        warehouse = tnx.run(query, item_id=item_id, description=description, size=size)
        return to_array(warehouse)

    @staticmethod
    def _create_stored_in_relationship(tnx: ManagedTransaction, item_id,
                                       warehouse_id, quantity):
        query = (
            "MATCH (u: Item{item_id: $item_id})"
            "MATCH (l: Warehouse{warehouse_id: $warehouse_id})"
            "CREATE (u)-[r:stored_in {quantity: $quantity}]->(l)"
            "RETURN r"
        )
        res = tnx.run(query, item_id=item_id, warehouse_id=warehouse_id, quantity=quantity)
        return to_array(res)

    @staticmethod
    def _find_item(tnx: ManagedTransaction, item_id):
        query = (
            "MATCH (u: Item{item_id: $item_id})-[r:stored_in]-(a: Warehouse)"
            "RETURN u, a"
        )
        res = tnx.run(query, item_id=item_id)
        data = to_array(res.data())
        return data

    def create(self, item_id, description, size, quantity, warehouse_id):
        with self.driver.session(database="neo4j") as session:
            queried_address = session.execute_read(self._find_warehouse, warehouse_id)
            if len(queried_address) == 0:
                return 0
            _ = session.execute_write(self._create_item, item_id, description, size)
            _ = session.execute_write(self._create_stored_in_relationship, item_id,
                                      warehouse_id, quantity)
            return 1

    def find_one(self, item_id):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_read(self._find_item, item_id)
            if len(data) > 1:
                raise Exception
            first = data[0]
            item, warehouse = first['u'], first['a']
            return {
                "item": item,
                "warehouse": warehouse
            }
