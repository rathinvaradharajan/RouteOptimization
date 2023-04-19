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
            "CREATE (u)-[r:located_in {apt: $apt}]->(l)"
            "RETURN r"
        )
        res = tnx.run(query, warehouse_id=warehouse_id, address_id=address.id, apt=address.apt)
        return to_array(res)

    @staticmethod
    def _find_warehouse(tnx: ManagedTransaction, warehouse_id):
        query = (
            "MATCH (u: Warehouse{warehouse_id: $warehouse_id})-[r:located_in]-(a: Location)"
            "RETURN u, r.apt, a"
        )
        res = tnx.run(query, warehouse_id=warehouse_id)
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
            if len(data) > 1:
                raise Exception
            first = data[0]
            warehouse, apt, address = first['u'], first['r.apt'], first['a']
            return {
                "warehouse": warehouse,
                "apt": apt,
                "address": address
            }
