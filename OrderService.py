import uuid
from datetime import datetime, timedelta
from neo4j import Driver, ManagedTransaction
from utils import apply_and_to_array


class OrderService:
    def __init__(self, driver: Driver):
        self.driver = driver

    @staticmethod
    def _create(tnx: ManagedTransaction, checkout_items, total_price, user_id):
        order_id = str(uuid.uuid4())
        create_order = ""
        for i, (item_id, item) in enumerate(checkout_items.items()):
            create_order += (
                f"MATCH (i{i}: Item{{item_id: '{item_id}'}})"
            )
        create_order += (
            "MATCH (u: User{user_id: $user_id})"
            "CREATE (o: Order{order_id: $order_id, total_price: $total_price, order_date: $order_date,"
            " status: 'Initiated', delivery_date: $delivery_date})"
            "CREATE (o)-[r:placed_by]->(u)"
        )
        for i, (item_id, item) in enumerate(checkout_items.items()):
            create_order += (
                f"CREATE (o)-[r{i}:contains{{quantity: {item['quantity']}}}]->(i{i})"
            )
        order_date = datetime.now()
        delivery_date = order_date + timedelta(days=5)
        tnx.run(create_order, order_id=order_id, user_id=user_id, total_price=total_price, order_date=order_date,
                delivery_date=delivery_date)
        return

    @staticmethod
    def _find_all_orders_for_user(tnx: ManagedTransaction, user_id):
        find_query = (
            "MATCH (u:User where u.user_id = $user_id)<-[:placed_by]-(o: Order)"
            "RETURN o"
        )
        res = tnx.run(find_query, user_id=user_id)
        return apply_and_to_array(res.data(), lambda x: x['o'])

    @staticmethod
    def _find_orders_due(tnx: ManagedTransaction):
        today = datetime.now() + timedelta(days=7)
        find_query = (
            "MATCH (o: Order where o.status <> 'completed' and o.delivery_date <= $today)"
            "MATCH (o)-[:placed_by]-(:User)-[r:lives_in]->(l:Location)"
            "return o, r.apt, l"
            " LIMIT 10"
        )

        def selector(x):
            order = x['o']
            address = x['l']
            address['apt'] = x['r.apt']
            order['delivery_location'] = address
            return order

        res = tnx.run(find_query, today=today)
        return apply_and_to_array(res.data(), selector)

    @staticmethod
    def _find_items_to_fill_orders(tnx: ManagedTransaction, orders):
        find_query = (
            "MATCH (o: Order where o.order_id=$order_id)-[c:contains]-(i: Item)"
            "-[r:stored_in]->(w: Warehouse)-[:located_in]->(l: Location)"
            "RETURN i, c.quantity, r.quantity, w, l"
        )
        res = tnx.run(find_query, order_id=orders)

        def selector(x):
            item = x['i']
            item['quantity'] = x['c.quantity']
            warehouse = x['l']
            warehouse['available_quantity'] = x['r.quantity']
            item['warehouse_location'] = warehouse
            return item

        return apply_and_to_array(res.data(), selector)

    def create(self, checkout_items, total_price, user_id):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._create, checkout_items, total_price, user_id)

    def find_all(self, user_id):
        with self.driver.session(database="neo4j") as session:
            return session.execute_read(self._find_all_orders_for_user, user_id)

    def find_orders_due(self):
        with self.driver.session(database="neo4j") as session:
            return session.execute_read(self._find_orders_due)

    def find_items_to_fill_order(self, orders):
        with self.driver.session(database="neo4j") as session:
            return session.execute_read(self._find_items_to_fill_orders, orders)
