# Route Optimization System

# Introduction
Route optimization system is a project that aims to address the problem of determining the most effective route for one or more vehicles to travel in order to visit a specific set of locations. This project considers multiple factors such as vehicle capacity, delivery windows, traffic conditions, and delivery priorities to minimize the total distance or time required to complete all deliveries while still satisfying all delivery constraints.

Given the current supply chain shortages, solving this problem is crucial for efficient delivery operations. In this project, we aim to address a simplified version of this problem to gain a deeper understanding of its complexities.

# Functionality
The system provides functionalities from the standpoint of three types of users who will be using this application:

* Customers - People who order different items
* Drivers - People who deliver their assigned orders
* Inventory Managers - People who manage the inventory and assign orders to drivers

# Customer Functionality
A customer can perform the following operations:

* Place an order: A customer can place an order by providing the item details, delivery address, and delivery time.
* View an order: A customer can view the details of their existing order(s).
* Update an order: A customer can update the details of their existing order(s).
* Delete an order: A customer can delete their existing order(s).

# Driver Functionality
A driver can perform the following operations:

* Deliver an order: A driver can mark an order as delivered once they have completed the delivery.
* View the items to be delivered: A driver can view the details of the items they are assigned to deliver.

# Inventory Manager Functionality
An inventory manager can perform the following operations:

* Assign orders to drivers: An inventory manager can assign orders to the respective drivers.
* View order details: An inventory manager can view the details of all the orders.
* View order details: An inventory manager can view the details of all the orders.

# Technologies Used
* Python
* Neo4j Database

# Setup Instructions
1. Install Neo4j Database.
2. Install Python version 3.4 or later
3. Install Neo4j driver for python from PIP using command - 'pip install neo4j' 
4. Clone the project from GitHub.
5. Open the terminal and navigate to the project directory.
6. Run pip install -r requirements.txt to install the dependencies.
7. Start the Neo4j Database.
8. Run python app.py to start the application.

# Conclusion
The route optimization system is a useful tool for delivery operations to optimize their routes and minimize the total distance or time required to complete all deliveries while still satisfying all delivery constraints. The system provides different functionalities for customers, drivers, and inventory managers to manage their orders efficiently.


