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
    def _create_item(tnx: ManagedTransaction, item_id, name, description, size, price):
        query = (
            "CREATE (p: Item {item_id: $item_id, name: $name, description: $description, size: $size, price: $price})"
            "RETURN p"
        )
        warehouse = tnx.run(query, item_id=item_id, name=name, description=description, size=size, price=price)
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
    def _remove_stored_in_relationship(tnx: ManagedTransaction, warehouse_id, item_id):
        query = (
            "MATCH (n:Item {item_id: $item_id})-[r:stored_in]-(w:Warehouse {warehouse_id: $warehouse_id})"
            "DELETE r"
        )
        res = tnx.run(query, item_id=item_id, warehouse_id=warehouse_id)
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

    @staticmethod
    def _find_item_individual(tnx: ManagedTransaction, item_id):
        query = (
            "MATCH (u: Item{item_id: $item_id})"
            "RETURN u"
        )
        res = tnx.run(query, item_id=item_id)
        data = to_array(res.data())
        return data

    @staticmethod
    def _find_all(tnx: ManagedTransaction):
        query = (
            "MATCH (u: Item)"
            "RETURN u"
            " ORDER BY u.item_id"
        )
        res = tnx.run(query)
        return to_array(res.data())

    @staticmethod
    def _find_all_item_in_a_warehouse(tnx: ManagedTransaction, warehouse_id):
        query = (
            "MATCH (u: Item)-[r:stored_in]-(a: Warehouse{warehouse_id: $warehouse_id})"
            "RETURN u"
        )
        res = tnx.run(query, warehouse_id=warehouse_id)
        data = to_array(res.data())
        return data

    @staticmethod
    def _update_item_quantity(tnx: ManagedTransaction, warehouse_id, item_id, qty):
        query = (
            "MATCH (n: Item{item_id: $item_id})-[rel:stored_in]-(w: Warehouse{warehouse_id: $warehouse_id})"
            "SET rel.quantity = $qty "
            "RETURN rel.quantity"
        )
        res = tnx.run(query, item_id=item_id, warehouse_id=warehouse_id, qty=qty)
        data = to_array(res.data())
        return data

    @staticmethod
    def _remove_all_stored_in_relationship(tnx: ManagedTransaction, warehouse_id):
        query = (
            "MATCH (n: Item)-[rel:stored_in]-(a: Warehouse{warehouse_id: $warehouse_id})"
            "DELETE rel"
        )
        res = tnx.run(query, warehouse_id=warehouse_id)
        return to_array(res)

    @staticmethod
    def _update_item(tnx: ManagedTransaction, item_id, name, description, size, price):
        query = (
            "MATCH (p:Item {item_id: $item_id}) "
            "SET p.name = $name "
            "SET p.description = $description "
            "set p.size = $size "
            "set p.price = $price "
            "RETURN p"
        )
        res = tnx.run(query, item_id=item_id, name=name, description=description, size=size, price=price)
        return to_array(res)

    @staticmethod
    def _remove_all_relationship_of_item(tnx: ManagedTransaction, item_id):
        query = (
            "MATCH (n:Item {item_id: $item_id})-[r:stored_in]->()"
            "DELETE r"
        )
        res = tnx.run(query, item_id=item_id)
        return to_array(res)

    @staticmethod
    def _delete_item(tnx: ManagedTransaction, item_id):
        query = (
            "MATCH (n:Item {item_id: $item_id})"
            "DELETE n"
        )
        res = tnx.run(query, item_id=item_id)
        return to_array(res)

    def create_item_and_add_to_warehouse(self, item_id, name, description, size, quantity,
                                         warehouse_id, price):
        with self.driver.session(database="neo4j") as session:
            queried_address = session.execute_read(self._find_warehouse, warehouse_id)
            if len(queried_address) == 0:
                return 0
            _ = session.execute_write(self._create_item, item_id, name, description, size, price)
            _ = session.execute_write(self._create_stored_in_relationship, item_id,
                                      warehouse_id, quantity)
            return 1

    def create_item(self, item_id, name, description, size, price):
        with self.driver.session(database="neo4j") as session:
            _ = session.execute_write(self._create_item, item_id, name, description, size, price)
            return 1

    def find_one(self, item_id, warehouse):
        with self.driver.session(database="neo4j") as session:
            if warehouse:
                data = session.execute_read(self._find_item, item_id)
            else:
                data = session.execute_read(self._find_item_individual, item_id)

            if len(data) == 0 or len(data) > 1:
                return None
            first = data[0]

            if warehouse:
                item, warehouse = first['u'], first['a']
                return {
                    "item": item,
                    "warehouse": warehouse
                }
            else:
                return first['u']

    def find_all(self):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_read(self._find_all)
            return data

    def find_all_item_in_a_warehouse(self, warehouse_id):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_read(self._find_all_item_in_a_warehouse, warehouse_id)
            return data

    def update_item_quantity(self, warehouse_id, item_id, qty):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_write(self._update_item_quantity, warehouse_id, item_id, qty)
            if len(data) == 0 or len(data) > 1:
                return None
            return data[0]['rel.quantity']

    def remove_item_from_warehouse(self, warehouse_id, item_id):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_write(self._remove_stored_in_relationship, warehouse_id, item_id)
            return 1

    def remove_all_item_from_warehouse(self, warehouse_id):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_write(self._remove_all_stored_in_relationship, warehouse_id)
            return 1

    def add_item_to_warehouse(self, warehouse_id, item_id, qty):
        with self.driver.session(database="neo4j") as session:
            _ = session.execute_write(self._create_stored_in_relationship, item_id,
                                      warehouse_id, qty)
            return 1

    def update_item(self, item_id, name, description, size, price):
        with self.driver.session(database="neo4j") as session:
            _ = session.execute_write(self._update_item, item_id, name, description, size, price)
            return 1

    def delete_item(self, item_id):
        with self.driver.session(database="neo4j") as session:
            _ = session.execute_write(self._remove_all_relationship_of_item, item_id)
            _ = session.execute_write(self._delete_item, item_id)
            return 1
