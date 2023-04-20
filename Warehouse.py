from neo4j import Driver, ManagedTransaction
from Address import Address
from utils import to_array


class Warehouse:
    def __init__(self, driver: Driver):
        self.driver = driver

    @staticmethod
    def _find_address(tnx: ManagedTransaction, address_id):
        query = (
            "MATCH (a: Location {location_id: $address_id})"
            "RETURN a"
        )
        result = tnx.run(query, address_id=address_id)
        return to_array(result)

    @staticmethod
    def _create_address(tnx: ManagedTransaction, address: Address):
        query = (
            "CREATE (a: Location {location_id: $id, street: $street, city: $city, state: $state, zip: $zip})"
            "RETURN a"
        )
        locations = tnx.run(query,
                            id=address.id,
                            street=address.street,
                            city=address.city,
                            state=address.state,
                            zip=address.zip_code
                            )
        return to_array(locations)

    @staticmethod
    def _create_warehouse(tnx: ManagedTransaction, warehouse_id, name):
        query = (
            "CREATE (p: Warehouse {warehouse_id: $warehouse_id, name: $name})"
            "RETURN p"
        )
        warehouse = tnx.run(query, warehouse_id=warehouse_id, name=name)
        return to_array(warehouse)

    @staticmethod
    def _create_located_in_relationship(tnx: ManagedTransaction, warehouse_id, address: Address):
        query = (
            "MATCH (u: Warehouse{warehouse_id: $warehouse_id})"
            "MATCH (l: Location{location_id: $address_id})"
            "CREATE (u)-[r:located_in]->(l)"
            "RETURN r"
        )
        res = tnx.run(query, warehouse_id=warehouse_id, address_id=address.id)
        return to_array(res)

    @staticmethod
    def _delete_located_in_relationship(tnx: ManagedTransaction, warehouse_id):
        query = (
            "MATCH (u: Warehouse{warehouse_id: $warehouse_id})-[r:located_in]->()"
            "DELETE r"
        )
        res = tnx.run(query, warehouse_id=warehouse_id)
        return to_array(res)

    @staticmethod
    def _find_warehouse(tnx: ManagedTransaction, warehouse_id):
        query = (
            "MATCH (u: Warehouse{warehouse_id: $warehouse_id})-[r:located_in]-(a: Location)"
            "RETURN u, a"
        )
        res = tnx.run(query, warehouse_id=warehouse_id)
        data = to_array(res.data())
        return data

    @staticmethod
    def _find_item_quantity(tnx: ManagedTransaction, warehouse_id, item_id):
        query = (
            "MATCH (u: Item{item_id: $item_id})-[rel:stored_in]-(w:Warehouse{warehouse_id: $warehouse_id})"
            "RETURN rel.quantity"
        )
        res = tnx.run(query, item_id=item_id, warehouse_id=warehouse_id)
        data = to_array(res.data())
        return data

    @staticmethod
    def _remove_warehouse(tnx: ManagedTransaction, warehouse_id):
        query = (
            "MATCH (n: Warehouse {warehouse_id: $warehouse_id})"
            "DELETE n"
        )
        res = tnx.run(query, warehouse_id=warehouse_id)
        data = to_array(res.data())
        return data

    @staticmethod
    def _update_warehouse_name(tnx: ManagedTransaction, warehouse_id, name):
        query = (
            "MATCH (p:Warehouse {warehouse_id: $warehouse_id}) "
            "SET p.name = $name "
            "RETURN p"
        )
        res = tnx.run(query, warehouse_id=warehouse_id, name=name)
        data = to_array(res.data())
        return data

    def create(self, warehouse_id, name, address: Address):
        with self.driver.session(database="neo4j") as session:
            queried_address = session.execute_read(self._find_address, address.id)
            if len(queried_address) == 0:
                _ = session.execute_write(self._create_address, address)
            _ = session.execute_write(self._create_warehouse, warehouse_id, name)
            _ = session.execute_write(self._create_located_in_relationship, warehouse_id, address)

    def find_one(self, warehouse_id):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_read(self._find_warehouse, warehouse_id)
            if len(data) == 0 or len(data) > 1:
                return None
            first = data[0]
            warehouse, address = first['u'], first['a']
            return {
                "warehouse": warehouse,
                "address": address
            }

    def find_item_quantity(self, warehouse_id, item_id):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_read(self._find_item_quantity, warehouse_id, item_id)
            if len(data) == 0 or len(data) > 1:
                return None
            return data[0]['rel.quantity']

    def remove_warehouse(self, warehouse_id):
        with self.driver.session(database="neo4j") as session:
            _ = session.execute_write(self._delete_located_in_relationship, warehouse_id)
            _ = session.execute_write(self._remove_warehouse, warehouse_id)
            return 1

    def update_warehouse_name(self, warehouse_id, name):
        with self.driver.session(database="neo4j") as session:
            _ = session.execute_write(self._update_warehouse_name, warehouse_id, name)
            return 1
