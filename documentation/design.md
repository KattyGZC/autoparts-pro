# Major Design Decisions and Trade-offs overview

## General Approach to the problem
The problem is to find the best way to optimize the repair orders based on the inventory parts available and the profit that can be made. The best way to do this is to use a priority queue to find the best way to optimize the repair orders. 

## Architecture
For this challenge, I have chosen to use a monolithic architecture with Clean Architecture principles, but keeping a decoupled structure between frontend and backend, orchestrating all with Docker. This decision was made to focus on the core functionality of the system and to keep the codebase simple and easy to maintain. It has use cases as classes with specific methods (CRUD operations) and optimization logic separated from the domain logic. Instead, I did business validation and error handling in the use cases, and domain validation and error handling in the domain logic. 
The used stack is: 
- Backend: Python 3.12, FastAPI, SQLAlchemy
- Frontend: React, Vite, Axios, React Router DOM
- Database: PostgreSQL
- Containerization: Docker, Docker Compose
- Testing: Pytest
- Mocking: Faker

## Database Design
The safer and standard way is design a normalized relational schema. It will use PostgreSQL as the database. In this case we have to design a database schema that efficiently supports core business processes, minimizes stock shortages and waste, optimizes repair order processing, keeps scalable and maintainable as the system grows.  It will have five tables: Customer, Vehicle, InventoryParts, RepairOrder and RepairOrderPart. The last one is a junction table for the many-to-many relationship between RepairOrder and InventoryParts.

1. **Customer**: id, name, email, phone, address, is_active

Central entity to link with Vehicle and RepairOrder. Keeping customer data separated from vehicle data to avoid data duplication.

2. **Vehicle**: id, customer_id, model, brand, year, license_plate, color, is_active

Vehicles are serviced assets, tightly coupled repair orders. 

3. **InventoryParts**: id, name, description, cost, final_price, stock_quantity, is_active

Central to the inventory system, every repair order will use parts from the inventory. Tracking stock directly in this table keeps inventory management simple and efficient.

4. **RepairOrder**: id, customer_id, vehicle_id, date_in, date_out, date_expected_out, status, labor_cost, is_active, total_cost_repair, created_at, updated_at

Represents each repair task, linking to Customer, Vehicle and parts. Storing vehicle and customer references allows quick association.

5. **RepairOrderPart**: id, repair_order_id, inventory_part_id, quantity, is_active, created_at, updated_at

Many-to-many relationship between repair orders and parts used in them. It enables tracking of parts used in each repair order and decouples part usage from inventory tracking. Besides, it supports optimization logic: given current inventory, which repair order can be fulfilled

### Normalization Approach
The database schema is normalized to third normal form (3NF), which means that it is free of any transitive dependencies and there are no partial dependencies. This ensures data integrity and reduces the risk of data anomalies.
- Ensure that all attributes are atomic and independent of each other.
- Remove partial dependencies between attributes.
- Remove transitive dependencies.

### Trade-offs
- Storing stock directly in InventoryPart is simple and performant, but it can lead to data consistency issues if not properly managed. 
- Avoiding embedded structures ensure relational integrity and simplify reporting and analytics.
- Slightly more JOINs in queries, but it's a small price to pay for the benefits of a normalized schema, JOINs are optimized in PostgreSQL.

### Limitations
1. **Stock trakings lacks audit trail**: The "stock" field in "InventoryParts" is efficient but doesn't provide a history of stock changes, making it challenging to track inventory issues of perform audits.
2. **Scalability for multi-branch operations**: The current design assumes a single store. Supporting multiple stores would require refactoring and adding location-based inventory control.
3. **Lack of historical pricing and cost tracking**: Only the current cost is stored per part. There is no mechanism to track cost changes and variations over time, which limits accurate profitability and historical analysis.


## Testing Strategy
I use SQLite as database for testing, and pytest as testing framework. This allows me a little bit more speed and simplicity in testing, and it's a good choice for this challenge.

I omited exhaustive testing of all use cases, due to time constraints. Instead, I focused on testing the most critical and complex use cases, such as the repair order optimization logic.

## Business challenges Solutions
I implemented a priority queue to find the best way to optimize the repair orders. It solves the main business challenge: maximizing profit while minimizing stock shortages and waste. Moreover, I implemented a strong CRUD system for repair orders, inventory parts, customers and vehicles.

### Implemented Features
1. Complete CRUDs with most important validation and error handling.
- Customer (customer_router.py)
- Vehicle (vehicle_router.py)
- InventoryPart (inventory_part_router.py)
- RepairOrder (repair_order_router.py)
- RepairOrderPart (repair_order_part_router.py)

Note: I decided to avoid delete operation because it's not a common practice in real world applications, so I used is_active field to mark records as deleted. This is a good practice for data integrity.

2. Order Repair Optimization (repair_order_router.py) with decoupled use cases in diferent modules.
- validate_order_inventory: Validates if an order can be fulfilled with the current inventory.
- calculate_order_profit: Calculates the estimated profit of an order.
- select_orders_by_profit: Runs all flow
This logic respects inventory constraints and prioritizes orders with higher profit.

3. Database
- Mapping all entities to tables using SQLAlchemy
- To migrations I used Alembic

4. Testing
- I implemented test to critical logic, using SQLite in-memory database. conftest.py was configured to facilitate more tests in the future.

5. Containerization
- I used Docker and Docker Compose to containerize the application. This allows to run the application in a consistent environment and to make it easy to scale and deploy.

6. Documentation
- I used Swagger to document the API. This allows to have a clear and easy way to understand the API and to make it easy to test the API. FastAPI automatically generates the documentation which is a great advantage.


## Limitations
- Lack of integration testing in the end-to-end flow.
- Doesn't include authentication and authorization.
- Doesn't cover cases like concurrency or cascade rollbacks.

## Future Improvements
- Add authentication, authorization and role management.
- Add integration testing.
- Add concurrency control or locking in selection of orders.
- Add cascade rollbacks.
- Add historical pricing and cost tracking.
- Add stock tracking audit trail.
- Add scalability for multi-branch operations.
- Add reporting and analytics.

## Frontend
- I used React to build the frontend. This allows to have a modern and responsive user interface. Vite is used as a build tool and Axios is used for HTTP requests.
- The interface is simple and easy to use, with a clear and intuitive layout. I take some considerations to make it user-friendly and easy to navigate.
- In the future, there is possible to add more features to the frontend, such as a dashboard to monitor the inventory and repair orders.