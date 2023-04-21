from neo4j import Driver, ManagedTransaction
from Address import Address
from utils import to_array


class UserService:
    def __init__(self, driver: Driver):
        self.driver = driver

    @staticmethod
    def _create_user(tnx: ManagedTransaction, user_id, name):
        query = (
            "CREATE (p: User {user_id: $user_id, name: $name})"
            "RETURN p"
        )
        user = tnx.run(query, user_id=user_id, name=name)
        return to_array(user)

    @staticmethod
    def _find_user(tnx: ManagedTransaction, user_id):
        query = (
            "MATCH (u: User{user_id: $user_id})-[r:lives_in]-(a: Location)"
            "RETURN u, r.apt, a"
        )
        res = tnx.run(query, user_id=user_id)
        data = to_array(res.data())
        return data

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
    def _find_address(tnx: ManagedTransaction, address_id):
        query = (
            "MATCH (a: Location {location_id: $address_id})"
            "RETURN a"
        )
        result = tnx.run(query, address_id=address_id)
        return to_array(result)

    @staticmethod
    def _create_lives_in_relationship(tnx: ManagedTransaction, user_id, address: Address):
        query = (
            "MATCH (u: User{user_id: $user_id})"
            "MATCH (l: Location{location_id: $address_id})"
            "CREATE (u)-[r:lives_in {apt: $apt}]->(l)"
            "RETURN r"
        )
        res = tnx.run(query, user_id=user_id, address_id=address.id, apt=address.apt)
        return to_array(res)

    @staticmethod
    def _remove_lives_in_relationship(tnx: ManagedTransaction, user_id):
        query = (
            "MATCH (u: User{user_id: $user_id})-[r:lives_in]-(:Location)"
            "DELETE r"
        )
        _ = tnx.run(query, user_id=user_id)

    def create(self, user_id, name, address: Address):
        with self.driver.session(database="neo4j") as session:
            queried_address = session.execute_read(self._find_address, address.id)
            if len(queried_address) == 0:
                _ = session.execute_write(self._create_address, address)
            _ = session.execute_write(self._create_user, user_id, name)
            _ = session.execute_write(self._create_lives_in_relationship, user_id, address)
            session.close()

    def find_one(self, user_id):
        with self.driver.session(database="neo4j") as session:
            data = session.execute_read(self._find_user, user_id)
            if len(data) == 0 or len(data) > 1:
                return None
            first = data[0]
            user, apt, address = first['u'], first['r.apt'], first['a']
            return {
                "user": user,
                "apt": apt,
                "address": address
            }

    def update_address(self, user_id, address: Address):
        with self.driver.session(database="neo4j") as session:
            _ = session.execute_write(self._remove_lives_in_relationship, user_id)
            address_exits = session.execute_read(self._find_address, address.id)
            if len(address_exits) == 0:
                _ = session.execute_write(self._create_address, address)
            _ = session.execute_write(self._create_lives_in_relationship, user_id, address)
            session.close()





